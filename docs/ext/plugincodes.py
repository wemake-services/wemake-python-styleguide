import importlib
import re
from collections.abc import Sequence
from inspect import isclass
from types import ModuleType
from typing import final

from docutils import nodes
from docutils.statemachine import StringList
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.ext import autosummary
from sphinx.ext.autodoc.directive import AutodocDirective
from sphinx.util.docutils import SphinxDirective

from wemake_python_styleguide.violations.base import BaseViolation


@final
class PlugincodesDirective(SphinxDirective):
    """Custom directive for parsing WPS violations for docs."""

    required_arguments = 1

    def run(self) -> Sequence[nodes.Node]:
        """Creating directive nodes."""
        module_full_path = self.arguments[0]
        module = importlib.import_module(module_full_path)
        violation_classes = self.get_violations(module)

        third_party_directive_payload = {
            'lineno': self.lineno,
            'content_offset': 0,
            'block_text': self.block_text,
            'state': self.state,
            'state_machine': self.state_machine,
        }

        summary_section = nodes.section(ids=['summary'])
        summary_section += nodes.title(text='Summary')

        return [
            *self.get_automodule_nodes(
                module_full_path,
                **third_party_directive_payload,
            ),
            summary_section,
            *self.get_autosummary_nodes(
                violation_classes,
                **third_party_directive_payload,
            ),
            *self.get_autoclass_nodes(
                violation_classes,
                **third_party_directive_payload,
            ),
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
        **kwargs,
    ) -> Sequence[nodes.Node]:
        """Use autosummary directive to build violation nodes."""
        autosummary_content = StringList([
            violation_class.__name__ for violation_class in violation_classes
        ])
        local_autosummary = autosummary.Autosummary(
            name='autosummary',
            arguments=[],
            options={'nosignatures': True},
            content=autosummary_content,
            **kwargs,
        )

        return local_autosummary.run()

    def get_autoclass_nodes(
        self,
        violation_classes: list[type[BaseViolation]],
        **kwargs,
    ) -> Sequence[nodes.Node]:
        """Use autodoc for build violation docstring nodes."""
        violation_class_nodes = []
        options = {
            'exclude-members': 'error_template,code',
        }
        for violation_class in violation_classes:
            local_autodoc = AutodocDirective(
                name='autoclass',
                arguments=[violation_class.__name__],
                options=options,
                content=StringList(),
                **kwargs,
            )
            filtered_nodes = self._filter_autoclass_nodes(local_autodoc.run())
            violation_class_nodes.extend(filtered_nodes)

        return violation_class_nodes

    def get_automodule_nodes(
        self,
        module_full_path: str,
        **kwargs,
    ) -> Sequence[nodes.Node]:
        """Use autodoc for build violation module docstring nodes."""
        local_autodoc = AutodocDirective(
            name='automodule',
            arguments=[module_full_path],
            options={'no-members': None},
            content=StringList(),
            **kwargs,
        )

        return local_autodoc.run()

    def _filter_autoclass_nodes(
        self, nodes_to_filter: Sequence[nodes.Node]
    ) -> Sequence[nodes.Node]:
        all_nodes = (
            inner_node
            for node in nodes_to_filter
            for inner_node in node.traverse(nodes.Node)
        )
        for node in all_nodes:
            text_node = node.astext().strip()

            if (
                isinstance(node, addnodes.desc_annotation)
                and text_node == 'final class'
            ):
                node.parent.remove(node)

            if isinstance(node, addnodes.desc_parameterlist):
                node.parent.remove(node)

            if isinstance(node, nodes.paragraph) and re.match(
                r'^Bases: [A-Za-z.]+$', text_node
            ):
                node.parent.remove(node)

        return nodes_to_filter


def setup(app: Sphinx) -> None:
    """Setup for sphinx extension."""
    app.setup_extension('sphinx.ext.autosummary')
    app.setup_extension('sphinx.ext.autodoc')
    app.add_directive('plugincodes', PlugincodesDirective)
