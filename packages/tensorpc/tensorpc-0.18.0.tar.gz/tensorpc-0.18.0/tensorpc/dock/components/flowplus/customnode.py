import contextlib
import dataclasses
import inspect
from pathlib import Path
from re import M
import sys
import traceback
import types
from typing import Any, Dict, Optional, Type
import uuid

from tensorpc.constants import TENSORPC_FILE_NAME_PREFIX

from .compute import FLOWUI_CNODE_NODEDATA_KEY, ComputeFlow, NodeSideLayoutOptions, ComputeNode, ComputeNodeWrapper, NodeConfig, ReservedNodeTypes, WrapperConfig, enter_flow_ui_context_object, get_compute_flow_context, register_compute_node, get_cflow_shared_node_key

from tensorpc.dock.components import flowui, mui
from tensorpc.dock.appctx import read_data_storage, save_data_storage, find_all_components

_MEDIA_ROOT = Path(__file__).parent / "media"

class CustomNodeEditorActionNames:
    CreateTemplate = "Make Shared"
    DetachFromTemplate = "Detach From Shared"
    RunCached = "Run Cached Node"

@dataclasses.dataclass
class ModuleWithCode:
    module: types.ModuleType
    code: str

@register_compute_node(key=ReservedNodeTypes.Custom, name="Custom Node", icon_cfg=mui.IconProps(icon=mui.IconType.Code))
class CustomNode(ComputeNode):
    def init_node(self):
        self.is_dynamic_class = True # affect annotation parse
        base_code_path = _MEDIA_ROOT / "customnode_base.py"
        with open(base_code_path, "r") as f:
            base_code = f.read()
        self._base_code = base_code
        self._init_custom_node()

    def _init_custom_node(self):
        actions = [
            mui.MonacoEditorAction(id=CustomNodeEditorActionNames.CreateTemplate, 
                label="Make Node Shared", contextMenuGroupId="tensorpc-flow-editor-action", contextMenuOrder=1.5),
            mui.MonacoEditorAction(id=CustomNodeEditorActionNames.DetachFromTemplate,
                label="Detach From Shared", contextMenuGroupId="tensorpc-flow-editor-action", contextMenuOrder=1.5),
            mui.MonacoEditorAction(id=CustomNodeEditorActionNames.RunCached,
                label="Run with Cached Inputs", keybindings=[([mui.MonacoKeyMod.Shift], 3)],
                contextMenuGroupId="tensorpc-flow-editor-action", contextMenuOrder=1.5)
        ]
        self._code_editor = mui.MonacoEditor(self._base_code, "python",
                                             f"<tensorpc-flow-cflow-{self.id}>").prop(flex=1, actions=actions)
        self._shared_key: Optional[str] = None
        self._module: Optional[ModuleWithCode] = None

        self._cnode = self._get_cnode_cls_from_code(self._base_code)
        self._code_editor.event_editor_save.on(self.handle_code_editor_save)
        self._code_editor.event_editor_action.on(self._handle_editor_action)
        self._disable_template_fetch: bool = False
        self._side_container = mui.VBox([]).prop(width="100%",
                                      height="100%")
        self._setting_template_name = mui.TextField("Shared Node Name")
        self._setting_dialog = mui.Dialog(
            [self._setting_template_name], lambda x: self._create_shared(self._setting_template_name.str())
            if x.ok else None)

    @property
    def icon_cfg(self):
        if self._shared_key is not None:
            return mui.IconProps(icon=mui.IconType.Code, muiColor="primary")
        else:
            return mui.IconProps(icon=mui.IconType.Code)

    @property 
    def init_cfg(self):
        return self._cnode.init_cfg

    @property
    def init_wrapper_config(self) -> Optional[WrapperConfig]:
        return self._cnode.init_wrapper_config

    async def init_node_async(self, is_node_mounted: bool):
        await self._cnode.init_node_async(is_node_mounted)
        if not self._disable_template_fetch:
            if self._shared_key is not None:
                template_code = await read_data_storage(
                    get_cflow_shared_node_key(self._shared_key),
                    raise_if_not_found=False)
                if template_code is not None:
                    try:
                        cnode = self._get_cnode_cls_from_code(template_code)
                        if is_node_mounted:
                            await self.handle_code_editor_save(
                                template_code,
                                update_editor=True,
                                check_template_key=False)
                        else:
                            self._cnode = cnode
                            self._code_editor.prop(value=template_code)
                    except Exception as e:
                        # ignore exception here because node will be removed if exception during
                        # ComputeFlow mounting
                        traceback.print_exc()

    @contextlib.contextmanager
    def disable_template_fetch(self):
        try:
            self._disable_template_fetch = True
            yield
        finally:
            self._disable_template_fetch = False

    def _get_cnode_cls_from_code(self, code: str):
        key = f"{TENSORPC_FILE_NAME_PREFIX}-cflow-node-{self.id}"
        mod_name = f"<{key}-{uuid.uuid4().hex}>"
        module = types.ModuleType(mod_name)
        module.__file__ = f"<{key}>"
        self._module = ModuleWithCode(module, code)
        codeobj = compile(code,  module.__file__, "exec")
        exec(codeobj, module.__dict__)
        cnode_cls: Optional[Type[ComputeNode]] = None
        for v in module.__dict__.values():
            if inspect.isclass(v) and v is not ComputeNode and issubclass(
                    v, ComputeNode):
                cnode_cls = v
                break
        assert cnode_cls is not None, f"can't find any class that inherit ComputeNode in your code!"
        cnode = cnode_cls(self.id, self.name, self._node_type, self._init_cfg, self._init_pos)
        return cnode

    async def handle_code_editor_save(self,
                                      save_ev: mui.MonacoEditorSaveEvent,
                                      update_editor: bool = False,
                                      check_template_key: bool = True):
        value = save_ev.value
        ctx = get_compute_flow_context()
        assert ctx is not None, "can't find compute flow context!"
        new_cnode = self._get_cnode_cls_from_code(value)
        self._cnode = new_cnode
        if self._shared_key is not None and check_template_key:
            # update all nodes that use this template
            await save_data_storage(
                get_cflow_shared_node_key(self._shared_key), value)
            all_cflows = find_all_components(ComputeFlow)
            for cflow in all_cflows:
                with enter_flow_ui_context_object(cflow.graph_ctx):
                    for node in cflow.graph.nodes:
                        wrapper = node.get_component_checked(
                            ComputeNodeWrapper)
                        if isinstance(
                                wrapper.cnode,
                                CustomNode) and wrapper.cnode is not self:
                            if wrapper.cnode._shared_key == self._shared_key:
                                await wrapper.cnode.handle_code_editor_save(
                                    save_ev,
                                    update_editor=True,
                                    check_template_key=False)
        with self.disable_template_fetch():
            # update_cnode will call init_node_async
            await ctx.cflow.update_cnode(self.id, self)
        if update_editor:
            if self._code_editor.is_mounted():
                await self._code_editor.send_and_wait(
                    self._code_editor.update_event(value=value))
            else:
                self._code_editor.prop(value=value)

    @property
    def is_async_gen(self):
        return inspect.isasyncgenfunction(self._cnode.compute)

    async def detach_from_template(self):
        if self._shared_key is not None:
            ctx = get_compute_flow_context()
            assert ctx is not None, "can't find compute flow context!"
            self._shared_key = None
            await ctx.cflow.update_cnode_icon_cfg(self.id, self.icon_cfg)
            await ctx.cflow.update_templates()

    async def _handle_editor_action(self, act_ev: mui.MonacoEditorActionEvent):
        act = act_ev.action
        if act == CustomNodeEditorActionNames.CreateTemplate:
            await self._setting_dialog.put_app_event(self._setting_template_name.update_event(value=self.name))
            await self._setting_dialog.set_open(True)
        elif act == CustomNodeEditorActionNames.DetachFromTemplate:
            await self.detach_from_template()
        elif act == CustomNodeEditorActionNames.RunCached:
            ctx = get_compute_flow_context()
            assert ctx is not None, "can't find compute flow context!"
            await ctx.cflow.run_cached_node(self.id)

    def _get_side_layouts(self):
        layouts: mui.LayoutType = {
            "dialog": self._setting_dialog,
            f"editor-{self.id}": self._code_editor,
        }
        return layouts

    def get_side_layout(self) -> Optional[mui.FlexBox]:
        layouts = self._get_side_layouts()
        self._side_container = mui.VBox(layouts).prop(width="100%",
                                      height="100%",
                                      overflow="hidden")
        self._side_container.set_user_meta_by_type(NodeSideLayoutOptions(vertical=True))
        return self._side_container

    async def _create_shared(self, template_key: str):
        if self._shared_key is None:
            ctx = get_compute_flow_context()
            assert ctx is not None, "can't find compute flow context!"
            await save_data_storage(get_cflow_shared_node_key(template_key),
                                    self._code_editor.props.value,
                                    raise_if_exist=True)
            self._shared_key = template_key
            # use new icon color to indicate template node
            await ctx.cflow.update_cnode_header(self.id, template_key)
            await ctx.cflow.update_cnode_icon_cfg(self.id, self.icon_cfg)
            await ctx.cflow.update_templates()
            if self._side_container.is_mounted():
                # update side layout if is mounted
                await self._side_container.set_new_layout({**self._get_side_layouts()})
        else:
            if self._side_container.is_mounted():
                await self._side_container.send_error("Template already created!", self.name)

    def get_node_layout(self) -> Optional[mui.FlexBox]:
        return self._cnode.get_node_layout()

    def state_dict(self) -> Dict[str, Any]:
        res = self._cnode.state_dict()
        this_state_dict = super().state_dict()
        # internal data use this
        res[FLOWUI_CNODE_NODEDATA_KEY] = this_state_dict[FLOWUI_CNODE_NODEDATA_KEY]
        res["__custom_node_code"] = self._code_editor.props.value
        res["__template_key"] = self._shared_key
        return res

    def get_compute_annotation(self):
        return self._cnode.get_compute_annotation()

    def get_compute_function(self):
        return self._cnode.get_compute_function()

    @classmethod
    async def from_state_dict(cls, data: Dict[str, Any]):
        res = ComputeNode.from_state_dict_default(data, cls)
        try:
            res._cnode = res._get_cnode_cls_from_code(data["__custom_node_code"])
        except:
            traceback.print_exc()
            res._cnode = res._get_cnode_cls_from_code(res._base_code)
        res._code_editor.prop(value=data["__custom_node_code"])
        res._shared_key = data["__template_key"]
        return res


@register_compute_node(key=ReservedNodeTypes.AsyncGenCustom, name="Async Gen Custom Node", icon_cfg=mui.IconProps(icon=mui.IconType.Code))
class AsyncGenCustomNode(CustomNode):
    def init_node(self):
        base_code_path = _MEDIA_ROOT / "asynccustom_base.py"
        with open(base_code_path, "r") as f:
            base_code = f.read()
        self._init_custom_node()
