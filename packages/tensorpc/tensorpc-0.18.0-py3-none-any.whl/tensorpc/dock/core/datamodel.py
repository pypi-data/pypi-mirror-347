import asyncio
import contextlib
from collections.abc import Mapping, Sequence
from functools import partial
import time
from typing import (Any, Callable, Coroutine, Generic, Optional, TypeVar,
                    Union, cast)

from mashumaro.codecs.basic import BasicDecoder, BasicEncoder
from pydantic import field_validator
from typing_extensions import Self, TypeAlias, override

from tensorpc.core.annolib import AnnotatedFieldMeta, BackendOnlyProp, get_dataclass_field_meta_dict
from tensorpc.core.datamodel.asdict import asdict_no_deepcopy_with_field
from tensorpc.core.datamodel.draftast import DraftASTNode
from tensorpc.core.datamodel.draftstore import DraftFileStorage, DraftStoreBackendBase
import tensorpc.core.datamodel.jmes as jmespath
from tensorpc.core import dataclass_dispatch as dataclasses
from tensorpc.core.datamodel.draft import (
    DraftBase, DraftFieldMeta, DraftUpdateOp, apply_draft_update_ops, capture_draft_update,
    create_draft, create_draft_type_only, enter_op_process_ctx,
    evaluate_draft_ast_noexcept, get_draft_ast_node, get_draft_update_context, get_draft_update_context_noexcept, prevent_draft_update, stabilize_getitem_path_in_op_main_path)
from tensorpc.core.datamodel.events import (DraftChangeEvent,
                                            DraftChangeEventHandler,
                                            DraftEventType,
                                            update_model_with_change_event)
from tensorpc.dock import appctx
from tensorpc.dock.core.component import (Component, ContainerBase,
                                          ContainerBaseProps, DraftOpUserData,
                                          EventSlotEmitter,
                                          EventSlotNoArgEmitter, UIType,
                                          undefined_comp_dict_factory_with_exclude,
                                          undefined_comp_obj_factory)
from tensorpc.dock.coretypes import StorageType

from ..jsonlike import Undefined, as_dict_no_undefined, undefined
from .appcore import Event

T = TypeVar("T")
_T = TypeVar("_T")
_CORO_NONE: TypeAlias = Union[Coroutine[None, None, None], None]

@dataclasses.dataclass
class DataModelProps(ContainerBaseProps):
    dataObject: Any = dataclasses.field(default_factory=dict)

def _print_draft_change_event(ev: DraftChangeEvent, draft_expr_str_dict):
    print("DraftChangeEvent:")
    for k, v in ev.type_dict.items():
        k_expr = draft_expr_str_dict[k]
        if not ev.old_value_dict:
            print(f"{k_expr}|{v}: New: {ev.new_value_dict[k]}")
        else:
            print(f"{k_expr}|{v}: {ev.old_value_dict[k]} -> {ev.new_value_dict[k]}")

@dataclasses.dataclass
class _DataclassSer:
    obj: Any

def _dict_facto_with_exclude(x: list[tuple[str, Any, Any]], exclude_field_ids: set[int]):
    res: dict[str, Any] = {}
    for k, v, f in x:
        if id(f) in exclude_field_ids:
            continue
        if not isinstance(v, (Undefined, BackendOnlyProp)):
            res[k] = v
    return res

class DataModel(ContainerBase[DataModelProps, Component], Generic[_T]):
    """DataModel is the model part of classic MVC pattern, child components can use `bind_fields` to query data from
    this component.
    
    Pitfalls:
        model may be replaced when you connect it to a storage, you should always access model instance via property instead of 
            keep it by user.
    """

    def __init__(
        self,
        model: _T,
        children: Union[Sequence[Component], Mapping[str, Component]],
        model_type: Optional[type[_T]] = None,
        debug: bool = False
    ) -> None:
        """
        Args:
            model: the model object
            children: child components
            model_type: the type of model, if not provided, we will use type(model) as model type.
                this is required when you use a generic model because we can't get type info
                in real object. 
                ```
                gdm = DataModel(GenericModel(), ..., model_type=GenericModel[int])
                ```
                We recommend to inherit your generic model with fixed type vars instead of
                use this argument.
        """
        if children is not None and isinstance(children, Sequence):
            children = {str(i): v for i, v in enumerate(children)}
        super().__init__(UIType.DataModel,
                         DataModelProps,
                         children,
                         allowed_events=[])
        self.prop(dataObject=model)
        self._model: _T = model
        self._model_type = model_type or type(model)
        self._backend_draft_update_event_key = "__backend_draft_update"
        self._backend_storage_fetched_event_key = "__backend_storage_fetched"

        self.event_draft_update: EventSlotEmitter[
            list[DraftUpdateOp]] = self._create_emitter_event_slot(
                self._backend_draft_update_event_key)
        self.event_storage_fetched: EventSlotEmitter[_T] = self._create_emitter_event_slot(
            self._backend_storage_fetched_event_key)

        self._draft_store_handler_registered: bool = False
        self._draft_store_data_fetched = False
        model_type_real = type(model)
        self._debug = debug
        self._is_model_dataclass = dataclasses.is_dataclass(model_type_real)
        self._is_model_pydantic_dataclass = dataclasses.is_pydantic_dataclass(
            model_type_real)
        self._flow_exclude_field_ids: set[int] = set()
        if dataclasses.is_dataclass(model_type_real):
            field_meta_dict = get_dataclass_field_meta_dict(model_type_real)
            for k, v in field_meta_dict.items():
                if v.annotype.annometa is not None:
                    for tt in v.annotype.annometa:
                        if isinstance(tt, DraftFieldMeta):
                            if tt.is_external:
                                if v.field.default is dataclasses.MISSING and v.field.default_factory is dataclasses.MISSING:
                                    raise ValueError(f"external field {v.field.name} must have default value or factory"
                                        " because this field is managed by user, it won't be stored to draft storage.")
                                self._flow_exclude_field_ids.add(v.field_id)
                            break

        self._mashumaro_decoder: Optional[BasicDecoder] = None
        self._mashumaro_encoder: Optional[BasicEncoder] = None

        self._draft_change_event_handlers: dict[tuple[str, ...], dict[
            Callable, DraftChangeEventHandler]] = {}

        # self.event_after_mount.on(self._init)

        self._store: Optional[DraftFileStorage] = None

        self._lock = asyncio.Lock()

    async def _run_all_draft_change_handlers_when_init(self):
        all_handlers = []
        for handlers in self._draft_change_event_handlers.values():
            for h in handlers.values():
                val_dict: dict[str, Any] = {}
                type_dict: dict[str, DraftEventType] = {}
                for k, expr in h.draft_expr_dict.items():
                    obj = evaluate_draft_ast_noexcept(expr, self.model)
                    val_dict[k] = obj
                    type_dict[k] = DraftEventType.MountChange
                # TODO if eval failed, should we call it during init?
                all_handlers.append(partial(h.handler, DraftChangeEvent(type_dict, {k: None for k in val_dict}, val_dict)))
        with prevent_draft_update():
            await self.run_callbacks(
                all_handlers,
                change_status=False,
                capture_draft=False)

    # async def _init(self):
    #     # we should trigger all draft change event handler when init or model fetched from storage.
    #     if not self._draft_store_handler_registered:
    #         await self._run_all_draft_change_handlers_when_init()

    async def _run_draft_effect_handler(self, handler: DraftChangeEventHandler, is_mount: bool):
        should_run_handler = False
        if not self._draft_store_handler_registered:
            should_run_handler = True
        else:
            should_run_handler = self._draft_store_data_fetched

        if should_run_handler:
            val_dict: dict[str, Any] = {}
            type_dict: dict[str, DraftEventType] = {}
            for k in handler.draft_expr_dict.keys():
                obj = handler.evaluate_draft_expr_noexcept(k, self.model)
                val_dict[k] = obj
                type_dict[k] = DraftEventType.MountChange
            # TODO if eval failed, should we call it during init?
            if is_mount:
                ev = DraftChangeEvent(type_dict, {k: None for k in val_dict}, val_dict)
            else:
                ev = DraftChangeEvent(type_dict, val_dict, {k: None for k in val_dict})
            if handler.user_eval_vars:
                # user can define custom evaluates to get new model value.
                user_vars = {}
                for k in handler.user_eval_vars.keys():
                    obj = handler.evaluate_user_eval_var_noexcept(k, self.model)
                    user_vars[k] = obj
                ev.user_eval_vars = user_vars

            with prevent_draft_update():
                await self.run_callback(partial(handler.handler, ev),
                                        change_status=False,
                                        capture_draft=False)

    async def _draft_change_handler_effect(self, paths: tuple[str, ...],
                                     handler: DraftChangeEventHandler):
        if paths not in self._draft_change_event_handlers:
            self._draft_change_event_handlers[paths] = {}
        self._draft_change_event_handlers[paths][handler.handler] = handler
        await self._run_draft_effect_handler(handler, True)
        # we have to run handler during UI mount/unmount (backend) with reversed data -> None because
        # uncontrolled components usually require draft event change to set
        # their UI value. 
        async def unmount():
            await self._run_draft_effect_handler(handler, False)
            self._draft_change_event_handlers[paths].pop(handler.handler)

        return unmount

    def install_draft_change_handler(
            self,
            draft: Union[Any, dict[str, Any]],
            handler: Callable[[DraftChangeEvent], _CORO_NONE],
            equality_fn: Optional[Callable[[Any, Any], bool]] = None,
            handle_child_change: bool = False,
            installed_comp: Optional[Component] = None,
            user_eval_vars: Optional[dict[str, Any]] = None):
        if not isinstance(draft, dict):
            draft = {"": draft}
        paths: list[str] = []
        draft_expr_dict: dict[str, DraftASTNode] = {}
        for k, v in draft.items():
            assert isinstance(v, DraftBase)
            node = get_draft_ast_node(v)
            path = node.get_jmes_path()
            paths.append(path)
            draft_expr_dict[k] = node
        user_eval_vars_dict: Optional[dict[str, DraftASTNode]] = None
        if user_eval_vars is not None:
            user_eval_vars_dict = {}
            for k, v in user_eval_vars.items():
                assert isinstance(v, DraftBase)
                user_eval_vars_dict[k] = get_draft_ast_node(v)
        handler_obj = DraftChangeEventHandler(draft_expr_dict, handler, equality_fn,
                                              handle_child_change,
                                              user_eval_vars=user_eval_vars_dict)
        effect_fn = partial(self._draft_change_handler_effect, tuple(paths),
                            handler_obj)
        if installed_comp is not None:
            installed_comp.use_effect(effect_fn)
        else:
            self.use_effect(effect_fn)
        # return effect_fn to let user remove the effect.
        return handler_obj, effect_fn

    def debug_print_draft_change(self, draft: Union[Any, dict[str, Any]]):
        if not isinstance(draft, dict):
            draft = {"": draft}
        draft_expr_str_dict = {k: get_draft_ast_node(v).get_jmes_path() for k, v in draft.items()}
        return self.install_draft_change_handler(draft, partial(_print_draft_change_event, draft_expr_str_dict=draft_expr_str_dict))

    def _lazy_get_mashumaro_coder(self):
        if self._mashumaro_decoder is None:
            self._mashumaro_decoder = BasicDecoder(type(self.model))
        if self._mashumaro_encoder is None:
            self._mashumaro_encoder = BasicEncoder(type(self.model))
        return self._mashumaro_decoder, self._mashumaro_encoder

    @property
    def model(self) -> _T:
        return self._model

    def get_model(self):
        """this func is used as a getter function for model, model instance
        may changed, so user shouldn't keep model instance.
        """
        return self._model

    @property
    def prop(self):
        propcls = self.propcls
        return self._prop_base(propcls, self)

    @property
    def update_event(self):
        propcls = self.propcls
        return self._update_props_base(propcls, exclude_field_ids=self._flow_exclude_field_ids)

    async def sync_model(self):
        await self.send_and_wait(self.update_event(dataObject=self.model))

    def get_draft_from_object(self) -> _T:
        """Create draft object, the generated draft AST is depend on real object.
        All opeartion you appied to draft object must be valid for real object.

        This mode should only be used on data without type.
        """
        return cast(_T, create_draft(self.model,
                                     userdata=DraftOpUserData(self),
                                     obj_type=self._model_type))

    def get_draft(self):
        """Create draft object, but the generated draft AST is depend on annotation type instead of real object.
        useful when your draft ast contains optional/undefined path, this kind of path produce undefined in frontend,
        but raise error if we use real object.

        We also enable method support in this mode, which isn't allowed in object mode.
        """
        return self.get_draft_type_only()

    def get_draft_type_only(self) -> _T:
        return cast(
            _T,
            create_draft_type_only(obj_type=self._model_type,
                                   userdata=DraftOpUserData(self)))

    async def _update_with_jmes_ops_backend(self, ops: list[DraftUpdateOp]):
        # convert dynamic node to static in op to avoid where op.
        ops = ops.copy()
        for i in range(len(ops)):
            op = ops[i]
            if op.has_dynamic_node_in_main_path():
                ops[i] = stabilize_getitem_path_in_op_main_path(
                    op, self.get_draft_type_only(), self._model)
        if not self._draft_change_event_handlers:
            apply_draft_update_ops(self.model, ops)
        else:
            all_disabled_ev_handlers: set[Callable] = set()
            for op in ops:
                userdata = op.get_userdata_typed(DraftOpUserData)
                if userdata is not None:
                    all_disabled_ev_handlers.update(userdata.disabled_handlers)
            all_ev_handlers: list[DraftChangeEventHandler] = []
            for path, handlers in self._draft_change_event_handlers.items():
                for handler in handlers.values():
                    if handler.handler not in all_disabled_ev_handlers:
                        all_ev_handlers.append(handler)
            event_handler_changes = update_model_with_change_event(
                self.model, ops, all_ev_handlers)
            cbs: list[Callable[[], _CORO_NONE]] = []
            for draft_change_ev, handler in zip(event_handler_changes, all_ev_handlers):
                if draft_change_ev.is_changed:
                    if handler.user_eval_vars:
                        # user can define custom evaluates to get new model value.
                        user_vars = {}
                        for k in handler.user_eval_vars.keys():
                            obj = handler.evaluate_user_eval_var_noexcept(k, self.model)
                            user_vars[k] = obj
                        draft_change_ev.user_eval_vars = user_vars
                    cbs.append(partial(handler.handler, draft_change_ev))
            # draft ops isn't allowed in draft event handler.
            with prevent_draft_update():
                await self.run_callbacks(cbs,
                                        change_status=False,
                                        capture_draft=False)
        return ops

    async def write_whole_model(self, new_model: _T):
        assert type(new_model) == type(self._model)
        self._model = new_model
        if self._store is not None:
            await self._store.write_whole_model(new_model)
        await self.sync_model()

    async def _update_with_jmes_ops_event(self, ops: list[DraftUpdateOp]):
        # convert dynamic node to static in op to avoid where op.
        ops = await self._update_with_jmes_ops_backend(ops)
        # any modify on external field won't be included in frontend.
        frontend_ops = list(filter(lambda op: not op.is_external, ops))
        # any external field data will be omitted in opData.
        if self._flow_exclude_field_ids:
            facto_fn = partial(_dict_facto_with_exclude, 
                            exclude_field_ids=self._flow_exclude_field_ids)
            for op in frontend_ops:
                opData = asdict_no_deepcopy_with_field(
                            _DataclassSer(obj=op.opData),
                            dict_factory_with_field=facto_fn)
                op.opData = cast(dict, opData)["obj"]
        frontend_ops = [op.to_jmes_path_op().to_dict() for op in frontend_ops]
        if frontend_ops:
            return self.create_comp_event({
                "type": 0,
                "ops": frontend_ops,
            })
        else:
            return None 

    async def _update_with_jmes_ops(self, ops: list[DraftUpdateOp]):
        if ops:
            async with self._lock:
                await self.flow_event_emitter.emit_async(
                    self._backend_draft_update_event_key,
                    Event(self._backend_draft_update_event_key, ops))
                ev_or_none = await self._update_with_jmes_ops_event(ops)
                if ev_or_none is not None:
                    return await self.send_and_wait(ev_or_none)

    async def _internal_update_with_jmes_ops_event(
            self, ops: list[DraftUpdateOp]):
        # internal event handle system will call this function
        if ops:
            async with self._lock:
                await self.flow_event_emitter.emit_async(
                    self._backend_draft_update_event_key,
                    Event(self._backend_draft_update_event_key, ops))
                return await self._update_with_jmes_ops_event(ops)
        return None 

    @override
    def bind_fields_unchecked(
        self, **kwargs: Union[str, tuple["Component", Union[str, DraftBase]],
                              DraftBase]
    ) -> Self:
        raise NotImplementedError("you can't bind fields on DataModel")

    @contextlib.asynccontextmanager
    async def draft_update(self):
        """Do draft update immediately after this context.
        We won't perform real update during draft operation because we need to keep state same between
        frontend and backend. if your update code raise error during draft operation, the real model in backend won't 
        be updated, so the state is still same. if we do backend update in each draft update, the state
        will be different between frontend and backend when exception happen.

        If your code after draft depends on the updated model, you can use this ctx to perform
        update immediately.

        WARNING: draft change event handler will be called (if change) in each draft update.
        """
        draft = self.get_draft()
        cur_ctx = get_draft_update_context_noexcept()
        if cur_ctx is not None and cur_ctx._prevent_inner_draft:
            raise RuntimeError("Draft operation is disabled by a prevent_draft_update context, usually exists in draft event handler.")
        with capture_draft_update() as ctx:
            yield draft
        await self._update_with_jmes_ops(ctx._ops)

    @staticmethod
    def get_draft_external(model: T) -> T:
        return cast(T, create_draft(model, userdata=None))

    def connect_draft_store(self,
                            path: str,
                            backend_map: Union[DraftStoreBackendBase, Mapping[str, DraftStoreBackendBase]]):
        """Register event handler that store and send update info to your backend.

        **WARNING**: this function must be called before mount.
        """
        assert self._is_model_dataclass, "only support dataclass model when use storage"
        assert not self.is_mounted(), "you should call this function when unmounted."
        assert not self._draft_store_handler_registered, "only support connect once. if you want to change path/type, create a new component."
        model = self.model
        assert dataclasses.is_dataclass(
            model), "only support dataclass model"
        self._store = DraftFileStorage(path, model, backend_map) # type: ignore
        self.event_after_mount.on(
            partial(self._fetch_internal_data_from_draft_store,
                    store=self._store))
        self.event_draft_update.on(
            partial(self._handle_draft_store_update,
                    store=self._store))
        self.event_before_unmount.on(
            partial(self._clear_draft_store_status))

        self._draft_store_handler_registered = True

    def _clear_draft_store_status(self):
        self._draft_store_data_fetched = False

    async def _fetch_internal_data_from_draft_store(self, store: DraftFileStorage):
        assert dataclasses.is_dataclass(
            self.model), "only support dataclass model"
        prev_model = self._model
        self._model = await store.fetch_model()
        self.props.dataObject = self._model
        # user should init their external fields in this event.
        # TODO should we capture draft here?
        await self.flow_event_emitter.emit_async(
            self._backend_storage_fetched_event_key,
            Event(self._backend_storage_fetched_event_key, prev_model))
        # finally sync the model.
        await self.sync_model()
        await self._run_all_draft_change_handlers_when_init()
        self._draft_store_data_fetched = True

    async def _handle_draft_store_update(self, ops: list[DraftUpdateOp],
                                         store: DraftFileStorage):
        # external fields won't be included in backend store.
        ops = list(filter(lambda op: not op.is_external and not op.is_store_external, ops))
        await store.update_model(self.get_draft(), ops)

    @staticmethod
    def _op_proc(op: DraftUpdateOp, handlers: list[DraftChangeEventHandler]):
        userdata = op.get_userdata_typed(DraftOpUserData)
        if userdata is None:
            return op
        # disable specific handler in draft update op, we must use dataclasses.replace
        # to make sure userdata in draft expr isn't changed.
        op.userdata = dataclasses.replace(userdata, disabled_handlers=userdata.disabled_handlers + [h.handler for h in handlers])
        return op

    @staticmethod
    @contextlib.contextmanager
    def add_disabled_handler_ctx(handlers: list[DraftChangeEventHandler]):
        """Disable specific draft change event handler for current draft update context.
        Usually used when you use a uncontrolled component (e.g. Monaco Editor). When you
        bind a data model draft change for editor, you will set editor value manually 
        (unlike controlled bind) when some data model prop change. If you save the editor from
        frontend, since we already modify the frontend editor value, we shouldn't trigger 
        draft change handler to set editor value manually again.

        don't need to use this with controlled component.
        """
        with enter_op_process_ctx(
                partial(DataModel._op_proc, handlers=handlers)):
            yield


@dataclasses.dataclass
class DataPortalProps(ContainerBaseProps):
    comps: list[Component] = dataclasses.field(default_factory=list)
    query: Union[Undefined, str] = undefined


class DataPortal(ContainerBase[DataPortalProps, Component]):
    """DataPortal is used to forward multiple container that isn't direct parent.
    can only be used with DataModel and resource loaders.
    """

    def __init__(
        self,
        sources: list[Component],
        children: Optional[Union[Sequence[Component],
                                 Mapping[str, Component]]] = None
    ) -> None:
        if children is not None and isinstance(children, Sequence):
            children = {str(i): v for i, v in enumerate(children)}
        allowed_comp_types = {
            UIType.DataModel, UIType.ThreeURILoaderContext,
            UIType.ThreeCubeCamera
        }
        for comp in sources:
            assert comp._flow_comp_type in allowed_comp_types, "DataPortal only support DataModel and resource loaders."
        assert len(sources) > 0, "DataPortal must have at least one source"
        super().__init__(UIType.DataPortal,
                         DataPortalProps,
                         children,
                         allowed_events=[])
        self.prop(comps=sources)

    @property
    def prop(self):
        propcls = self.propcls
        return self._prop_base(propcls, self)

    @property
    def update_event(self):
        propcls = self.propcls
        return self._update_props_base(propcls)

    def bind_fields_unchecked(
        self, **kwargs: Union[str, tuple["Component", Union[str, DraftBase]],
                              DraftBase]
    ) -> Self:
        if "comps" not in kwargs and "query" not in kwargs:
            return super().bind_fields_unchecked(**kwargs)
        raise NotImplementedError(
            "you can't bind `comps` and `query` on DataModel")


@dataclasses.dataclass
class DataSubQueryProps(ContainerBaseProps):
    query: Union[Undefined, str] = undefined
    enable: Union[Undefined, bool] = undefined

    @field_validator('query')
    def jmes_query_validator(cls, v: Union[str, Undefined]):
        assert isinstance(v, str), "query must be string"
        # compile test
        jmespath.compile(v)


class DataSubQuery(ContainerBase[DataSubQueryProps, Component]):

    def __init__(
        self,
        query: str,
        children: Optional[Union[Sequence[Component],
                                 Mapping[str, Component]]] = None
    ) -> None:
        # compile test
        jmespath.compile(query)
        if children is not None and isinstance(children, Sequence):
            children = {str(i): v for i, v in enumerate(children)}
        super().__init__(UIType.DataSubQuery,
                         DataSubQueryProps,
                         children,
                         allowed_events=[])
        self.prop(query=query)

    @property
    def prop(self):
        propcls = self.propcls
        return self._prop_base(propcls, self)

    @property
    def update_event(self):
        propcls = self.propcls
        return self._update_props_base(propcls)

    def bind_fields_unchecked(
        self, **kwargs: Union[str, tuple["Component", Union[str, DraftBase]],
                              DraftBase]
    ) -> Self:
        if "query" not in kwargs:
            return super().bind_fields_unchecked(**kwargs)
        raise NotImplementedError(
            "you can't bind `comps` and `query` on DataModel")
