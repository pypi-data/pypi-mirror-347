import dataclasses
import enum
import gzip
from os import stat_result

from mashumaro.mixins.yaml import DataClassYAMLMixin
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union, Any
from pathlib import Path
import base64
import json

from tensorpc.constants import TENSORPC_SPLIT


@dataclass
class Service(DataClassYAMLMixin):
    module_name: str
    config: Dict[str, Any]


@dataclass
class ServiceDef(DataClassYAMLMixin):
    services: List[Service]


class DynamicEvent:

    def __init__(self, name: str, data: Any) -> None:
        self.name = name
        self.data = data


class DynamicEvents:

    def __init__(self, name_and_datas: List[Tuple[str, Any]]) -> None:
        self.name_and_datas = name_and_datas

@dataclass
class File:
    name: str
    content: bytes
    data: Any


@dataclass
class FileResource:
    name: str
    path: Optional[str] = None
    content: Optional[Union[str, bytes]] = None
    chunk_size: Optional[int] = None
    content_type: Optional[str] = None
    length: Optional[int] = None
    stat: Optional[stat_result] = None
    modify_timestamp_ns: Optional[int] = None

    _empty: bool = False 

    @classmethod
    def empty(cls):
        return cls("", _empty=True)


@dataclass
class FileDesc:
    name: str
    content_type: Optional[str] = None
    length: Optional[int] = None
    stat: Optional[stat_result] = None


@dataclass
class FileResourceRequest:
    key: str
    is_metadata_req: bool
    offset: Optional[int] = None
    params: Dict[str, Any] = dataclasses.field(default_factory=dict)


def from_yaml_path(path: Union[Path, str]) -> ServiceDef:
    """read yaml config with strong-type check
    """
    p = Path(path)
    with p.open("r") as f:
        data = f.read()
    return ServiceDef.from_yaml(data)

def update_service_def_config(serv_config: Any, servs: List[Service]):
    key_to_serv: Dict[str, Service] = {}
    for serv in servs:
        key = serv.module_name
        key = TENSORPC_SPLIT.join(key.split(TENSORPC_SPLIT)[:2])
        key_to_serv[key] = serv
    for k, v in serv_config.items():
        assert k in key_to_serv, f"{k} not exist in services"
        key_to_serv[k].config = v

def decode_config_b64_and_update(cfg_b64: str, servs: List[Service], is_gzip: bool = False):
    if is_gzip:
        serv_config_str = gzip.decompress(base64.b64decode(cfg_b64)).decode("utf-8")
    else:
        serv_config_str = base64.b64decode(cfg_b64).decode("utf-8")
    serv_config = json.loads(serv_config_str)
    return update_service_def_config(serv_config, servs)

class RelayCallType(enum.IntEnum):
    RemoteCall = 0
    ClientStream = 1
    RemoteGenerator = 2
    BiStream = 3
