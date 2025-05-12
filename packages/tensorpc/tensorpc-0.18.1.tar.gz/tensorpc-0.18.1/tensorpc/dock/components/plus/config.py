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

import dataclasses
import enum
from functools import partial
import json
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, TypeVar, Union, Generic
import operator
from typing_extensions import Literal, Annotated, get_origin, get_args
from tensorpc.core.tree_id import UniqueTreeIdForTree
from tensorpc.core.annolib import is_annotated

from .. import mui
from tensorpc.core.datamodel import typemetas
from tensorpc.dock.core.component import AppEvent
from .. import three
import inspect

T = TypeVar("T")

_CONFIG_META_KEY = "_tensorpc_config_panel_meta"

_BASE_TYPES = (
    int,
    float,
    bool,
    str,
)

# def get_args(t: Any) -> Tuple[Any, ...]:
#     return getattr(t, "__args__", None) or ()

_BASE_TYPES = (int, float, bool, str, mui.Undefined)


def _check_is_basic_type(tp):
    origin = get_origin(tp)
    if origin is not None:
        if origin in (list, tuple, dict, Union):
            args = get_args(tp)
            return all(_check_is_basic_type(a) for a in args)
        else:
            return origin in _BASE_TYPES or origin is Literal
    else:
        if inspect.isclass(tp):
            return tp in _BASE_TYPES or issubclass(tp,
                                                   (enum.Enum, enum.IntEnum))
        else:
            return False


@dataclasses.dataclass
class ConfigMeta:
    alias: Optional[str]


@dataclasses.dataclass
class SwitchMeta(ConfigMeta):
    pass


@dataclasses.dataclass
class InputMeta(ConfigMeta):
    multiline: bool
    rows: int
    font_size: mui.ValueType
    font_family: str


@dataclasses.dataclass
class SliderMeta(ConfigMeta):
    begin: mui.NumberType
    end: mui.NumberType
    step: Optional[mui.NumberType] = None


@dataclasses.dataclass
class ControlItemMeta:
    getter: Callable[[], Any]
    setter: Callable[[Any], None]
    compare: Callable[[Any], bool]


_BUILTIN_DCLS_TYPE = set([mui.ControlColorRGB, mui.ControlColorRGBA])


def setattr_single(val, obj, name, mapper: Optional[Callable] = None):
    if mapper is not None:
        setattr(obj, name, mapper(val))
    else:
        setattr(obj, name, val)


# def setattr_vector_n(val, obj, name):
#     # val: [axis, value]
#     val_prev = getattr(obj, name).data.copy()
#     val_prev[val[0]] = val[1]
#     setattr(obj, name, mui.ControlVectorN(val_prev))


def setattr_vector_n_tuple(val,
                           obj,
                           name,
                           count: int,
                           default: Optional[Tuple] = None):
    # val: [axis, value]
    prev_val = getattr(obj, name)
    if isinstance(prev_val, mui.Undefined):
        if default is None:
            prev_val = [0] * count
        else:
            prev_val = default
    val_prev = list(prev_val).copy()
    val_prev[val[0]] = val[1]
    setattr(obj, name, tuple(val_prev))


def getattr_single(obj, name):
    return getattr(obj, name)


def compare_single(value, obj, name, mapper: Optional[Callable] = None):
    if mapper is not None:
        return getattr(obj, name) == mapper(value)
    else:
        return getattr(obj, name) == value


def compare_vector_n(value, obj, name):
    # val: [axis, value]
    return getattr(obj, name).data[value[0]] == value[1]


def compare_vector_n_tuple(value, obj, name):
    # val: [axis, value]
    val = getattr(obj, name)
    if isinstance(val, mui.Undefined):
        return False
    return getattr(obj, name)[value[0]] == value[1]


def _parse_base_type(ty: Type, current_obj, field_name: str,
                     child_node: mui.ControlNode) -> Optional[ControlItemMeta]:
    getter = partial(getattr_single, obj=current_obj, name=field_name)
    comparer = partial(compare_single, obj=current_obj, name=field_name)
    if ty is bool:
        # use switch
        # if meta is not None:
        #     assert isinstance(meta, SwitchMeta)
        child_node.type = mui.ControlNodeType.Bool.value
        child_node.value = getattr(current_obj, field_name)
        setter = partial(setattr_single,
                         obj=current_obj,
                         name=field_name,
                         mapper=bool)
        # setter = lambda x: setattrV2(current_obj, f.name, bool(x))

    elif ty is int or ty is float:
        # use textfield with number type
        if ty is int:
            setter = partial(setattr_single,
                             obj=current_obj,
                             name=field_name,
                             mapper=int)

            # setter = lambda x: setattrV2(current_obj, f.name, int(x))
        else:
            setter = partial(setattr_single,
                             obj=current_obj,
                             name=field_name,
                             mapper=float)

            # setter = lambda x: setattrV2(current_obj, f.name, float(x))
        child_node.type = mui.ControlNodeType.Number.value
        child_node.value = getattr(current_obj, field_name)
        if ty is int:
            child_node.isInteger = True
        if ty is int:
            child_node.step = 1
        #     raise NotImplementedError
    elif ty is str:
        # use textfield
        setter = partial(setattr_single,
                         obj=current_obj,
                         name=field_name,
                         mapper=str)

        # setter = lambda x: setattr(current_obj, f.name, str(x))
        child_node.type = mui.ControlNodeType.String.value
        child_node.value = getattr(current_obj, field_name)
    elif ty is mui.ControlColorRGB or ty is mui.ControlColorRGBA:
        if ty is mui.ControlColorRGB:
            child_node.type = mui.ControlNodeType.ColorRGB.value
        else:
            child_node.type = mui.ControlNodeType.ColorRGBA.value
        child_node.value = getattr(current_obj, field_name)
        if ty is mui.ControlColorRGB:
            mapper = lambda x: mui.ControlColorRGB(x["r"], x["g"], x["b"])
        else:
            mapper = lambda x: mui.ControlColorRGBA(x["r"], x["g"], x["b"], x[
                "a"])
        setter = partial(setattr_single,
                         obj=current_obj,
                         name=field_name,
                         mapper=mapper)
        comparer = partial(compare_single,
                           obj=current_obj,
                           name=field_name,
                           mapper=mapper)
    else:
        ty_origin = get_origin(ty)
        # print(ty, ty_origin, type(ty), type(ty_origin))
        if ty_origin is Literal:
            child_node.type = mui.ControlNodeType.Select.value
            child_node.value = getattr(current_obj, field_name)
            child_node.selects = list((str(x), x) for x in get_args(ty))
            # setter = lambda x: setattr(current_obj, f.name, x)
            setter = partial(setattr_single, obj=current_obj, name=field_name)

        elif ty_origin is None and issubclass(ty, (enum.Enum, enum.IntEnum)):
            child_node.type = mui.ControlNodeType.Select.value
            item = getattr(current_obj, field_name)
            if not isinstance(item, mui.Undefined):
                child_node.value = getattr(current_obj, field_name).value
            child_node.selects = list((x.name, x.value) for x in ty)
            # setter = lambda x: setattr(current_obj, f.name, ty(x))
            # print(ty, child_node.selects)
            setter = partial(setattr_single,
                             obj=current_obj,
                             name=field_name,
                             mapper=ty)
        elif ty_origin is Union:
            # handle "Union[..., Undefined]" in component props
            union_args = get_args(ty)
            if mui.Undefined in union_args:
                union_args = tuple(x for x in union_args
                                   if x is not mui.Undefined)
            if len(union_args) == 1:
                return _parse_base_type(union_args[0], current_obj, field_name,
                                        child_node)
            else:
                # handle NumberType and ValueType in component props
                union_args_set = set(union_args)
                if union_args_set == set([int, float]):
                    # number type
                    # use float type
                    return _parse_base_type(float, current_obj, field_name,
                                            child_node)
                elif union_args_set == set([int, float, str]):
                    # value type
                    # use str type
                    return _parse_base_type(str, current_obj, field_name,
                                            child_node)
            return None
        else:
            return None

    return ControlItemMeta(getter, setter, comparer)


def _check_union_is_valid_subset_ignore_undefined(ty, ty_origin,
                                                  target_set: Set[Type]):
    if ty_origin is Union:
        # handle "Union[..., Undefined]" in component props
        union_args = get_args(ty)
        if mui.Undefined in union_args:
            union_args = tuple(x for x in union_args if x is not mui.Undefined)
        union_args_set = set(union_args)
        return union_args_set.issubset(target_set)
    return ty in target_set


def parse_to_control_nodes(origin_obj,
                           current_obj,
                           current_name: str,
                           obj_uid_to_meta: Dict[str, ControlItemMeta],
                           ignored_field_names: Optional[Set[str]] = None):
    res_node = mui.ControlNode(id=current_name,
                               name=current_name.split(".")[-1],
                               type=mui.ControlNodeType.Folder.value)
    if ignored_field_names is None:
        ignored_field_names = set()
    for f in dataclasses.fields(current_obj):
        if f.name in ignored_field_names:
            continue
        next_name = f.name
        if current_name:
            next_name = current_name + "." + f.name
        child_node = mui.ControlNode(id=next_name,
                                     name=f.name,
                                     type=mui.ControlNodeType.Folder.value)
        # meta: Optional[ConfigMeta] = None
        # if _CONFIG_META_KEY in f.metadata:
        #     meta = f.metadata[_CONFIG_META_KEY]
        ty = f.type
        if isinstance(ty, str):
            continue # ignore str type
        is_anno = is_annotated(ty)
        # ty_origin = get_origin(ty)
        annotated_metas = None
        if is_anno:
            annotated_metas = ty.__metadata__
            ty = get_args(ty)[0]
        ty_origin = get_origin(ty)
        # if f.name == "a":
        #     print(f.name, ty_origin, ty, type(ty), not _check_is_basic_type(ty) and ty not in _BUILTIN_DCLS_TYPE, annotated_metas)
        field_value = getattr(current_obj, f.name)
        if (dataclasses.is_dataclass(ty) or dataclasses.is_dataclass(field_value)) and ty not in _BUILTIN_DCLS_TYPE:
            res = parse_to_control_nodes(origin_obj,
                                         getattr(current_obj, f.name),
                                         next_name, obj_uid_to_meta)
            res_node.children.append(res)

            continue
        if not _check_is_basic_type(ty) and ty not in _BUILTIN_DCLS_TYPE:
            continue  # TODO add support for simple complex type
        # we support int/float/bool/str
        getter = partial(getattr_single, obj=current_obj, name=f.name)
        comparer = partial(compare_single, obj=current_obj, name=f.name)
        # if meta is not None and meta.alias is not None:
        #     child_node.alias = meta.alias
        # check anno meta first
        if annotated_metas is not None:
            first_anno_meta = annotated_metas[0]
            if isinstance(first_anno_meta,
                          (typemetas.ColorRGB, typemetas.ColorRGBA)):
                if isinstance(first_anno_meta, typemetas.ColorRGB):
                    child_node.type = mui.ControlNodeType.ColorRGB.value
                else:
                    child_node.type = mui.ControlNodeType.ColorRGBA.value
                val = getattr(current_obj, f.name)
                if not isinstance(val, mui.Undefined):
                    child_node.value = val
                else:
                    if first_anno_meta.default is not None:
                        child_node.value = first_anno_meta.default
                # child_node.value = getattr(current_obj, f.name)
                ty_valid_color = ty is str or ty is mui.ValueType
                if ty_origin is Union:
                    # handle "Union[..., Undefined]" in component props
                    union_args = get_args(ty)
                    if mui.Undefined in union_args:
                        union_args = tuple(x for x in union_args
                                           if x is not mui.Undefined)
                    if len(union_args) == 1:
                        ty_valid_color = union_args[0] is str or union_args[
                            0] is int
                    else:
                        # handle NumberType and ValueType in component props
                        union_args_set = set(union_args)
                        ty_valid_color = union_args_set == set([int, str])
                    # print(ty, ty_origin, ty_valid_color, "RTX")
                if ty_valid_color:
                    if first_anno_meta.value_is_string:
                        mapper = lambda x: "#{:02X}{:02X}{:02X}".format(
                            x["r"], x["g"], x["b"])
                    else:
                        mapper = lambda x: x["r"] << 16 | x["g"] << 8 | x["b"]
                    setter = partial(setattr_single,
                                     obj=current_obj,
                                     name=f.name,
                                     mapper=mapper)
                    comparer = partial(compare_single,
                                       obj=current_obj,
                                       name=f.name,
                                       mapper=mapper)
                    res_node.children.append(child_node)
                    obj_uid_to_meta[child_node.id] = ControlItemMeta(
                        getter, setter, comparer)
                    continue
            elif isinstance(first_anno_meta,
                            (typemetas.RangedVector3, typemetas.Vector3, typemetas.RangedVector2, typemetas.Vector2)):
                child_node.type = mui.ControlNodeType.VectorN.value
                child_node.count = 3 if isinstance(first_anno_meta, (typemetas.RangedVector3, typemetas.Vector3)) else 2
                val = getattr(current_obj, f.name)
                if not isinstance(val, mui.Undefined):
                    if isinstance(val, (int, float)):
                        val = (val, val, val)
                    # TODO validate val
                    child_node.value = val
                else:
                    if first_anno_meta.default is not None:
                        child_node.value = list(first_anno_meta.default)
                if isinstance(first_anno_meta, (typemetas.RangedVector3, typemetas.RangedVector2)):
                    child_node.min = first_anno_meta.lo
                    child_node.max = first_anno_meta.hi
                child_node.step = mui.undefined if first_anno_meta.step is None else first_anno_meta.step
                child_node.alias = mui.undefined if first_anno_meta.alias is None else first_anno_meta.alias

                setter = partial(setattr_vector_n_tuple,
                                 obj=current_obj,
                                 name=f.name,
                                 count=child_node.count,
                                 default=first_anno_meta.default)
                comparer = partial(compare_vector_n_tuple,
                                   obj=current_obj,
                                   name=f.name)
                res_node.children.append(child_node)
                obj_uid_to_meta[child_node.id] = ControlItemMeta(
                    getter, setter, comparer)
                continue
            elif (isinstance(first_anno_meta,
                             (typemetas.RangedInt, typemetas.RangedFloat))
                  and _check_union_is_valid_subset_ignore_undefined(
                      ty, ty_origin, set([int, float]))):
                res = _parse_base_type(ty, current_obj, f.name, child_node)
                if res is not None:
                    child_node.type = mui.ControlNodeType.RangeNumber.value
                    if first_anno_meta.default is not None:
                        if isinstance(child_node.value, mui.Undefined):
                            child_node.value = first_anno_meta.default
                    child_node.min = first_anno_meta.lo
                    child_node.max = first_anno_meta.hi
                    child_node.isInteger = isinstance(first_anno_meta,
                                                      typemetas.RangedInt)
                    child_node.alias = mui.undefined if first_anno_meta.alias is None else first_anno_meta.alias
                    child_node.step = mui.undefined if first_anno_meta.step is None else first_anno_meta.step
                    if first_anno_meta.step is None and ty is int:
                        child_node.step = 1
                    res_node.children.append(child_node)
                    obj_uid_to_meta[child_node.id] = res
                    continue
            elif isinstance(first_anno_meta, (typemetas.Enum)):
                res = _parse_base_type(ty, current_obj, f.name, child_node)
                if res is not None and issubclass(ty, (enum.Enum, enum.IntEnum)):
                    if first_anno_meta.alias is not None:
                        child_node.alias = first_anno_meta.alias
                    if first_anno_meta.excludes is not None:
                        child_node.selects = list((x.name, x.value) for x in ty if x not in first_anno_meta.excludes)
                    res_node.children.append(child_node)
                    obj_uid_to_meta[child_node.id] = res
                    continue

            elif isinstance(first_anno_meta, (typemetas.CommonObject)):
                res = _parse_base_type(ty, current_obj, f.name, child_node)
                if res is not None:
                    if first_anno_meta.alias is not None:
                        child_node.alias = first_anno_meta.alias
                    if first_anno_meta.default is not None:
                        if isinstance(child_node.value, mui.Undefined):
                            child_node.value = first_anno_meta.default
                    res_node.children.append(child_node)
                    obj_uid_to_meta[child_node.id] = res
                    continue

        # type don't have anno meta, or invalid meta, use base types
        res = _parse_base_type(ty, current_obj, f.name, child_node)
        if res is not None:
            res_node.children.append(child_node)
            obj_uid_to_meta[child_node.id] = res
            continue

    return res_node


def control_nodes_v1_to_v2(
        ctrl_node_v1: mui.ControlNode,
        uid_to_json_like_node: Dict[str,
                                    mui.JsonLikeNode]) -> mui.JsonLikeNode:
    childs: List[mui.JsonLikeNode] = [
        control_nodes_v1_to_v2(c, uid_to_json_like_node)
        for c in ctrl_node_v1.children
    ]
    ctrl_desp = mui.SimpleControlsItem(type=ctrl_node_v1.type,
                                value=ctrl_node_v1.value,
                                min=ctrl_node_v1.min,
                                max=ctrl_node_v1.max,
                                step=ctrl_node_v1.step,
                                selects=ctrl_node_v1.selects,
                                rows=ctrl_node_v1.rows,
                                count=ctrl_node_v1.count,
                                isInteger=ctrl_node_v1.isInteger)
    node = mui.JsonLikeNode(
        id=UniqueTreeIdForTree.from_parts(ctrl_node_v1.id.split(".")),
        name=ctrl_node_v1.name if isinstance(
            ctrl_node_v1.alias, mui.Undefined) else ctrl_node_v1.alias,
        type=mui.JsonLikeType.Object.value,
        typeStr="",
        children=childs,
        userdata=ctrl_desp)
    uid_to_json_like_node[node.id.uid_encoded] = node
    return node


class ConfigPanel(mui.SimpleControls):

    def __init__(self,
                 config_obj: Any,
                 callback: Optional[Callable[[str, Any],
                                             mui._CORO_NONE]] = None,
                 ignored_field_names: Optional[Set[str]] = None):
        assert dataclasses.is_dataclass(config_obj)
        # parse config dataclass.
        items, self._obj_to_ctrl_meta, self.uid_to_json_like_node = self._get_controls_tree(
            config_obj)
        super().__init__(init=items,
                         callback=self.callback)
        self.__config_obj = config_obj
        self.__callback_key = "config_panel_v3_handler"
        if callback is not None:
            self.register_event_handler(self.__callback_key,
                                        callback,
                                        backend_only=True)

    def _get_controls_tree(self, cfg: Any):
        # parse config dataclass.
        _obj_to_ctrl_meta = {}
        uid_to_json_like_node = {}
        node = parse_to_control_nodes(cfg, cfg, "", _obj_to_ctrl_meta)
        node_v2 = control_nodes_v1_to_v2(
            node, uid_to_json_like_node)
        return node_v2.children, _obj_to_ctrl_meta, uid_to_json_like_node

    async def callback(self, value: Tuple[str, Any]):
        uid = value[0]
        uid_obj = UniqueTreeIdForTree(uid)
        uid_dot_split = ".".join(uid_obj.parts)
        cmeta = self._obj_to_ctrl_meta[uid_dot_split]
        compare_res = cmeta.compare(value[1])
        if not compare_res:
            # here we need to compare value, emit event iff
            # the value is changed.
            # TODO this is due to limitation of leva control.
            # we may need to write own dynamic control
            # based on tanstack table.
            assert uid in self.uid_to_json_like_node
            userdata = self.uid_to_json_like_node[uid].userdata
            assert isinstance(userdata, mui.SimpleControlsItem)
            cmeta.setter(value[1])
            userdata.value = value[1]
            handlers = self.get_event_handlers(self.__callback_key)
            if handlers is not None:
                for handler in handlers.handlers:
                    coro = handler.cb(uid_dot_split, cmeta.getter())
                    if inspect.iscoroutine(coro):
                        await coro

    async def set_config_object(self, cfg: Any):
        if not isinstance(self.props.controlled, mui.Undefined) and not self.props.controlled:
            raise ValueError("you must use controlled simple control to use set_config_object")
        items, self._obj_to_ctrl_meta, self.uid_to_json_like_node = self._get_controls_tree(
            cfg)
        await self.send_and_wait(self.update_event(tree=items))

    @property
    def config(self):
        return self.__config_obj

    @staticmethod
    def base_meta(alias: Optional[str] = None):
        return {_CONFIG_META_KEY: ConfigMeta(alias)}

    @staticmethod
    def switch_meta(alias: Optional[str] = None):
        return {_CONFIG_META_KEY: SwitchMeta(alias)}

    @staticmethod
    def input_meta(multiline: bool,
                   rows: int,
                   font_size: mui.ValueType,
                   font_family: str,
                   alias: Optional[str] = None):
        return {
            _CONFIG_META_KEY:
            InputMeta(alias=alias,
                      multiline=multiline,
                      rows=rows,
                      font_size=font_size,
                      font_family=font_family)
        }

    @staticmethod
    def slider_meta(begin: mui.NumberType,
                    end: mui.NumberType,
                    step: Optional[mui.NumberType] = None,
                    alias: Optional[str] = None):
        return {
            _CONFIG_META_KEY:
            SliderMeta(begin=begin, end=end, step=step, alias=alias)
        }

@dataclasses.dataclass
class ConfigDialogEvent(Generic[T]):
    cfg: T 
    userdata: Any = None


class ConfigPanelDialog(mui.Dialog, Generic[T]):
    def __init__(self, callback: Callable[[ConfigDialogEvent[T]], mui._CORO_NONE], children: Optional[mui.LayoutType] = None):
        self._content = mui.VBox([

        ]).prop(flex=1)
        
        super().__init__([] if children is None else children, self._on_dialog_close)
        # save callback to standard flow event handlers to enable reload for user callback
        self.__callback_key = "_config_panel_dialog_ev_handler"
        self.__layout_key = "__tensorpc_config_dialog_panel"
        self.register_event_handler(self.__callback_key,
                                    callback,
                                    backend_only=True)

        self._cur_cfg: Optional[T] = None
        self._cur_user_data: Any = None

    async def open_config_dialog(self, config_obj: T, userdata: Any = None):
        assert dataclasses.is_dataclass(config_obj) and not isinstance(config_obj, type), "config_obj should be a dataclass"
        config_obj = dataclasses.replace(config_obj)
        self._cur_cfg = config_obj
        self._cur_user_data = userdata
        panel = ConfigPanel(config_obj)
        await self.update_childs({
            self.__layout_key: panel,
        }, post_ev_creator=lambda: self.update_event(open=True)) 

    async def _on_dialog_close(self, ev: mui.DialogCloseEvent):
        assert self._cur_cfg is not None, "shouldn't happen"
        handlers = self.get_event_handlers(self.__callback_key)
        try:
            if handlers is not None and ev.ok:
                for handler in handlers.handlers:
                    coro = handler.cb(ConfigDialogEvent(self._cur_cfg, self._cur_user_data))
                    if inspect.iscoroutine(coro):
                        await coro
        finally:
            self._cur_cfg = None
            self._cur_user_data = None
            await self.remove_childs_by_keys([self.__layout_key])

class ConfigPanelDialogPersist(mui.Dialog, Generic[T]):
    def __init__(self, cfg: T, callback: Callable[[ConfigDialogEvent[T]], mui._CORO_NONE], children: Optional[mui.LayoutType] = None):
        self._config = ConfigPanel(cfg)
        super().__init__([
            mui.HBox([
                self._config
            ]).prop(flex=1, overflow="auto")
        ], self._on_dialog_close)
        if children is not None:
            self.init_add_layout(children)
        # save callback to standard flow event handlers to enable reload for user callback
        self.__callback_key = "_config_panel_dialog_ev_handler"
        self.register_event_handler(self.__callback_key,
                                    callback,
                                    backend_only=True)
        assert dataclasses.is_dataclass(cfg) and not isinstance(cfg, type), "config_obj should be a dataclass"
        self.prop(display="flex", flexDirection="column", overflow="hidden")
        self._cur_cfg: T = cfg
        self._cur_user_data: Any = None

    @property
    def config(self):
        return self._cur_cfg

    async def open_config_dialog(self, userdata: Any = None, inplace: bool = True):
        config_obj = self._cur_cfg
        if not inplace:
            assert dataclasses.is_dataclass(config_obj) and not isinstance(config_obj, type), "config_obj should be a dataclass"
            config_obj = dataclasses.replace(config_obj)
            self._cur_cfg = config_obj
            await self._config.set_config_object(config_obj)
        self._cur_user_data = userdata
        await self.set_open(True)

    async def _on_dialog_close(self, ev: mui.DialogCloseEvent):
        handlers = self.get_event_handlers(self.__callback_key)
        if handlers is not None and ev.ok:
            for handler in handlers.handlers:
                coro = handler.cb(ConfigDialogEvent(self._cur_cfg, self._cur_user_data))
                if inspect.iscoroutine(coro):
                    await coro

    async def set_config_object(self, cfg: T):
        assert dataclasses.is_dataclass(cfg) and not isinstance(cfg, type), "config_obj should be a dataclass"
        self._cur_cfg = cfg
        await self._config.set_config_object(cfg)
