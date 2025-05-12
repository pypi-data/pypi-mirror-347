import os
from pathlib import Path
import google.protobuf

_proto_ver = list(map(int, google.protobuf.__version__.split(".")))
PROTOBUF_VERSION = (_proto_ver[0], _proto_ver[1])

PACKAGE_ROOT = Path(__file__).parent.resolve()

TENSORPC_FUNC_META_KEY = "__tensorpc_func_meta"
TENSORPC_FLOW_FUNC_META_KEY = "__tensorpc_flow_func_meta"

TENSORPC_CLASS_META_KEY = "__tensorpc_class_meta"

TENSORPC_WEBSOCKET_MSG_SIZE = (4 << 20)
TENSORPC_SPLIT = "::"

TENSORPC_SUBPROCESS_SMEM = "TENSORPC_SUBPROCESS_SMEM"

TENSORPC_READUNTIL = "__tensorpc_readuntil_string"

TENSORPC_FILE_NAME_PREFIX = "__tensorpc_inmemory_fname"

TENSORPC_OBSERVED_FUNCTION_ATTR = "__tensorpc_observed_function__"

TENSORPC_PORT_MAX_TRY = 15

TENSORPC_SERVER_PROCESS_NAME_PREFIX = "__tensorpc_s"

TENSORPC_BG_PROCESS_NAME_PREFIX = "__tensorpc_bg_server"

TENSORPC_ENABLE_RICH_LOG = True

TENSORPC_MAIN_PID = os.getpid()

TENSORPC_SERVER_DEFAULT_PORT = 50051

TENSORPC_SSH_TASK_DEFAULT_PORT = 50151

TENSORPC_DEV_SECRET_PATH = PACKAGE_ROOT / "secret.yaml"