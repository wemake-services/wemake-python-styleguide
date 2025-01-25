import importlib
from collections.abc import Collection
from contextlib import suppress
from pathlib import Path
from types import ModuleType
from typing import Final

_VIOLATION_MODULE_BASE: Final = 'wemake_python_styleguide.violations'


def get_violation_submodules() -> Collection[ModuleType]:
    """Get all possible violation submodules."""
    return _safely_get_all_submodules(_VIOLATION_MODULE_BASE)


def _safely_get_all_submodules(module_name: str) -> Collection[ModuleType]:
    """Get all submodules of given module. Ignore missing."""
    submodule_names = _get_all_possible_submodule_names(module_name)
    modules = []
    for submodule_name in submodule_names:
        # just in case if there are some bad module paths
        # (which generally should not happen)
        with suppress(ModuleNotFoundError):
            modules.append(importlib.import_module(submodule_name))
    return modules


def _get_all_possible_submodule_names(module_name: str) -> Collection[str]:
    """Get .py submodule names listed in given module."""
    root_module = importlib.import_module(module_name)
    root_paths = root_module.__path__
    names = []
    for root in root_paths:
        names.extend([
            f'{module_name}.{name}'
            for name in _get_all_possible_names_in_root(root)
        ])
    return names


def _get_all_possible_names_in_root(root: str) -> Collection[str]:
    """Get .py submodule names listed in given root path."""
    return [
        path.name.removesuffix('.py')
        for path in Path(root).glob('*.py')
        if '__' not in path.name  # filter dunder files like __init__.py
    ]
