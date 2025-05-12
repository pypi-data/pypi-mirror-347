import pickle
from typing import Any, Dict, List, Union
from typing_extensions import TypeAlias
from tensorpc.dock.components import mui, three
from tensorpc.dock import appctx
from tensorpc.dock.components import plus
from tensorpc.dock import mark_create_layout
import sys
from tensorpc import PACKAGE_ROOT
from tensorpc.dock.marker import mark_did_mount
import torch 

import numpy as np 
class MarkdownTutorialsTree:

    @mark_create_layout
    def my_layout(self):
        # appctx.set_app_z_index(200)  # required for drawer/dialog.
        appctx.get_app().set_enable_language_server(True)
        pyright_setting = appctx.get_app().get_language_server_settings()
        pyright_setting.python.analysis.pythonPath = sys.executable
        pyright_setting.python.analysis.extraPaths = [
            str(PACKAGE_ROOT.parent),
        ]
        tutorials_path = PACKAGE_ROOT / "examples" / "tutorials"
        tutorials: Dict[str, Any] = {}
        paths = list(tutorials_path.rglob("*.md"))
        paths.sort(key=lambda p: list(map(int,
                                          p.stem.split("-")[0].split("."))))
        for p in paths:
            md_relative_path = p.relative_to(tutorials_path)
            parts = md_relative_path.parts
            tutorials_cur = tutorials
            for part in parts[:-1]:
                if part not in tutorials:
                    tutorials_cur[part] = {}
                tutorials_cur = tutorials_cur[part]
            md_content = p.read_text()
            tutorials_cur[md_relative_path.stem] = plus.MarkdownTutorial(
                md_content, str(md_relative_path)).prop(width="100%",
                                                        height="100%",
                                                        overflow="auto")
        self.tutorials = tutorials
        init_data = {
            "points": np.random.uniform(-10, 10, size=[100, 3]),
            "wtf": False,
            "data": {'Name': ['a', 'b', None], 'Age': [10, 11, 12]},
            "net": torch.nn.Transformer(),
        }
        self.panel = plus.InspectPanel(init_data, use_fast_tree=True)
        return self.panel.prop(width="100%", height="100%", overflow="hidden")

    @mark_did_mount
    async def _on_init(self):
        await self.panel.inspector.add_object_to_tree(self.tutorials,
                                              key="tutorials",
                                              expand_level=2)
