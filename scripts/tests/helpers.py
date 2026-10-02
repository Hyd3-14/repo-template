"""拡張子なしのscriptをtestからmoduleとして読み込む。"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

SCRIPTS = Path(__file__).resolve().parent.parent


def load_script(name: str) -> ModuleType:
    loader = importlib.machinery.SourceFileLoader(name.replace("-", "_"), str(SCRIPTS / name))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    # dataclassが定義元moduleを参照するため、実行前に登録する。
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module
