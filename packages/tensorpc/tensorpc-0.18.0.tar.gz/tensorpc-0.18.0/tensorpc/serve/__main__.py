import json
from pathlib import Path
from typing import Dict, Optional

import fire
import time
from tensorpc.constants import TENSORPC_PORT_MAX_TRY
from tensorpc.core.client import RemoteManager
from tensorpc.core.asyncserver import serve, serve_with_http
from tensorpc.core.defs import Service, ServiceDef, from_yaml_path, decode_config_b64_and_update, update_service_def_config
from tensorpc.core import BUILTIN_SERVICES
import base64


# TODO service prompt
def serve_in_terminal(*modules: str,
                      wait_time=-1,
                      port=50051,
                      http_port=None,
                      length=-1,
                      serv_def_file: Optional[str] = None,
                      max_threads=10,
                      serv_config_b64: str = "",
                      serv_config_is_gzip: bool = False,
                      ssl_key_path: str = "",
                      ssl_crt_path: str = "",
                      serv_config_json: Optional[dict] = None,
                      max_port_retry: int = TENSORPC_PORT_MAX_TRY):
    if serv_def_file is not None:
        service_def = from_yaml_path(serv_def_file)
    else:
        servs = [Service(m, {}) for m in modules]
        service_def = ServiceDef(servs)
    service_def.services.extend(BUILTIN_SERVICES)
    if serv_config_b64 != "":
        decode_config_b64_and_update(serv_config_b64, service_def.services, serv_config_is_gzip)
    elif serv_config_json is not None:
        # used for wrapper
        update_service_def_config(serv_config_json, service_def.services)
    if http_port is not None:
        return serve_with_http(wait_time=wait_time,
                               http_port=http_port,
                               port=port,
                               length=length,
                               max_threads=max_threads,
                               service_def=service_def,
                               ssl_key_path=ssl_key_path,
                               ssl_crt_path=ssl_crt_path,
                               max_port_retry=max_port_retry)
    return serve(wait_time=wait_time,
                 port=port,
                 length=length,
                 max_threads=max_threads,
                 service_def=service_def,
                 ssl_key_path=ssl_key_path,
                 ssl_crt_path=ssl_crt_path,
                 max_port_retry=max_port_retry)


if __name__ == "__main__":
    fire.Fire(serve_in_terminal)
