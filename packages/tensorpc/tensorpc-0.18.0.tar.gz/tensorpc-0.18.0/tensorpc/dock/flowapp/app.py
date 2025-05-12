# Copyright 2024 Yan Yan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Flow APP: simple GUI application in devflow
Reload System

Layout Instance: App itself and layout objects created on AnyFlexLayout.
"""
import ast
import asyncio
import base64
from typing import Mapping, Sequence, cast
import contextlib
import contextvars
import dataclasses
import enum
import importlib
import importlib.machinery
import inspect
import io
import json
import pickle
import runpy
import sys
import threading
import time
import tokenize
import traceback
import types
from functools import partial
from pathlib import Path
from types import ModuleType
from typing import (Any, AsyncGenerator, Awaitable, Callable, Coroutine, Dict,
                    Iterable, List, Optional, Set, Tuple, Type, TypeVar, Union)

import numpy as np
import watchdog
import watchdog.events
from typing_extensions import ParamSpec
from watchdog.observers import Observer
from watchdog.observers.api import ObservedWatch
from tensorpc.core import dataclass_dispatch

from tensorpc import compat, simple_chunk_call_async
from tensorpc.autossh.coretypes import SSHTarget
from tensorpc.constants import PACKAGE_ROOT, TENSORPC_FILE_NAME_PREFIX, TENSORPC_FLOW_FUNC_META_KEY, TENSORPC_OBSERVED_FUNCTION_ATTR
from tensorpc.core.astex.astcache import AstCache
from tensorpc.core.asynctools import cancel_task
from tensorpc.core.defs import FileDesc, FileResource, FileResourceRequest
from tensorpc.core.event_emitter.call_server import SimpleRPCHandler
from tensorpc.core.funcid import remove_common_indent_from_code
from tensorpc.core.inspecttools import get_all_members_by_type
from tensorpc.core.moduleid import (get_qualname_of_type, is_lambda,
                                    is_tensorpc_dynamic_path,
                                    is_valid_function, loose_isinstance)
from tensorpc.core.rprint_dispatch import rprint
from tensorpc.core.serviceunit import (ObjectReloadManager,
                                       ObservedFunctionRegistryProtocol,
                                       ReloadableDynamicClass,
                                       ServFunctionMeta, ServiceUnit,
                                       SimpleCodeManager, get_qualname_to_code)
from tensorpc.core.tracers.codefragtracer import get_trace_infos_from_coderange_item
from tensorpc.dock.client import MasterMeta
from tensorpc.dock.constants import TENSORPC_APP_DND_SRC_KEY, TENSORPC_APP_ROOT_COMP, TENSORPC_APP_STORAGE_VSCODE_TRACE_PATH, TENSORPC_FLOW_COMP_UID_TEMPLATE_SPLIT, TENSORPC_FLOW_EFFECTS_OBSERVE
from tensorpc.core.tree_id import UniqueTreeId, UniqueTreeIdForComp, UniqueTreeIdForTree
from tensorpc.dock.flowapp.appstorage import AppStorage
from tensorpc.utils.wait_tools import debounce
from ..components import mui, three
from tensorpc.dock.coretypes import ScheduleEvent, StorageDataItem
from tensorpc.dock.vscode.coretypes import VscodeBreakpoint, VscodeTensorpcMessage, VscodeTensorpcQuery, VscodeTensorpcQueryType, VscodeTraceItem, VscodeTraceQueries, VscodeTraceQuery, VscodeTraceQueryResult
from tensorpc.dock.components.plus.objinspect.inspector import get_exception_frame_stack
from tensorpc.dock.components.plus.objinspect.treeitems import TraceTreeItem
from tensorpc.dock.core.reload import (AppReloadManager,
                                          bind_and_reset_object_methods,
                                          reload_object_methods)
from tensorpc.dock.jsonlike import JsonLikeNode, as_dict_no_undefined, parse_obj_to_jsonlike
from tensorpc.dock.langserv.pyrightcfg import LanguageServerConfig
from tensorpc.dock.marker import AppFunctionMeta, AppFuncType
from tensorpc.dock.serv_names import serv_names
from tensorpc.utils.registry import HashableRegistry
from tensorpc.utils.reload import reload_method
from tensorpc.utils.uniquename import UniqueNamePool
from tensorpc.dock.vscode.storage import AppDataStorageForVscode, AppVscodeState
from ..core.appcore import (ALL_OBSERVED_FUNCTIONS, AppContext, AppSpecialEventType,
                      _CompReloadMeta, RemoteCompEvent, Event, EventHandlingContext, create_reload_metas, enter_event_handling_conetxt)
from ..core.appcore import enter_app_context
from ..core.appcore import enter_app_context as _enter_app_conetxt
from ..core.appcore import get_app, get_app_context
from ..components import plus
from tensorpc.core.tracers.tracer import FrameResult, Tracer, TraceEventType
from ..core.component import (AppComponentCore, AppEditorEvent, AppEditorEventType,
                   AppEditorFrontendEvent, AppEditorFrontendEventType,
                   AppEvent, AppEventType, BasicProps, Component,
                   ContainerBase, CopyToClipboardEvent, EventHandler,
                   FlowSpecialMethods, ForEachResult, FrontendEventType,
                   LayoutEvent, RemoteComponentBase, TaskLoopEvent, UIEvent, UIExceptionEvent,
                   UIRunStatus, UIType, UIUpdateEvent, Undefined, UserMessage,
                   ValueType, component_dict_to_serializable_dict_async, undefined)
from tensorpc.core.event_emitter.aio import AsyncIOEventEmitter

ALL_APP_EVENTS = HashableRegistry()
P = ParamSpec('P')

T = TypeVar('T')

T_comp = TypeVar("T_comp")

_ROOT = TENSORPC_APP_ROOT_COMP

class AppEditor:

    def __init__(self, init_value: str, language: str,
                 queue: "asyncio.Queue[AppEvent]") -> None:
        self._language = language
        self._value: str = init_value
        self.__freeze_language = False
        self._init_line_number = 1
        self._monaco_state: Optional[Any] = None
        self._queue = queue

        # for object inspector only
        # TODO better way to implement
        self.external_path: Optional[str] = None

    def set_init_line_number(self, val: int):
        self._init_line_number = val

    def freeze(self):
        self.__freeze_language = True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: str):
        self._value = val

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, val: str):
        if not self.__freeze_language:
            self._language = val
        else:
            raise ValueError("language freezed, you can't change it.")

    def get_state(self):
        state = {}
        state["language"] = self._language
        state["value"] = self._value
        state["monacoEditorState"] = self._monaco_state
        state["initLineNumber"] = self._init_line_number
        return state

    async def _send_editor_event(self, event: AppEditorEvent):
        await self._queue.put(AppEvent("", {AppEventType.AppEditor: event}))

    async def set_editor_value(self, value: str, language: str = ""):
        """use this method to set editor value and language.
        """
        self.value = value
        if language:
            self.language = language
        app_ev = AppEditorEvent(AppEditorEventType.SetValue, {
            "value": self.value,
            "language": self.language,
        })
        await self._send_editor_event(app_ev)


T = TypeVar("T")


@dataclasses.dataclass
class _LayoutObserveMeta:
    # one type (base class) may related to multiple layouts
    layouts: Dict[Union[mui.FlexBox, "App"],
                  Optional[Callable[[mui.FlexBox, ServFunctionMeta],
                                    Coroutine[None, None,
                                              Optional[mui.FlexBox]]]]]
    qualname_prefix: str
    # if type is None, it means they are defined in global scope.
    type: Type
    is_leaf: bool
    metas: List[ServFunctionMeta]
    # callback: Optional[Callable[[mui.FlexBox, ServFunctionMeta],
    #                             Coroutine[None, None, Optional[mui.FlexBox]]]]


@dataclasses.dataclass
class _WatchDogWatchEntry:
    obmetas: Dict[ObjectReloadManager.TypeUID, _LayoutObserveMeta]
    watch: Optional[ObservedWatch]


class _FlowAppObserveContext:

    def __init__(self) -> None:
        self._removed_layouts: List[mui.FlexBox] = []
        self._added_layouts_and_cbs: Dict[mui.FlexBox, Optional[Callable[
            [mui.FlexBox, ServFunctionMeta], Coroutine]]] = {}
        self._reloaded_layout_pairs: List[Tuple[mui.FlexBox, mui.FlexBox]] = []


_FLOWAPP_OBSERVE_CONTEXT: contextvars.ContextVar[
    Optional[_FlowAppObserveContext]] = contextvars.ContextVar(
        "_FLOWAPP_OBSERVE_CONTEXT", default=None)


def _get_flowapp_observe_context():
    return _FLOWAPP_OBSERVE_CONTEXT.get()


@contextlib.contextmanager
def _enter_flowapp_observe_context(ctx: _FlowAppObserveContext):
    token = _FLOWAPP_OBSERVE_CONTEXT.set(ctx)
    try:
        yield ctx
    finally:
        _FLOWAPP_OBSERVE_CONTEXT.reset(token)

def _component_rpc_runner(args_kwargs: Tuple[tuple, Dict[str, Any]], fn: Callable):
    return fn(*args_kwargs[0], **args_kwargs[1])

class App:
    """
    App Init Callbacks:
    1. app init/app init async
    2. set_persist_props_async for all comps
    """

    def __init__(self,
                 flex_flow: Union[str, Undefined] = "column nowrap",
                 maxqsize: int = 10,
                 enable_value_cache: bool = False,
                 external_root: Optional[mui.FlexBox] = None,
                 external_wrapped_obj: Optional[Any] = None,
                 reload_manager: Optional[AppReloadManager] = None,
                 is_remote_component: bool = False) -> None:
        # self._uid_to_comp: Dict[str, Component] = {}
        self._queue: "asyncio.Queue[AppEvent]" = asyncio.Queue(
            maxsize=maxqsize)
        if reload_manager is None:
            reload_manager = AppReloadManager(ALL_OBSERVED_FUNCTIONS)
        # self._flow_reload_manager = reload_manager
        self._is_remote_component = is_remote_component
        self._flow_app_comp_core = AppComponentCore(self._queue,
                                                    reload_manager)
        self._send_callback: Optional[Callable[[AppEvent],
                                               Coroutine[None, None,
                                                         None]]] = None
        self._is_external_root = False
        self._use_app_editor = False
        # self.__flowapp_external_wrapped_obj = external_wrapped_obj
        root_uid = UniqueTreeIdForComp.from_parts([_ROOT])

        if external_root is not None:
            # TODO better mount
            root = external_root
            external_root._flow_uid = root_uid
            # if root._children is not None:
            #     # consume this _children
            #     root.add_layout(root._children)
            #     root._children = None
            # layout saved in external_root
            # self._uid_to_comp = root._uid_to_comp
            root._attach(root_uid, self._flow_app_comp_core)

            self._is_external_root = True
        else:
            root = mui.FlexBox(uid=root_uid,
                               app_comp_core=self._flow_app_comp_core)
            root.prop(flexFlow=flex_flow)
            if external_wrapped_obj is not None:
                root._wrapped_obj = external_wrapped_obj
                self._is_external_root = True

        # self._uid_to_comp[_ROOT] = root
        self.root = root.prop(minHeight=0, minWidth=0)
        self._enable_editor = False
        self._dialog_z_index: Optional[int] = None
        self._flowapp_special_eemitter: AsyncIOEventEmitter[
            AppSpecialEventType, Any] = AsyncIOEventEmitter()
        self._flowapp_component_rpc_eemitter: AsyncIOEventEmitter[
            str, RemoteCompEvent] = AsyncIOEventEmitter()
        self._flowapp_thread_id = threading.get_ident()
        self._flowapp_enable_exception_inspect: bool = False

        self.code_editor = AppEditor("", "python", self._queue)
        self._app_dynamic_cls: Optional[ReloadableDynamicClass] = None
        # other app can call app methods via service_unit
        self._app_service_unit: Optional[ServiceUnit] = None
        self._flowapp_vscode_workspace_root: Optional[str] = None 
        # loaded if you connect app node with a full data storage
        self._data_storage: Dict[str, Any] = {}

        self._force_special_layout_method = False

        self.__persist_storage: Dict[str, Any] = {}

        self.__previous_error_sync_props = {}
        self.__previous_error_persist_state = {}
        self._enable_value_cache = enable_value_cache
        self._flow_app_is_headless = False

        self.__flowapp_master_meta = MasterMeta()
        # self.__flowapp_storage_cache: Dict[str, StorageDataItem] = {}
        self.app_storage = AppStorage(self.__flowapp_master_meta, is_remote_component)
        # for app and dynamic layout in AnyFlexLayout
        self._flowapp_change_observers: Dict[str, _WatchDogWatchEntry] = {}
        self._flowapp_vscode_storage: Optional[AppDataStorageForVscode] = None
        self._flowapp_vscode_state = AppVscodeState()
        self._flowapp_is_inited: bool = False
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._flowapp_enable_lsp: bool = False
        self._flowapp_internal_lsp_config: LanguageServerConfig = LanguageServerConfig(
        )
        self._flowapp_internal_lsp_config.python.analysis.pythonPath = sys.executable
        self._flowapp_observed_func_registry: Optional[
            ObservedFunctionRegistryProtocol] = None
        self._flowapp_file_resource_handlers: SimpleRPCHandler[Callable[[FileResourceRequest], Union[FileResource, Coroutine[None, None, FileResource]]]] = SimpleRPCHandler()
        self._flowapp_simple_rpc_handlers: SimpleRPCHandler = SimpleRPCHandler()

    @property
    def _flow_reload_manager(self):
        return self._flow_app_comp_core.reload_mgr

    def add_file_resource(
        self, key: str,
        handler: Callable[[FileResourceRequest], Union[FileResource, Coroutine[None, None, FileResource]]]):
        self._flowapp_file_resource_handlers.on(key, handler)

    def remove_file_resource(
        self,
        key: str,
    ):
        self._flowapp_file_resource_handlers.off(key)

    def set_enable_language_server(self, enable: bool):
        """must be setted before app init (in layout function), only valid
        in app init. layout reload won't change this setting
        """
        self._flowapp_enable_lsp = enable

    def get_language_server_settings(self):
        """must be setted before app init (in layout function), only valid
        in app init. layout reload won't change this setting
        """
        return self._flowapp_internal_lsp_config

    async def get_vscode_storage_lazy(self):
        if self._flowapp_vscode_storage is None:
            data = await self.app_storage.read_data_storage(TENSORPC_APP_STORAGE_VSCODE_TRACE_PATH, raise_if_not_found=False)
            if data is not None:
                self._flowapp_vscode_storage = AppDataStorageForVscode(**data)
            else:
                self._flowapp_vscode_storage = AppDataStorageForVscode(trace_trees={})
        return self._flowapp_vscode_storage

    def get_vscode_state(self):
        return self._flowapp_vscode_state

    def set_observed_func_registry(self,
                                   registry: ObservedFunctionRegistryProtocol):
        self._flowapp_observed_func_registry = registry
        self._flow_reload_manager.update_observed_registry(registry)

    def set_vscode_workspace_root(self, root: str):
        self._flowapp_vscode_workspace_root = root

    def _is_app_workspace_child_of_vscode_workspace_root(self, vscode_root: str):
        # if app workspace root is child of vscode workspace root or
        # equal to vscode workspace root, return True
        # used to filter all vscode query.
        app_root_path = self._flowapp_vscode_workspace_root
        if app_root_path is None and self._app_service_unit is not None:
            app_root_path = self._app_service_unit.file_path 
            if app_root_path == "":
                return False 
            try:
                Path(app_root_path).relative_to(vscode_root)
            except ValueError:
                return False
            return True 
        return False 

    def register_app_simple_rpc_handler(self, type: str,
                                           handler: Callable[[Any],
                                                             mui._CORO_NONE]):
        assert isinstance(type, AppSpecialEventType)
        self._flowapp_simple_rpc_handlers.on(type, handler)

    def unregister_app_simple_rpc_handler(self, type: str):
        self._flowapp_simple_rpc_handlers.off(type)

    def register_app_special_event_handler(self, type: AppSpecialEventType,
                                           handler: Callable[[Any],
                                                             mui._CORO_NONE]):
        assert isinstance(type, AppSpecialEventType)
        self._flowapp_special_eemitter.on(type, handler)

    def unregister_app_special_event_handler(
            self, type: AppSpecialEventType,
            handler: Callable[[Any], mui._CORO_NONE]):
        assert isinstance(type, AppSpecialEventType)
        self._flowapp_special_eemitter.remove_listener(type, handler)

    def unregister_app_special_event_handlers(self, type: AppSpecialEventType):
        assert isinstance(type, AppSpecialEventType)
        self._flowapp_special_eemitter.remove_all_listeners(type)

    def _get_user_app_object(self):
        if self._is_external_root:
            if self.root._wrapped_obj is not None:
                return self.root._wrapped_obj
            return self.root
        else:
            return self

    def _is_wrapped_obj(self):
        return self._is_external_root and self.root._wrapped_obj is not None

    async def get_ssh_node_data(self, node_id: str):
        meta = self.__flowapp_master_meta
        assert self.__flowapp_master_meta.is_inside_devflow, "you must call this in devflow apps."
        res: SSHTarget = await simple_chunk_call_async(
            meta.grpc_url, serv_names.FLOW_GET_SSH_NODE_DATA, meta.graph_id,
            node_id)
        return res

    def get_persist_storage(self):
        return self.__persist_storage

    def get_observed_func_registry(self):
        registry = self._flowapp_observed_func_registry
        if registry is None:
            registry = ALL_OBSERVED_FUNCTIONS
        return registry

    def _get_simple_app_state(self):
        """get state of Input/Switch/Radio/Slider/Select
        """
        state: Dict[str, Any] = {}
        user_state: Dict[str, Any] = {}

        for comp in self.root._get_all_nested_childs():
            # automatic simple state store
            if isinstance(comp, (
                    mui.Input,
                    mui.Switch,
                    mui.RadioGroup,
                    mui.Slider,
                    mui.Select,
                    mui.MultipleSelect,
            )):
                state[comp._flow_uid_encoded] = {
                    "type": comp._flow_comp_type.value,
                    "props": comp.get_sync_props(),
                }
            # user state
            st = comp.get_persist_props()
            if st is not None:
                user_state[comp._flow_uid_encoded] = {
                    "type": comp._flow_comp_type.value,
                    "state": st,
                }
        # print("persist_storage_SAVE", self.__persist_storage, id(self.__persist_storage))
        return {
            "persist_storage": self.__persist_storage,
            "uistate": state,
            "userstate": user_state,
        }

    async def _restore_simple_app_state(self, state: Dict[str, Any]):
        """try to restore state of Input/Switch/Radio/Slider/Select
        no exception if fail.
        """
        uistate = state["uistate"]
        userstate = state["userstate"]
        # print("persist_storage", state["persist_storage"])
        if state["persist_storage"]:
            self.__persist_storage.update(state["persist_storage"])
        uid_to_comp = self.root._get_uid_encoded_to_comp_dict()
        if self._enable_value_cache:
            ev = AppEvent("", {})
            for k, s in uistate.items():
                if k in uid_to_comp:
                    comp_to_restore = uid_to_comp[k]
                    if comp_to_restore._flow_comp_type.value == s["type"]:
                        comp_to_restore.set_props(s["props"])
                        ev += comp_to_restore.get_sync_event(True)
            with _enter_app_conetxt(self):
                for k, s in userstate.items():
                    if k in uid_to_comp:
                        comp_to_restore = uid_to_comp[k]
                        if comp_to_restore._flow_comp_type.value == s["type"]:
                            try:
                                await comp_to_restore.set_persist_props_async(
                                    s["state"])
                            except:
                                traceback.print_exc()
                                continue
            await self._queue.put(ev)

    def _app_force_use_layout_function(self):
        self._force_special_layout_method = True
        self.root._prevent_add_layout = True

    async def _app_run_layout_function(
        self,
        send_layout_ev: bool = False,
        with_code_editor: bool = True,
        reload: bool = False,
        decorator_fn: Optional[Callable[[], Union[mui.LayoutType,
                                                  mui.FlexBox]]] = None):
        self.root._prevent_add_layout = False
        prev_comps = self.__previous_error_sync_props.copy()
        prev_user_states = self.__previous_error_persist_state.copy()
        uid_to_comp = self.root._get_uid_encoded_to_comp_dict()
        if reload:
            for u, c in uid_to_comp.items():
                prev_comps[u] = c._to_dict_with_sync_props()
                user_state = c.get_persist_props()
                if user_state is not None:
                    prev_user_states[u] = {
                        "type": c._flow_comp_type.value,
                        "state": user_state,
                    }
        if reload:
            detached = self.root._prepare_detach_child()
            # make sure will_unmount is called from leaf to root (reverse breadth first order)
            detached_items = list(detached.items())
            detached_items.sort(key=lambda x: len(x[0].parts), reverse=True)

            await self.root._run_special_methods(
                [], {x[0] : x[1] for x in detached_items}, self._flow_reload_manager)
            for v in detached.values():
                v._finish_detach()
            del detached
        root_uid = UniqueTreeIdForComp.from_parts([_ROOT])

        await self.root._clear()
        # self._uid_to_comp.clear()
        self.root._flow_uid = root_uid
        new_is_flex = False
        res: mui.LayoutType = {}
        wrapped_obj = self.root._wrapped_obj
        attached: Dict[UniqueTreeIdForComp, Component] = {}
        try:
            with _enter_app_conetxt(self):
                if decorator_fn is not None:
                    temp_res = decorator_fn()
                    if isinstance(temp_res, mui.FlexBox):
                        # if temp_res._children is not None:
                        #     # consume this _children
                        #     temp_res.add_layout(temp_res._children)
                        #     temp_res._children = None
                        # temp_res._flow_uid = _ROOT
                        attached = temp_res._attach(root_uid,
                                                    self._flow_app_comp_core)
                        # self._uid_to_comp = temp_res._uid_to_comp
                        new_is_flex = True
                        self.root = temp_res
                        self.root._wrapped_obj = wrapped_obj
                    else:
                        res = temp_res
                else:
                    res = self.app_create_layout()
            self.__previous_error_sync_props.clear()
            self.__previous_error_persist_state.clear()
        except BaseException as e:
            # TODO store
            traceback.print_exc()
            ss = io.StringIO()
            traceback.print_exc(file=ss)
            user_exc = UserMessage.create_error("", str(e), ss.getvalue())
            ev = UIExceptionEvent([user_exc])
            fbm = (
                "app_create_layout failed!!! check your app_create_layout. if "
                "you are using reloadable app, just check and save your app code!"
            )
            await self._queue.put(
                AppEvent(
                    "", {
                        AppEventType.UIException:
                        ev,
                        AppEventType.UpdateLayout:
                        LayoutEvent(
                            self._get_fallback_layout(fbm, with_code_editor))
                    }))
            return
        if not new_is_flex:
            if isinstance(res, Sequence):
                res = {str(i): v for i, v in enumerate(res)}
            res_anno: Mapping[str, Component] = {**res}
            self.root.add_layout(res_anno)
            attached = self.root._attach(root_uid, self._flow_app_comp_core)
        uid_to_comp = self.root._get_uid_encoded_to_comp_dict()
        # self._uid_to_comp[_ROOT] = self.root
        self.root._prevent_add_layout = True
        if reload:
            # comps = self.root._get_all_nested_childs()
            with _enter_app_conetxt(self):
                for comp in uid_to_comp.values():
                    if comp._flow_uid_encoded in prev_comps:
                        if comp._flow_comp_type.value == prev_comps[
                                comp._flow_uid_encoded]["type"]:
                            comp.set_props(
                                prev_comps[comp._flow_uid_encoded]["props"])
                    if comp._flow_uid_encoded in prev_user_states:
                        if comp._flow_comp_type.value == prev_user_states[
                                comp._flow_uid_encoded]["type"]:
                            await comp.set_persist_props_async(
                                prev_user_states[
                                    comp._flow_uid_encoded]["state"])
            del prev_comps
            del prev_user_states

        if send_layout_ev:
            layout = await self._get_app_layout(with_code_editor)
            ev = AppEvent(
                "", {
                    AppEventType.UpdateLayout:
                    LayoutEvent(layout)
                })
            await self._queue.put(ev)
            if reload:
                # make sure did_mount is called from leaf to root (reversed breadth first order)
                attached_items = list(attached.items())
                attached_items.sort(key=lambda x: len(x[0].parts),
                                    reverse=True)

                await self.root._run_special_methods(
                    [x[1] for x in attached_items], {},
                    self._flow_reload_manager)

    def app_initialize(self):
        """override this to init app before server start
        """
        pass

    async def app_initialize_async(self):
        """override this to init app before server start
        """
        self._loop = asyncio.get_running_loop()
        uid_to_comp = self.root._get_uid_to_comp_dict()
        # make sure did_mount is called from leaf to root (reversed breadth first order)
        uid_to_comp_items = list(uid_to_comp.items())
        uid_to_comp_items.sort(key=lambda x: len(x[0].parts), reverse=True)
        with enter_app_context(self):
            for _, v in uid_to_comp_items:
                await v._run_mount_special_methods(v, self._flow_reload_manager)

    def app_terminate(self):
        """override this to init app after server stop
        """
        pass

    async def app_terminate_async(self):
        """override this to init app after server stop
        """
        uid_to_comp = self.root._get_uid_encoded_to_comp_dict()
        with enter_app_context(self):
            for v in uid_to_comp.values():
                await v._run_unmount_special_methods(v, self._flow_reload_manager)

    def app_create_layout(self) -> mui.LayoutType:
        """override this in EditableApp to support reloadable layout
        """
        return {}

    def app_create_node_layout(self) -> Optional[mui.LayoutType]:
        """override this in EditableApp to support layout without fullscreen
        if not provided, will use fullscreen layout
        """
        return None

    def app_create_side_layout(self) -> Optional[mui.LayoutType]:
        """override this in EditableApp to support side layout when selected
        if not provided, will use fullscreen layout
        """
        return None

    def _get_app_dynamic_cls(self):
        assert self._app_dynamic_cls is not None
        return self._app_dynamic_cls

    def __repr__(self):
        if self._app_dynamic_cls is None:
            return f"App"
        return f"App[{self._get_app_dynamic_cls().module_path}]"

    def _get_app_service_unit(self):
        assert self._app_service_unit is not None
        return self._app_service_unit

    async def _get_app_layout(self, with_code_editor: bool = True):
        uid_to_comp = self.root._get_uid_encoded_to_comp_dict()
        # print({k: v._flow_uid for k, v in uid_to_comp.items()})
        layout_dict = await component_dict_to_serializable_dict_async(uid_to_comp)
        # print("????????????????", layout_dict)
        res = {
            "layout": layout_dict,
            "enableEditor": self._enable_editor,
            "fallback": "",
        }
        if self._dialog_z_index is not None:
            res["zIndex"] = self._dialog_z_index
        # if with_code_editor:
        #     res.update({
        #         "codeEditor": self.code_editor.get_state(),
        #     })
        # node_layout = self.app_create_node_layout()
        # if node_layout is not None:
        #     res["nodeLayout"] = mui.layout_unify(node_layout)
        # side_layout = self.app_create_side_layout()
        # if side_layout is not None:
        #     res["sideLayout"] = mui.layout_unify(side_layout)
        return res

    def _get_app_editor_state(self):
        res = {
            "enableEditor": self._enable_editor,
            "codeEditor": self.code_editor.get_state(),
        }
        return res

    def _get_fallback_layout(self,
                             fallback_msg: str,
                             with_code_editor: bool = True):
        res = {
            "layout": {},
            "enableEditor": self._enable_editor,
            "fallback": fallback_msg,
        }
        if with_code_editor:
            res.update({
                "codeEditor": self.code_editor.get_state(),
            })
        return res

    def init_enable_editor(self):
        self._enable_editor = True

    def set_init_window_size(self, size: List[Union[int, Undefined]]):
        self.root.props.width = size[0]
        self.root.props.height = size[1]

    async def headless_main(self):
        """override this method to support headless mode.
        you can use headless methods for control UIs such as 
        btn.headless_click and inp.headless_write to trigger
        callbacks.
        """
        raise NotImplementedError(
            "headless_main not exists. "
            "override headless_main to run in headless mode.")

    async def flow_run(self, event: ScheduleEvent):
        """override this method to support flow. output data will be 
        sent to all child nodes if not None.
        """
        return None

    async def _handle_code_editor_event_system(self,
                                               event: AppEditorFrontendEvent):
        if event.type == AppEditorFrontendEventType.SaveEditorState:
            self.code_editor._monaco_state = event.data
            return
        elif event.type == AppEditorFrontendEventType.Save:
            self.code_editor.value = event.data
        with _enter_app_conetxt(self):
            return await self.handle_code_editor_event(event)

    async def handle_code_editor_event(self, event: AppEditorFrontendEvent):
        """override this method to support vscode editor.
        """
        return

    async def _send_editor_event(self, event: AppEditorEvent):
        await self._queue.put(AppEvent("", {AppEventType.AppEditor: event}))

    def set_editor_value_event(self,
                               value: str,
                               language: str = "",
                               lineno: Optional[int] = None):
        self.code_editor.value = value
        if language:
            self.code_editor.language = language
        res: Dict[str, Any] = {
            "value": self.code_editor.value,
            "language": self.code_editor.language,
        }
        if lineno is not None:
            res["lineno"] = lineno
        app_ev = AppEditorEvent(AppEditorEventType.SetValue, res)
        return app_ev

    async def set_editor_value(self,
                               value: str,
                               language: str = "",
                               lineno: Optional[int] = None):
        """use this method to set editor value and language.
        """
        await self._send_editor_event(
            self.set_editor_value_event(value, language, lineno))

    @staticmethod
    async def __handle_dnd_event(handler: EventHandler,
                                 src_handler: EventHandler, src_event: Event):
        res = await src_handler.run_event_async(src_event)
        ev_res = Event(FrontendEventType.Drop.value, res, src_event.keys, src_event.indexes)
        await handler.run_event_async(ev_res)

    def _is_editable_app(self):
        return isinstance(self, EditableApp)

    def _get_self_as_editable_app(self):
        assert isinstance(self, EditableApp)
        return self

    async def handle_event(self, ev: UIEvent, is_sync: bool = False):
        res: Dict[str, Any] = {}
        for uid, data in ev.uid_to_data.items():
            keys: Union[Undefined, List[str]] = undefined
            uid_original = uid
            if TENSORPC_FLOW_COMP_UID_TEMPLATE_SPLIT in uid:
                split_idx = uid.find(TENSORPC_FLOW_COMP_UID_TEMPLATE_SPLIT)
                keys_str = uid[split_idx + len(TENSORPC_FLOW_COMP_UID_TEMPLATE_SPLIT):]
                uid = uid[:split_idx]
                keys = UniqueTreeId(keys_str).parts
            indexes = undefined
            indexes_raw = None
            if len(data) == 3 and data[2] is not None:
                indexes_raw = data[2]
                assert indexes_raw is not None 
                indexes = list(map(int, indexes_raw.split(".")))
            event = Event(data[0], data[1], keys, indexes)
            comps = self.root._get_comps_by_uid(uid)
            last_comp = comps[-1]
            if isinstance(last_comp, RemoteComponentBase) and last_comp.is_remote_mounted:
                if event.type == FrontendEventType.Drop.value:
                    # we know drop component is remote, we need to check src component.
                    src_data = data[1]
                    src_uid = src_data[TENSORPC_APP_DND_SRC_KEY]
                    src_comp = self.root._get_comp_by_uid(src_uid)
                    src_event = Event(FrontendEventType.DragCollect.value,
                                    src_data["data"], keys, indexes)
                    uievent_for_remote = UIEvent({
                        src_uid: (FrontendEventType.DragCollect.value, src_event, indexes_raw)
                    })
                    # shortcut for internal dnd
                    if isinstance(src_comp, RemoteComponentBase):
                        if src_comp is last_comp:
                            # internal dnd inside remote comp
                            res[uid_original] = await last_comp.handle_remote_event((uid_original, data), is_sync)
                            continue 
                    if isinstance(src_comp, RemoteComponentBase):
                        # collect drag data from remote comp
                        # TODO if collect_drag_source_data fail, should we call drop handler?
                        collect_res = await src_comp.collect_drag_source_data(uievent_for_remote)
                    else:
                        # collect drag data from local
                        collect_handlers = src_comp.get_event_handlers(
                            FrontendEventType.DragCollect.value)
                        if collect_handlers is None:
                            # no need to call DragCollect
                            collect_res = None
                        else:
                            collect_res = await src_comp.run_callback(partial(collect_handlers.handlers[0].run_event_async, event=src_event))
                    if collect_res is None:
                        src_data.pop(TENSORPC_APP_DND_SRC_KEY)
                        res[uid_original] = await last_comp.handle_remote_event((uid_original, data), is_sync)
                    else:
                        ev_data = (FrontendEventType.DropFromRemoteComp.value, collect_res, indexes_raw)
                        res[uid_original] = await last_comp.handle_remote_event((uid_original, ev_data), is_sync)
                    continue 
                else:
                    # handle another remote event here.
                    res[uid_original] = await last_comp.handle_remote_event((uid_original, data), is_sync)
                    continue
            ctxes = [
                c._flow_event_context_creator() for c in comps
                if c._flow_event_context_creator is not None
            ]
            with contextlib.ExitStack() as stack:
                for ctx in ctxes:
                    stack.enter_context(ctx)
                if event.type == FrontendEventType.DragCollect.value:
                    # WARNING: only used in remote comp dnd
                    # frontend shouldn't send this event.
                    # print("WTF1", uid, data)
                    src_uid = uid 
                    src_event = data[1]
                    src_comp = self.root._get_comp_by_uid(src_uid)
                    collect_handlers = src_comp.get_event_handlers(
                        FrontendEventType.DragCollect.value)
                    if collect_handlers is not None:
                        collect_res = await src_comp.run_callback(partial(collect_handlers.handlers[0].run_event_async, event=src_event))
                    else:
                        collect_res = None 
                    # print("WTF2", collect_res)

                    res[uid] = collect_res
                elif event.type == FrontendEventType.DropFromRemoteComp.value:
                    event = dataclasses.replace(event, type=FrontendEventType.Drop)
                    comp = comps[-1]
                    res[uid_original] = await comp.handle_event(
                        event, is_sync=is_sync)
                elif event.type == FrontendEventType.Drop.value:
                    # for drop event, we only support contexts in drop component.
                    src_data = data[1]
                    comp = comps[-1]
                    if TENSORPC_APP_DND_SRC_KEY not in src_data:
                        # if uid not in data, means no drag collect needed.
                        # 'uid' field is included by default. but
                        # we may remove it for remote comp dnd.
                        # so don't rely on this field.
                        # TODO change 'uid' to better name
                        res[uid_original] = await comp.handle_event(
                            event, is_sync=is_sync)
                        continue
                    src_uid = src_data[TENSORPC_APP_DND_SRC_KEY]
                    src_comp = self.root._get_comp_by_uid(src_uid)
                    src_event = Event(FrontendEventType.DragCollect.value,
                                    src_data["data"], keys, indexes)
                    if isinstance(src_comp, RemoteComponentBase):
                        # remote comp drop to local comp
                        uievent_for_remote = UIEvent({
                            src_uid: (FrontendEventType.DragCollect.value, src_event, indexes_raw)
                        })
                        collect_res = await src_comp.collect_drag_source_data(uievent_for_remote)
                        ev_res = event
                        if collect_res is not None:
                            ev_res = dataclasses.replace(event, data=collect_res)
                        res[uid_original] = await comp.handle_event(
                            ev_res, is_sync=is_sync)
                        continue 
                    collect_handlers = src_comp.get_event_handlers(
                        FrontendEventType.DragCollect.value)
                    handlers = comp.get_event_handlers(data[0])
                    # print(src_uid, comp, src_comp, handler, collect_handler)
                    if handlers is not None and collect_handlers is not None:
                        cbs = []
                        for handler in handlers.handlers:
                            cb = partial(self.__handle_dnd_event,
                                        handler=handler,
                                        # only first collect handler valid.
                                        # TODO limit number of collect handlers.
                                        src_handler=collect_handlers.handlers[0],
                                        src_event=src_event)
                            cbs.append(cb)
                        comp._task = asyncio.create_task(
                            comp.run_callbacks(cbs, sync_status_first=False))
                    else:
                        # drag object already contains drag data.
                        res[uid_original] = await comp.handle_event(
                            event, is_sync=is_sync)
                elif event.type == FrontendEventType.FileDrop.value:
                    # TODO remote component support
                    # for file drop, we can't use regular drop above, so
                    # just convert it to drop event, no drag collect needed.
                    res[uid_original] = await comps[-1].handle_event(
                        Event(FrontendEventType.FileDrop.value, data[1], keys,
                            indexes),
                        is_sync=is_sync)
                else:
                    res[uid_original] = await comps[-1].handle_event(
                        event, is_sync=is_sync)
        if is_sync:
            return res

    async def _handle_event_with_ctx(self, ev: UIEvent, is_sync: bool = False):
        # TODO run control from other component
        with _enter_app_conetxt(self):
            res = await self.handle_event(ev, is_sync)
        return res 

    def register_remote_comp_event_handler(self, key: str,
                                       handler: Callable[[RemoteCompEvent], Any]):
        self._flowapp_component_rpc_eemitter.on(key, handler)

    def unregister_remote_comp_event_handler(self, key: str,
                                            handler: Callable[[RemoteCompEvent],
                                                            Any]):
        self._flowapp_component_rpc_eemitter.remove_listener(key, handler)

    async def handle_msg_from_remote_comp(self, key: str, msg: RemoteCompEvent):
        with _enter_app_conetxt(self):
            return await self._flowapp_component_rpc_eemitter.emit_async(
                key, msg)

    async def handle_vscode_event(self, data: VscodeTensorpcMessage):
        with _enter_app_conetxt(self):
            return await self._flowapp_special_eemitter.emit_async(
                AppSpecialEventType.VscodeTensorpcMessage, data)

    async def handle_vscode_query(self, event: VscodeTensorpcQuery) -> Optional[dict]:
        # print("VSCODE QUERY", event)
        with _enter_app_conetxt(self):
            try:
                workspace = event.get_workspace_path()
                if workspace is None:
                    return None 
                if event.type == VscodeTensorpcQueryType.SyncBreakpoints:
                    self._flowapp_vscode_state.set_workspace_breakpoints(event.workspaceUri, [VscodeBreakpoint(**d) for d in event.data])
                    return None
                elif event.type == VscodeTensorpcQueryType.BreakpointUpdate:
                    # bkpts = [VscodeBreakpoint(**d) for d in event.data]
                    self._flowapp_vscode_state.set_workspace_breakpoints(event.workspaceUri, [VscodeBreakpoint(**d) for d in event.data])
                    await self._flowapp_special_eemitter.emit_async(
                        AppSpecialEventType.VscodeBreakpointChange, self._flowapp_vscode_state.get_all_breakpoints())
                    return None
                if not self._is_app_workspace_child_of_vscode_workspace_root(str(workspace)):
                    return None
                storage = await self.get_vscode_storage_lazy()
                if event.type == VscodeTensorpcQueryType.TraceTrees:
                    queries = VscodeTraceQueries(**event.data)
                    res = as_dict_no_undefined(storage.handle_vscode_trace_query(queries))
                    return res 
                elif event.type == VscodeTensorpcQueryType.DeleteTraceTree:
                    await storage.remove_trace_tree_with_update(event.data)
                    return None
            except:
                traceback.print_exc()
                raise
        return None 

    async def _run_autorun(self, cb: Callable):
        try:
            coro = cb()
            if inspect.iscoroutine(coro):
                await coro
            await self._flowapp_special_eemitter.emit_async(
                AppSpecialEventType.AutoRunEnd, None)
        except:
            traceback.print_exc()
            if self._flowapp_enable_exception_inspect:
                await self._inspect_exception()

    async def _inspect_exception(self):
        try:
            comp = self.find_component(plus.ObjectInspector)
            if comp is not None and comp.enable_exception_inspect:
                await comp.add_object_to_tree(get_exception_frame_stack(), "exception")
        except:
            traceback.print_exc()

    def _inspect_exception_sync(self):
        try:
            comp = self.find_component(plus.ObjectInspector)
            if comp is not None and comp.enable_exception_inspect:
                comp.set_object_sync(get_exception_frame_stack(), "exception")
        except:
            traceback.print_exc()

    async def copy_text_to_clipboard(self, text: str):
        """copy to clipboard in frontend."""
        await self._queue.put(
            AppEvent(
                "",
                {AppEventType.CopyToClipboard: CopyToClipboardEvent(text)}))

    def find_component(
            self,
            type: Type[T],
            validator: Optional[Callable[[T], bool]] = None) -> Optional[T]:
        """find component in comp tree. breath-first.
        """
        res: List[Optional[T]] = [None]

        def handler(name, comp):
            if loose_isinstance(comp, (type, )):
                if (validator is None) or (validator is not None
                                           and validator(comp)):
                    res[0] = comp
                    return ForEachResult.Return
            elif isinstance(
                    comp, mui.FlexBox
            ) and comp._wrapped_obj is not None and loose_isinstance(
                    comp._wrapped_obj, (type, )):
                if (validator is None) or (validator is not None
                                           and validator(comp._wrapped_obj)):
                    res[0] = comp._wrapped_obj
                    return ForEachResult.Return

        self.root._foreach_comp(handler)
        return res[0]

    def find_all_components(
            self,
            type: Type[T],
            check_nested: bool = False,
            validator: Optional[Callable[[T], bool]] = None) -> List[T]:
        res: List[T] = []

        def handler(name, comp):
            if isinstance(comp, type):
                if (validator is None) or (validator is not None
                                           and validator(comp)):
                    res.append(comp)
                    # tell foreach to continue instead of search children
                    if not check_nested:
                        return ForEachResult.Continue

        self.root._foreach_comp(handler)
        return res

    async def _recover_code_editor(self):
        if self._use_app_editor:
            obj = type(self._get_user_app_object())
            lines, lineno = inspect.findsource(obj)
            await self.set_editor_value(value="".join(lines), lineno=lineno)


_WATCHDOG_MODIFY_EVENT_TYPES = Union[watchdog.events.DirModifiedEvent,
                                     watchdog.events.FileModifiedEvent]


class _WatchDogForAppFile(watchdog.events.FileSystemEventHandler):

    def __init__(
            self, on_modified: Callable[[_WATCHDOG_MODIFY_EVENT_TYPES],
                                        None]) -> None:
        super().__init__()
        self._on_modified = on_modified

    def on_modified(self, event: _WATCHDOG_MODIFY_EVENT_TYPES):
        if isinstance(event, watchdog.events.FileModifiedEvent):
            return self._on_modified(event)


class EditableApp(App):

    def __init__(self,
                 reloadable_layout: bool = False,
                 use_app_editor: bool = True,
                 flex_flow: Union[str, Undefined] = "column nowrap",
                 maxqsize: int = 10,
                 observed_files: Optional[List[str]] = None,
                 external_root: Optional[mui.FlexBox] = None,
                 external_wrapped_obj: Optional[Any] = None,
                 reload_manager: Optional[AppReloadManager] = None,
                 is_remote_component: bool = False) -> None:
        super().__init__(flex_flow,
                         maxqsize,
                         external_root=external_root,
                         external_wrapped_obj=external_wrapped_obj,
                         reload_manager=reload_manager,
                         is_remote_component=is_remote_component)
        self._use_app_editor = use_app_editor
        if use_app_editor:
            obj = type(self._get_user_app_object())
            lines, lineno = inspect.findsource(obj)
            self.code_editor.value = "".join(lines)
            self.code_editor.language = "python"
            self.code_editor.set_init_line_number(lineno)
            self.code_editor.freeze()
        self._watchdog_prev_content = ""
        self._flow_reloadable_layout = reloadable_layout
        if reloadable_layout:
            self._app_force_use_layout_function()
        self._flow_observed_files = observed_files
        self._init_observe_paths: Set[str] = set()
        self._protect_app_observe_call: bool = False
        # some network based fs modify event may trigger multiple times
        # during write, so we need to debounce it to avoid incomplete write.
        self._fs_event_debounce = 0.1

    @contextlib.contextmanager
    def _flowapp_protect_app_observe_call(self, ctx: _FlowAppObserveContext):
        try:
            self._protect_app_observe_call = True
            with _enter_flowapp_observe_context(ctx) as ctx:
                yield ctx
        finally:
            self._protect_app_observe_call = False

    def app_initialize(self):
        super().app_initialize()
        user_obj = self._get_user_app_object()
        metas_dict = self._flow_reload_manager.query_type_method_meta_dict(
            type(user_obj))

        # for m in metas:
        #     m.bind(user_obj)
        # qualname_prefix = type(user_obj).__qualname__
        obentry = _WatchDogWatchEntry({}, None)
        for meta_type_uid, meta_item in metas_dict.items():
            if meta_item.type is not None:
                # TODO should we ignore global functions?
                qualname_prefix = meta_type_uid[1]
                obmeta = _LayoutObserveMeta({self: None}, qualname_prefix,
                                            meta_item.type, meta_item.is_leaf,
                                            meta_item.metas)
                obentry.obmetas[meta_type_uid] = obmeta
        # obentry = _WatchDogWatchEntry(
        #     [_LayoutObserveMeta(self, qualname_prefix, metas, None)], None)
        path = ""
        if not self._is_remote_component:
            dcls = self._get_app_dynamic_cls()
            print("dcls.is_dynamic_code", dcls.is_dynamic_code)
            if not dcls.is_dynamic_code:
                path = dcls.file_path
                self._flowapp_change_observers[path] = obentry
        self._watchdog_watcher = None
        self._watchdog_observer = None
        registry = self.get_observed_func_registry()
        if not self._flow_app_is_headless:
            observer = Observer()
            self._watchdog_watcher = _WatchDogForAppFile(
                debounce(self._fs_event_debounce)(self._watchdog_on_modified))
            if self._flow_observed_files is not None:
                for p in self._flow_observed_files:
                    assert Path(p).exists(), f"{p} must exist"
                paths = set(self._flow_observed_files)
            else:
                paths = set(self.__get_default_observe_paths())
            for p in registry.get_path_to_qname().keys():
                paths.add(str(Path(p).resolve()))
            self._init_observe_paths.update(paths)
            self._flowapp_code_mgr = SimpleCodeManager(list(paths))
            paths = set(self._flowapp_code_mgr.file_to_entry.keys())
            # add all observed function paths
            for p in paths:
                observer.schedule(self._watchdog_watcher, p, recursive=True if compat.InMacOS else False)
            observer.start()
            self._watchdog_observer = observer
        else:
            self._flowapp_code_mgr = None
        self._watchdog_ignore_next = False
        self._loop = asyncio.get_running_loop()
        self._watch_lock = threading.Lock()

    def __observe_layout_effect(
        self,
        obj: mui.FlexBox,
        callback: Optional[Callable[[mui.FlexBox, ServFunctionMeta],
                                    Coroutine]] = None):
        self._flowapp_observe(obj, callback)
        return partial(self._flowapp_remove_observer, obj)

    def observe_layout(
        self,
        obj: mui.FlexBox,
        callback: Optional[Callable[[mui.FlexBox, ServFunctionMeta],
                                    Coroutine]] = None):
        if not obj.effects.has_effect_key(TENSORPC_FLOW_EFFECTS_OBSERVE):
            # already observed
            obj.effects.use_effect(partial(self.__observe_layout_effect, obj,
                                           callback),
                                   key=TENSORPC_FLOW_EFFECTS_OBSERVE)
            if obj.is_mounted():
                self._flowapp_observe(obj, callback)
                # TODO better code
                obj.effects._flow_unmounted_effects[
                    TENSORPC_FLOW_EFFECTS_OBSERVE].append(
                        partial(self._flowapp_remove_observer, obj))

    def _flowapp_observe(
        self,
        obj: mui.FlexBox,
        callback: Optional[Callable[[mui.FlexBox, ServFunctionMeta],
                                    Coroutine]] = None):
        ctx = _get_flowapp_observe_context()
        if ctx is not None:
            ctx._added_layouts_and_cbs[obj] = callback
            return
        # TODO better error msg if app editable not enabled
        path = obj._flow_comp_def_path
        assert self._protect_app_observe_call is False, "you can't call observe inside observe reload callback"
        assert path != "" and self._watchdog_observer is not None
        path_resolved = self._flow_reload_manager._resolve_path_may_in_memory(
            path)
        if path_resolved not in self._flowapp_change_observers:
            self._flowapp_change_observers[
                path_resolved] = _WatchDogWatchEntry({}, None)
        obentry = self._flowapp_change_observers[path_resolved]
        if len(obentry.obmetas) == 0 and not is_tensorpc_dynamic_path(path) and self._watchdog_watcher is not None:
            # no need to schedule watchdog.
            if path_resolved not in self._init_observe_paths:
                watch = self._watchdog_observer.schedule(
                    self._watchdog_watcher, path, recursive=True if compat.InMacOS else False)
                obentry.watch = watch
        assert self._flowapp_code_mgr is not None
        if not self._flowapp_code_mgr._check_path_exists(path):
            self._flowapp_code_mgr._add_new_code(
                path, self._flow_reload_manager.in_memory_fs)
        metas_dict = self._flow_reload_manager.query_type_method_meta_dict(
            type(obj._get_user_object()))

        for meta_type_uid, meta_item in metas_dict.items():
            if meta_item.type is not None:
                if meta_type_uid in obentry.obmetas:
                    obentry.obmetas[meta_type_uid].layouts[obj] = callback
                else:
                    qualname_prefix = meta_type_uid[1]
                    obmeta = _LayoutObserveMeta({obj: callback},
                                                qualname_prefix,
                                                meta_item.type,
                                                meta_item.is_leaf,
                                                meta_item.metas)
                    obentry.obmetas[meta_type_uid] = obmeta

    def _flowapp_remove_observer(self, obj: mui.FlexBox):
        ctx = _get_flowapp_observe_context()
        if ctx is not None:
            ctx._removed_layouts.append(obj)
            return
        path = obj._flow_comp_def_path
        assert path != "" and self._watchdog_observer is not None
        path_resolved = self._flow_reload_manager._resolve_path_may_in_memory(
            path)
        assert self._protect_app_observe_call is False, "you can't call remove observer inside observe reload callback"
        assert self._flowapp_code_mgr is not None
        # self._flowapp_code_mgr._remove_path(path)
        if path_resolved in self._flowapp_change_observers:
            obentry = self._flowapp_change_observers[path_resolved]
            types_to_remove: List[ObjectReloadManager.TypeUID] = []
            for k, v in obentry.obmetas.items():
                if obj in v.layouts:
                    v.layouts.pop(obj)
                if len(v.layouts) == 0:
                    types_to_remove.append(k)
            for k in types_to_remove:
                del obentry.obmetas[k]
            # new_obmetas: List[_LayoutObserveMeta] = []
            # for obmeta in obentry.obmetas:
            #     if obj is not obmeta.layout:
            #         new_obmetas.append(obmeta)
            # obentry.obmetas = new_obmetas
            if len(obentry.obmetas) == 0 and obentry.watch is not None:
                if path_resolved not in self._init_observe_paths:
                    self._watchdog_observer.unschedule(obentry.watch)

    def __get_default_observe_paths(self):
        uid_to_comp = self.root._get_uid_encoded_to_comp_dict()
        res: Set[str] = set()
        for k, v in uid_to_comp.items():
            v_file = v._flow_comp_def_path
            if not v_file:
                continue
            try:
                # if comp is inside tensorpc official, ignore it.
                Path(v_file).relative_to(PACKAGE_ROOT)
                continue
            except:
                pass
            res.add(v_file)
        if not self._is_remote_component:
            dcls = self._get_app_dynamic_cls()
            if not dcls.is_dynamic_code:
                res.add(dcls.file_path)
        return res

    def __get_callback_metas_in_file(self, change_file: str,
                                     layout: mui.FlexBox):
        uid_to_comp = layout._get_uid_encoded_to_comp_dict()
        resolved_path = self._flow_reload_manager._resolve_path_may_in_memory(
            change_file)
        return create_reload_metas(uid_to_comp, resolved_path)

    async def _reload_object_with_new_code(self,
                                           path: str,
                                           new_code: Optional[str] = None):
        """reload order:
        for leaf type, we will support new method. if code change, we will replace all method with reloaded methods.
        for base types, we don't support new method. if code change, only reload method with same name. if the method
            is already reloaded in child type, it will be ignored.
        """
        assert self._flowapp_code_mgr is not None
        resolved_path = self._flowapp_code_mgr._resolve_path(path)
        if self._use_app_editor and not self._is_remote_component:
            dcls = self._get_app_dynamic_cls()
            resolved_app_path = self._flowapp_code_mgr._resolve_path(
                dcls.file_path)

            if resolved_path == resolved_app_path and new_code is not None:
                await self.set_editor_value(new_code)
        try:
            changes = self._flowapp_code_mgr.update_code(
                resolved_path, new_code)
        except:
            # ast parse error
            traceback.print_exc()
            return
        if changes is None:
            return
        rprint(f"<watchdog> {path}")
        new, change, _ = changes
        new_data = self._flowapp_code_mgr.get_code(resolved_path)
        is_reload = False
        is_callback_change = False
        callbacks_of_this_file: Optional[List[_CompReloadMeta]] = None
        observe_ctx = _FlowAppObserveContext()
        try:
            with self._flowapp_protect_app_observe_call(observe_ctx):
                if resolved_path in self._flowapp_change_observers:
                    obmetas = self._flowapp_change_observers[
                        resolved_path].obmetas.copy()
                    obmetas_items = list(obmetas.items())
                    # sort obmetas_items by mro
                    obmetas_items.sort(key=lambda x: len(x[1].type.mro()),
                                       reverse=True)
                    # store accessed metas in inheritance tree
                    resolved_metas: Dict[ObjectReloadManager.TypeUID,
                                         Set[str]] = {}
                    # print("len(obmetas)", resolved_path, len(obmetas))
                    for type_uid, obmeta in obmetas_items:
                        # get changed metas for special methods
                        # print(new, change)
                        if type_uid not in resolved_metas:
                            resolved_metas[type_uid] = set()
                        changed_metas: List[ServFunctionMeta] = []
                        for m in obmeta.metas:
                            if m.qualname in change:
                                changed_metas.append(m)
                        new_method_names: List[str] = [
                            x for x in new
                            if x.startswith(obmeta.qualname_prefix)
                            and x != obmeta.qualname_prefix
                        ]
                        # layout = obmeta.layout
                        for layout in obmeta.layouts:
                            if not is_callback_change:
                                if isinstance(layout, App):
                                    callbacks_of_this_file = self.__get_callback_metas_in_file(
                                        resolved_path, self.root)
                                else:
                                    # TODO should we check all callbacks instead of changed layout?
                                    callbacks_of_this_file = self.__get_callback_metas_in_file(
                                        resolved_path, self.root)
                                # print(len(callbacks_of_this_file), "callbacks_of_this_file 0", change.keys())
                                for cb_meta in callbacks_of_this_file:
                                    # print(cb_meta.cb_qualname)
                                    if cb_meta.cb_qualname in change:
                                        is_callback_change = True
                                        break
                            # print("is_callback_change", is_callback_change)
                        # for m in changed_metas:
                        #     print(m.qualname, "CHANGED")
                        # do reload, run special methods
                        flow_special_for_check = FlowSpecialMethods(
                            changed_metas)
                        do_reload = flow_special_for_check.contains_special_method(
                        ) or bool(new_method_names)
                        # print("do_reload", do_reload)
                        if not do_reload:
                            continue
                        # rprint(obmeta.layouts)
                        for i, (layout, layout_reload_cb) in enumerate(
                                obmeta.layouts.items()):
                            changed_user_obj = None

                            if layout is self:
                                # reload app
                                if changed_metas or bool(new_method_names):
                                    # reload app servunit and method
                                    changed_user_obj = self._get_user_app_object(
                                    )
                                    # self._get_app_dynamic_cls(
                                    # ).reload_obj_methods(user_obj, {}, self._flow_reload_manager)
                                    if not self._is_remote_component:
                                        self._get_app_service_unit().reload_metas(
                                            self._flow_reload_manager)
                            else:
                                assert isinstance(
                                    layout, mui.FlexBox), f"{type(layout)}"
                                # if self.code_editor.external_path is not None and new_code is None:
                                #     if str(
                                #             Path(self.code_editor.external_path).
                                #             resolve()) == resolved_path:
                                #         await self.set_editor_value(new_data, lineno=0)
                                # reload dynamic layout
                                if changed_metas or bool(new_method_names):
                                    changed_user_obj = layout._get_user_object(
                                    )
                            # print("RTX", changed_user_obj, new_method_names)
                            if changed_user_obj is not None:
                                # reload_res = self._flow_reload_manager.reload_type(
                                #     type(changed_user_obj))
                                reload_res = self._flow_reload_manager.reload_type(
                                    obmeta.type)

                                if not is_reload:
                                    is_reload = reload_res.is_reload
                                updated_type = reload_res.type_meta.get_local_type_from_module_dict(
                                    reload_res.module_entry.module_dict)
                                # recreate metas with new type and new qualname_to_code
                                # TODO handle special methods in mro
                                updated_metas = self._flow_reload_manager.query_type_method_meta(
                                    updated_type, include_base=False)
                                # if is leaf type, reload all meta, otherwise only reload meta saved initally.
                                if is_reload and obmeta.is_leaf:
                                    obmeta.metas = updated_metas
                                # print("CHANGED USER OBJ", len(obmetas))
                                changed_metas = [
                                    m for m in updated_metas
                                    if m.qualname in change
                                ]
                                if obmeta.is_leaf:
                                    changed_metas += [
                                        m for m in updated_metas
                                        if m.qualname in new
                                    ]
                                else:
                                    prev_meta_names = [
                                        x.qualname for x in obmeta.metas
                                    ]
                                    changed_metas = list(
                                        filter(
                                            lambda x: x.qualname in
                                            prev_meta_names, changed_metas))
                                changed_metas_candidate = changed_metas
                                new_changed_metas: List[ServFunctionMeta] = []
                                # if meta already reloaded in child type, ignore it.
                                for c in changed_metas_candidate:
                                    if c.name not in resolved_metas[type_uid]:
                                        resolved_metas[type_uid].add(c.name)
                                        new_changed_metas.append(c)
                                change_metas = new_changed_metas
                                for c in change_metas:
                                    c.bind(changed_user_obj)
                                    print(f"{c.name}, ------------")
                                    # print(c.code)
                                    # print("-----------")
                                    # print(change[c.qualname])
                                # we need to update metas of layout with new type.
                                # meta is binded in bind_and_reset_object_methods
                                if changed_metas:
                                    bind_and_reset_object_methods(
                                        changed_user_obj, changed_metas)
                                if layout is self:
                                    if not self._is_remote_component:
                                        self._get_app_dynamic_cls(
                                        ).module_dict = reload_res.module_entry.module_dict
                                        self._get_app_service_unit().reload_metas(
                                            self._flow_reload_manager)
                            # use updated metas to run special methods such as create_layout and auto_run
                            if changed_metas:
                                flow_special = FlowSpecialMethods(
                                    changed_metas)
                                with _enter_app_conetxt(self):
                                    if flow_special.create_layout:
                                        fn = flow_special.create_layout.get_binded_fn(
                                        )
                                        if isinstance(layout, App):
                                            await self._app_run_layout_function(
                                                True,
                                                with_code_editor=False,
                                                reload=True,
                                                decorator_fn=fn)
                                        else:
                                            if layout_reload_cb is not None:
                                                # handle layout in callback
                                                new_layout = await layout_reload_cb(
                                                    layout,
                                                    flow_special.create_layout)
                                                # if new_layout is not None:
                                                # obmeta.layouts[i] = new_layout
                                                # observe_ctx._reloaded_layout_pairs.append((layout, new_layout))
                                            # dynamic layout
                                    if flow_special.create_preview_layout:
                                        if not isinstance(layout, App):
                                            if layout_reload_cb is not None:
                                                # handle layout in callback
                                                new_layout = await layout_reload_cb(
                                                    layout, flow_special.
                                                    create_preview_layout)
                                                # if new_layout is not None:
                                                # obmeta.layouts[i] = new_layout
                                                # observe_ctx._reloaded_layout_pairs.append((layout, new_layout))
                                    for auto_run in flow_special.auto_runs:
                                        if auto_run is not None:
                                            await self._run_autorun(
                                                auto_run.get_binded_fn())
                            # handle special methods
                ob_registry = self.get_observed_func_registry()
                observed_func_changed = ob_registry.observed_func_changed(
                    resolved_path, change)
                if observed_func_changed:
                    # this handler only handle one file, so we only need to reload once.
                    first_func_qname_pair = ob_registry.get_path_to_qname(
                    )[resolved_path][0]
                    entry = ob_registry[first_func_qname_pair[0]]
                    entry_func_unwrap = inspect.unwrap(entry.current_func)
                    reload_res = self._flow_reload_manager.reload_type(
                        entry_func_unwrap)
                    if not is_reload:
                        is_reload = reload_res.is_reload
                    # for qname in observed_func_changed:
                    with _enter_app_conetxt(self):
                        for qname in observed_func_changed:
                            entry = ob_registry[qname]
                            if len(entry.autorun_block_symbol) == 0:
                                if entry.autorun_when_changed:
                                    await self._run_autorun(entry.current_func)
                            else:
                                if entry.first_changed_block_idx < len(
                                        entry.body_code_blocks):
                                    first_changed_block_idx = entry.first_changed_block_idx
                                    if not entry.autorun_locals:
                                        first_changed_block_idx = 0
                                    code_to_run = "\n".join(
                                        entry.body_code_blocks[
                                            first_changed_block_idx:])
                                    code_to_run = remove_common_indent_from_code(
                                        code_to_run)
                                    code_locals = entry.autorun_locals
                                    func_globals = entry.current_func.__globals__
                                    code_comp = compile(
                                        code_to_run,
                                        f"<{TENSORPC_FILE_NAME_PREFIX}-scripts-{entry.qualname}>",
                                        "exec")
                                    exec(code_comp, func_globals, code_locals)
                        await self._flowapp_special_eemitter.emit_async(
                            AppSpecialEventType.ObservedFunctionChange,
                            observed_func_changed)
                # print(is_callback_change, is_reload)
                if is_callback_change or is_reload:
                    # reset all callbacks in this file
                    if callbacks_of_this_file is None:
                        callbacks_of_this_file = self.__get_callback_metas_in_file(
                            resolved_path, self.root)
                    # print(len(callbacks_of_this_file), "callbacks_of_this_file")
                    if callbacks_of_this_file:
                        cb_real = callbacks_of_this_file[0].cb_real
                        reload_res = self._flow_reload_manager.reload_type(
                            inspect.unwrap(cb_real))
                        for meta in callbacks_of_this_file:
                            print("RELOAD CB", meta.cb_qualname)
                            handler = meta.handler
                            cb = inspect.unwrap(handler.cb)
                            new_method, _ = reload_method(
                                cb, reload_res.module_entry.module_dict)
                            if new_method is not None:
                                handler.cb = new_method

        except:
            # watchdog thread can't fail
            traceback.print_exc()
            return
        finally:
            # print("START MODIFY OMBETA")
            # for pair in observe_ctx._reloaded_layout_pairs:
            #     observe_ctx._removed_layouts.remove(pair[0])
            #     observe_ctx._added_layouts_and_cbs.pop(pair[1])
            # print(len(observe_ctx._removed_layouts), len(observe_ctx._added_layouts_and_cbs))
            for layout in observe_ctx._removed_layouts:
                self._flowapp_remove_observer(layout)
            for layout, cb in observe_ctx._added_layouts_and_cbs.items():
                self._flowapp_observe(layout, cb)
            return

    def _watchdog_on_modified(self, ev: _WATCHDOG_MODIFY_EVENT_TYPES):
        # which event trigger reload?
        # 1. special method code change
        # 2. callback code change (handled outsite)
        # 3. new methods detected in layout

        # WARNING: other events WON'T trigger reload.

        # what happened when reload?
        # 1. all method of object (app or dynamic layout) will be reset
        # 2. all callback defined in changed file will be reset
        # 3. if layout function changed, load new layout
        # 4. if mount/unmount function changed, reset them
        # 5. if autorun changed, run them

        if isinstance(ev, watchdog.events.FileModifiedEvent):
            rprint("<watchdog>", ev)
            with self._watch_lock:
                if self._flowapp_code_mgr is None or self._loop is None:
                    return
                if isinstance(ev.src_path, bytes):
                    src_path = ev.src_path.decode()
                else:
                    src_path = cast(str, ev.src_path)
                asyncio.run_coroutine_threadsafe(
                    self._reload_object_with_new_code(src_path), self._loop)

    async def handle_code_editor_event(self, event: AppEditorFrontendEvent):
        """override this method to support vscode editor.
        """
        if self._use_app_editor and not self._is_remote_component:
            app_path = self._get_app_dynamic_cls().file_path
            if event.type == AppEditorFrontendEventType.Save:
                with self._watch_lock:
                    # self._watchdog_ignore_next = True
                    if self.code_editor.external_path is not None:
                        path = self.code_editor.external_path
                    else:
                        path = app_path
                    # if self.code_editor.external_path is None:
                    with open(path, "w") as f:
                        f.write(event.data)
                    await self._reload_object_with_new_code(path, event.data)
        return


class EditableLayoutApp(EditableApp):

    def __init__(self,
                 use_app_editor: bool = True,
                 flex_flow: Union[str, Undefined] = "column nowrap",
                 maxqsize: int = 10,
                 observed_files: Optional[List[str]] = None,
                 external_root: Optional[mui.FlexBox] = None,
                 reload_manager: Optional[AppReloadManager] = None) -> None:
        super().__init__(True,
                         use_app_editor,
                         flex_flow,
                         maxqsize,
                         observed_files,
                         external_root=external_root,
                         reload_manager=reload_manager)

