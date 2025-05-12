from tensorpc.dock import plus, mui
from tensorpc.dock.components.flowplus import ComputeFlow
from tensorpc.dock import mark_create_layout
from tensorpc.dock import appctx
import sys 
from tensorpc import PACKAGE_ROOT
import numpy as np 
class ComputeFlowApp:
    @mark_create_layout
    def my_layout(self):
        appctx.get_app().set_enable_language_server(True)
        pyright_setting = appctx.get_app().get_language_server_settings()
        pyright_setting.python.analysis.pythonPath = sys.executable
        pyright_setting.python.analysis.extraPaths = [
            str(PACKAGE_ROOT.parent),
        ]
        self.cflow = ComputeFlow("tensorpc_default_cflow")
        self.panel = plus.InspectPanel({
            "a": np.zeros((100, 3)),
            "cflow_dev": ComputeFlow("tensorpc_default_cflow_dev"),
        }, use_fast_tree=True, init_layout=self.cflow)
        return self.panel.prop(width="100%", height="100%", overflow="hidden")

