import importlib
from collections.abc import Sequence
from inspect import isclass
from types import ModuleType

from docutils import nodes
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.ext import autosummary
from sphinx.ext.autodoc.directive import AutodocDirective
from sphinx.util.docutils import SphinxDirective

from wemake_python_styleguide.violations.base import BaseViolation


class PlugincodesDirective(SphinxDirective):
    """Custom directive for parsing WPS violations for docs."""

    required_arguments = 1

    def run(self) -> Sequence[nodes.Node]:
        """Creating directive nodes."""
        module_full_path = self.arguments[0]
        module = importlib.import_module(module_full_path)
        violation_classes = self.get_violations(module)

        return [
            *self.get_automodule_nodes(module_full_path),
            nodes.subtitle(text='Summary'),  # FIXME: Dose not render correctly.
            *self.get_autosummary_nodes(violation_classes),
            *self.get_autoclass_nodes(violation_classes),
        ]

    def get_violations(self, module: ModuleType) -> list[type[BaseViolation]]:
        """Get WPS Violation classes sorted by code."""
        violation_classes = []
        for attribute_name in dir(module):  # noqa: WPS421
            attribute = getattr(module, attribute_name)
            if (
                isclass(attribute)
                and issubclass(attribute, BaseViolation)
                and attribute.__module__ == module.__name__
            ):
                violation_classes.append(attribute)

        return sorted(violation_classes, key=lambda violation: violation.code)

    def get_autosummary_nodes(
        self,
        violation_classes: list[type[BaseViolation]],
    ) -> Sequence[nodes.Node]:
        """Use autosummary directive to build violation nodes."""
        autosummary_content = StringList([
            f'{violation_class.__name__}'
            for violation_class in violation_classes
        ])
        local_autosummary = autosummary.Autosummary(
            name='autosummary',
            arguments=[],
            options={'nosignatures': True},
            content=autosummary_content,
            lineno=self.lineno,
            content_offset=0,
            block_text=self.block_text,
            state=self.state,
            state_machine=self.state_machine,
        )

        return local_autosummary.run()

    def get_autoclass_nodes(
        self, violation_classes: list[type[BaseViolation]]
    ) -> Sequence[nodes.Node]:
        """Use autodoc for build violation docstring nodes."""
        violation_class_nodes = []
        for violation_class in violation_classes:
            local_autodoc = AutodocDirective(
                name='autoclass',
                arguments=[f'{violation_class.__name__}'],
                options={},
                content=StringList(),
                lineno=self.lineno,
                content_offset=0,
                block_text=self.block_text,
                state=self.state,
                state_machine=self.state_machine,
            )
            violation_class_nodes.extend(local_autodoc.run())

        return violation_class_nodes

    def get_automodule_nodes(
        self, module_full_path: str
    ) -> Sequence[nodes.Node]:
        """Use autodoc for build violation module docstring nodes."""
        local_autodoc = AutodocDirective(
            name='automodule',
            arguments=[module_full_path],
            options={'no-members': None},
            content=StringList(),
            lineno=self.lineno,
            content_offset=0,
            block_text=self.block_text,
            state=self.state,
            state_machine=self.state_machine,
        )

        return local_autodoc.run()


def setup(app: Sphinx):
    """Setup for sphinx extension."""
    app.setup_extension('sphinx.ext.autosummary')
    app.setup_extension('sphinx.ext.autodoc')
    app.add_directive('plugincodes', PlugincodesDirective)
