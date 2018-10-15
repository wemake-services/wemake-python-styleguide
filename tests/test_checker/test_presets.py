# -*- coding: utf-8 -*-

import glob
import importlib
import inspect
from importlib.machinery import SourceFileLoader
from operator import itemgetter

import pytest

from wemake_python_styleguide.checker import Checker
from wemake_python_styleguide.visitors.base import (
    BaseFilenameVisitor,
    BaseNodeVisitor,
    BaseTokenVisitor,
    BaseVisitor,
)


def _is_visitor_class(cls) -> bool:
    base_classes = {
        BaseFilenameVisitor,
        BaseNodeVisitor,
        BaseTokenVisitor,
        BaseVisitor,
    }

    return (
        inspect.isclass(cls) and
        issubclass(cls, BaseVisitor) and
        cls not in base_classes
    )


def _import_module_by_path(path: str):
    module_name = path[:-3].replace('/', '.')
    spec = importlib.util.spec_from_file_location(
        module_name,
        loader=SourceFileLoader(module_name, path),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope='module')
def all_visitors():
    """Loads all visitors into the list to be checked."""
    visitors = []
    for path in glob.glob('wemake_python_styleguide/visitors/**/*.py'):
        module = _import_module_by_path(path)
        classes_names_list = inspect.getmembers(module, _is_visitor_class)
        visitors.extend(map(itemgetter(1), classes_names_list))
    return set(visitors)


def test_all_visitors_contained_in_checker(all_visitors):
    """Ensures that all visitors are contained in a checker."""
    checker_visitors = {klass.__qualname__ for klass in Checker.visitors}

    for visitor in all_visitors:
        assert visitor.__qualname__ in checker_visitors

    assert len(all_visitors) == len(checker_visitors)
