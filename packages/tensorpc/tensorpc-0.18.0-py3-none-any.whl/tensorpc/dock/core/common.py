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

from functools import partial
from typing import Any, Tuple, Union
import asyncio
from tensorpc.dock.core.component import Component, Event, create_ignore_usr_msg, Undefined, UIRunStatus, FrontendEventType, ALL_POINTER_EVENTS, LOGGER

_STATE_CHANGE_EVENTS = set([
    FrontendEventType.Change.value,
    FrontendEventType.InputChange.value,
    FrontendEventType.ModalClose.value,
    FrontendEventType.TreeItemSelectChange.value,
    FrontendEventType.TreeItemExpandChange.value,
])

_ONEARG_KEYBOARD_EVENTS = set([
    FrontendEventType.KeyHold.value,
    FrontendEventType.KeyDown.value,
    FrontendEventType.KeyUp.value,
])

_ONEARG_TREE_EVENTS = set([
    FrontendEventType.TreeItemSelectChange.value,
    FrontendEventType.TreeItemExpandChange.value,
    FrontendEventType.TreeItemToggle.value,
    FrontendEventType.TreeLazyExpand.value,
    FrontendEventType.TreeItemFocus.value,
    FrontendEventType.TreeItemButton.value,
    FrontendEventType.ContextMenuSelect.value,
    FrontendEventType.TreeItemRename.value,
])

_ONEARG_COMPLEXL_EVENTS = set([
    FrontendEventType.ComplexLayoutCloseTab.value,
    FrontendEventType.ComplexLayoutSelectTab.value,
    FrontendEventType.ComplexLayoutTabReload.value,
    FrontendEventType.ComplexLayoutSelectTabSet.value,
    FrontendEventType.ComplexLayoutStoreModel.value,
])

_ONEARG_EDITOR_EVENTS = set([
    FrontendEventType.EditorSave.value,
    FrontendEventType.EditorSaveState.value,
    FrontendEventType.EditorAction.value,
    FrontendEventType.EditorCursorSelection.value,
])

_ONEARG_SPECIAL_EVENTS = set([
    FrontendEventType.Drop.value,
    FrontendEventType.SelectNewItem.value,
    FrontendEventType.FlowSelectionChange.value,
    FrontendEventType.FlowNodesInitialized.value,
    FrontendEventType.FlowNodeDelete.value,
    FrontendEventType.FlowEdgeConnection.value,
    FrontendEventType.FlowEdgeDelete.value,
    FrontendEventType.FlowNodeContextMenu.value,
    FrontendEventType.FlowPaneContextMenu.value,
    FrontendEventType.FlowNodeLogicChange.value, 
    FrontendEventType.FlowVisChange.value, 

    

])

_ONEARG_DATAGRID_EVENTS = set([
    FrontendEventType.DataGridRowSelection.value,
    FrontendEventType.DataGridFetchDetail.value,
    FrontendEventType.DataGridRowRangeChanged.value,
    FrontendEventType.DataGridProxyLazyLoadRange.value,

    FrontendEventType.DataBoxSecondaryActionClick.value,
])

_ONEARG_TERMINAL_EVENTS = set([
    FrontendEventType.TerminalInput.value,
    FrontendEventType.TerminalResize.value,
    FrontendEventType.TerminalFrontendUnmount.value,
    FrontendEventType.TerminalFrontendMount.value,
])

_ONEARG_EVENTS = set(
    ALL_POINTER_EVENTS
) | _ONEARG_TREE_EVENTS | _ONEARG_COMPLEXL_EVENTS | _ONEARG_SPECIAL_EVENTS | _ONEARG_EDITOR_EVENTS
_ONEARG_EVENTS = _ONEARG_EVENTS | _ONEARG_DATAGRID_EVENTS | _ONEARG_TERMINAL_EVENTS | _ONEARG_KEYBOARD_EVENTS

_NOARG_EVENTS = set([
    FrontendEventType.Click.value,
    FrontendEventType.ComponentReady.value,
    FrontendEventType.DoubleClick.value,
    FrontendEventType.EditorQueryState.value,
    FrontendEventType.Delete.value,
])

async def handle_raw_event(event: Event,
                           comp: Component,
                           just_run: bool = False,
                           capture_draft: bool = True):
    # ev: [type, data]
    type = event.type
    data = event.data
    handlers = comp.get_event_handlers(event.type)
    if handlers is None:
        return
    if comp._flow_comp_status == UIRunStatus.Running.value:
        msg = create_ignore_usr_msg(comp)
        await comp.send_and_wait(msg)
        return
    elif comp._flow_comp_status == UIRunStatus.Stop.value:
        comp.state_change_callback(data, type)
        run_funcs = handlers.get_bind_event_handlers(event)
        if not just_run:
            comp._task = asyncio.create_task(
                comp.run_callbacks(run_funcs, True, capture_draft=capture_draft))
        else:
            return await comp.run_callbacks(run_funcs, True, capture_draft=capture_draft)


async def handle_standard_event(comp: Component,
                                event: Event,
                                sync_status_first: bool = False,
                                sync_state_after_change: bool = True,
                                is_sync: bool = False,
                                change_status: bool = True,
                                capture_draft: bool = True):
    """ common event handler
    """
    # print("WTF", event.type, event.data, comp._flow_comp_status)
    if comp._flow_comp_status == UIRunStatus.Running.value:
        flowuid = comp._flow_uid
        if flowuid is not None:
            LOGGER.warning("Component (%s) %s is running, ignore user event %s", type(comp).__name__, flowuid, event.type)
        else:
            LOGGER.warning("Component (%s) is running, ignore user event %s", type(comp).__name__, event.type)
        # msg = create_ignore_usr_msg(comp)
        # await comp.send_and_wait(msg)
        return
    elif comp._flow_comp_status == UIRunStatus.Stop.value:
        if not isinstance(event.keys, Undefined):
            # for all data model components, we must disable
            # status change and sync. status indicator
            # in Button and IconButton will be disabled.
            sync_status_first = False
            change_status = False
        # print("WTF2x", event.type, event.data)

        if event.type in _STATE_CHANGE_EVENTS:
            # print("WTF2", event.type, event.data)

            handlers = comp.get_event_handlers(event.type)
            sync_state = False
            # for data model components, we don't need to sync state.
            if isinstance(event.keys, Undefined):
                comp.state_change_callback(event.data, event.type)
                sync_state = sync_state_after_change
            if handlers is not None:
                # state change events must sync state after callback
                if is_sync:
                    return await comp.run_callbacks(
                        handlers.get_bind_event_handlers(event),
                        sync_state,
                        sync_status_first=False,
                        change_status=change_status,
                        capture_draft=capture_draft)
                else:
                    comp._task = asyncio.create_task(
                        comp.run_callbacks(
                            handlers.get_bind_event_handlers(event),
                            sync_state,
                            sync_status_first=sync_status_first,
                            change_status=change_status,
                            capture_draft=capture_draft))
            else:
                # all controlled component must sync state after state change
                if sync_state_after_change:
                    await comp.sync_status(sync_state)
        elif event.type in _NOARG_EVENTS:
            handlers = comp.get_event_handlers(event.type)
            # other events don't need to sync state
            if handlers is not None:
                run_funcs = handlers.get_bind_event_handlers_noarg(event)
                if is_sync:
                    return await comp.run_callbacks(run_funcs,
                                                    sync_status_first=False,
                                                    capture_draft=capture_draft)
                else:
                    comp._task = asyncio.create_task(
                        comp.run_callbacks(run_funcs,
                                           sync_status_first=sync_status_first,
                                           change_status=change_status,
                                           capture_draft=capture_draft))
        elif event.type in _ONEARG_EVENTS:
            handlers = comp.get_event_handlers(event.type)
            # other events don't need to sync state
            if handlers is not None:
                run_funcs = handlers.get_bind_event_handlers(event)
                if is_sync:
                    return await comp.run_callbacks(
                        run_funcs,
                        sync_status_first=False,
                        change_status=change_status,
                        capture_draft=capture_draft)
                else:
                    comp._task = asyncio.create_task(
                        comp.run_callbacks(run_funcs,
                                           sync_status_first=sync_status_first,
                                           change_status=change_status,
                                           capture_draft=capture_draft))

        else:
            raise NotImplementedError


# async def handle_change_event_no_arg(comp: Component, sync_status_first: bool = False):
#     if comp._flow_comp_status == UIRunStatus.Running.value:
#         msg = create_ignore_usr_msg(comp)
#         await comp.send_and_wait(msg)
#         return
#     elif comp._flow_comp_status == UIRunStatus.Stop.value:
#         cb2 = comp.get_callback()
#         if cb2 is not None:
#             comp._task = asyncio.create_task(comp.run_callback(cb2, sync_status_first=sync_status_first))
