# -*- coding: utf-8 -*-

import importlib
import inspect
from importlib.machinery import SourceFileLoader
from operator import itemgetter
from pathlib import Path

import pytest

from wemake_python_styleguide.checker import Checker
from wemake_python_styleguide.visitors.base import (
    BaseCSTVisitor,
    BaseFilenameVisitor,
    BaseNodeVisitor,
    BaseTokenVisitor,
    BaseVisitor,
)


def _is_visitor_class(cls) -> bool:
    base_classes = {
        BaseCSTVisitor,
        BaseFilenameVisitor,
        BaseNodeVisitor,
        BaseTokenVisitor,
        BaseVisitor,
    }
    if not inspect.isclass(cls):
        return False

    return issubclass(cls, BaseVisitor) and cls not in base_classes


def _import_module_by_path(path: str):
    module_name = path[:-3].replace('/', '.')
    spec = importlib.util.spec_from_file_location(
        module_name,
        loader=SourceFileLoader(module_name, path),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _visitors_paths():
    base_path = Path('wemake_python_styleguide')
    excluded_paths = list(Path(base_path, 'presets').glob('**/*.py'))
    return [
        path for path in
        base_path.glob('**/*.py')
        if path not in excluded_paths
    ]


@pytest.fixture(scope='module')
def all_visitors():
    """Loads all visitors into the list to be checked."""
    visitors = []
    for path in _visitors_paths():
        module = _import_module_by_path(str(path))
        classes_names_list = inspect.getmembers(module, _is_visitor_class)
        visitors.extend(map(itemgetter(1), classes_names_list))
    return set(visitors)


def test_all_visitors_contained_in_checker(all_visitors):  # noqa: WPS442
    """Ensures that all visitors are contained in a checker."""
    checker_visitors = {
        klass.__qualname__
        for klass in Checker._visitors  # noqa: WPS437
        if not klass.__qualname__.startswith('_')
    }

    for visitor in all_visitors:
        assert visitor.__qualname__ in checker_visitors

    assert len(all_visitors) == len(checker_visitors)
