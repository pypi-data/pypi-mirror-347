import importlib
from pathlib import Path

pkg_dir = Path(__file__).parent
py_files = [f.stem for f in pkg_dir.glob('*.py') if f.is_file() and f.name != '__init__.py']

for module_name in py_files:
    module = importlib.import_module(f'.{module_name}', __package__)
    globals().update(vars(module))

__all__ = py_files