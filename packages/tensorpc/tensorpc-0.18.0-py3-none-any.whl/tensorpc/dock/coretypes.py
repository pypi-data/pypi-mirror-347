import enum

from pathlib import Path
from typing import (TYPE_CHECKING, Any, AsyncGenerator, Awaitable, Callable,
                    Coroutine, Dict, Generic, Iterable, List, Optional, Set,
                    Tuple, Type, TypeVar, Union)
from tensorpc.autossh.core import Event, event_from_dict
from tensorpc.core import dataclass_dispatch
from tensorpc.core.moduleid import get_qualname_of_type
from .jsonlike import JsonLikeNode, as_dict_no_undefined, Undefined, undefined
import dataclasses


def get_unique_node_id(graph_id: str, node_id: str):
    return f"{graph_id}@{node_id}"

def split_unique_node_id(node_uid: str):
    gid, nid = node_uid.split("@")
    return gid, nid

@dataclasses.dataclass
class StorageMeta:
    path_fmt: str

class StorageType(enum.IntEnum):
    JSON = 0
    RAW = 1
    JSONARRAY = 2
    # DEPRECATED
    PICKLE_DEPRECATED = -1


class StorageDataItem:

    def __init__(self, data: Union[bytes, bytearray], meta: JsonLikeNode) -> None:
        self.data = data
        self.meta = meta
        assert not isinstance(self.meta.userdata, Undefined)

    def empty(self):
        return len(self.data) == 0

    @property
    def timestamp(self):
        assert not isinstance(self.meta.userdata, Undefined)
        return self.meta.userdata["timestamp"]

    def __len__(self):
        return len(self.data)

    def get_meta_dict(self):
        return as_dict_no_undefined(self.meta)

    @property
    def storage_type(self):
        assert not isinstance(self.meta.userdata, Undefined)
        return StorageType(self.meta.userdata.get("type", StorageType.PICKLE_DEPRECATED.value))

    @property
    def version(self):
        assert not isinstance(self.meta.userdata, Undefined)
        return self.meta.userdata.get("version", 1)

    def shallow_copy(self):
        return StorageDataItem(self.data, self.meta)

class StorageDataLoadedItem:

    def __init__(self, data: Any, meta: JsonLikeNode) -> None:
        self.data = data
        self.meta = meta
        assert not isinstance(self.meta.userdata, Undefined)

    @property
    def timestamp(self):
        assert not isinstance(self.meta.userdata, Undefined)
        return self.meta.userdata["timestamp"]

    def get_meta_dict(self):
        return as_dict_no_undefined(self.meta)

    def shallow_copy(self):
        return StorageDataLoadedItem(self.data, self.meta)

class MessageItemType(enum.Enum):
    Text = 0
    Image = 1


class MessageLevel(enum.Enum):
    Info = 0
    Warning = 1
    Error = 2


class MessageItem:

    def __init__(self, type: MessageItemType, data: Any) -> None:
        self.type = type
        self.data = data

    def to_dict(self):
        return {
            "type": self.type.value,
            "data": self.data,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(MessageItemType(data["type"]), data["data"])


class Message:

    def __init__(self, uid: str, level: MessageLevel, timestamp: int,
                 graph_id: str, node_id: str, title: str,
                 items: List[MessageItem]) -> None:
        self.uid = uid
        self.title = title
        self.items = items
        self.timestamp = timestamp
        self.graph_id = graph_id
        self.node_id = node_id
        self.level = level

    def get_node_uid(self):
        return get_unique_node_id(self.graph_id, self.node_id)

    def __hash__(self) -> int:
        return hash(self.uid)

    def to_dict(self, with_detail: bool = False):
        res = {
            "uid": self.uid,
            "level": self.level.value,
            "nodeId": self.node_id,
            "graphId": self.graph_id,
            "ts": self.timestamp,
            "title": self.title,
            "items": []
        }
        if with_detail:
            res["items"] = [n.to_dict() for n in self.items]
        return res

    def to_dict_with_detail(self):
        return self.to_dict(True)

    @classmethod
    def from_dict(cls, data):
        return cls(data["uid"], MessageLevel(data["level"]), data["ts"],
                   data["graphId"], data["nodeId"], data["title"],
                   [MessageItem.from_dict(it) for it in data["items"]])


class MessageEventType(enum.Enum):
    Update = "Update"
    Replace = "Replace"


class MessageEvent:

    def __init__(self, type: MessageEventType, rawmsgs: List[Any]) -> None:
        self.type = type
        self.rawmsgs = rawmsgs

    def to_dict(self):
        return {
            "type": self.type.value,
            "msgs": self.rawmsgs,
        }


class UserEventType(enum.Enum):
    """user event: event come from user code instead of
    ssh.
    for example:
    1. node call api to update content
        of a command node.
    2. node submit a message
    3. node submit a new status (currently
        only come from master server)
    """
    Status = 0
    Content = 1
    Message = 2
    DataUpdate = 3


class UserEvent:

    def __init__(self, type: UserEventType):
        self.type = type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
        }


class SessionStatus(enum.Enum):
    Running = 0
    Stop = 1


class UserStatusEvent(UserEvent):
    ALL_STATUS = set(["idle", "running", "error", "success"])

    def __init__(self, status: str, session_status: SessionStatus):
        super().__init__(UserEventType.Status)
        assert status in self.ALL_STATUS
        self.status = status
        self.session_status = session_status

    def to_dict(self):
        res = super().to_dict()
        res["status"] = self.status
        res["sessionStatus"] = self.session_status.value
        return res

    @staticmethod
    def empty():
        return UserStatusEvent("idle", SessionStatus.Stop)


class UserContentEvent(UserEvent):

    def __init__(self, content: Any):
        super().__init__(UserEventType.Content)
        self.content = content

    def to_dict(self):
        res = super().to_dict()
        res["content"] = self.content
        return res


class UserDataUpdateEvent(UserEvent):

    def __init__(self, content: Any):
        super().__init__(UserEventType.DataUpdate)
        self.content = content

    def to_dict(self):
        res = super().to_dict()
        res["update"] = self.content
        return res


class ScheduleEvent:

    def __init__(self, timestamp: int, data: Any, envs: Dict[str,
                                                             Any]) -> None:
        self.data = data
        self.timestamp = timestamp
        self.envs = envs

    def to_dict(self):
        return {
            "ts": self.timestamp,
            "data": self.data,
            "envs": self.envs,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["ts"], data["data"], data["envs"])

