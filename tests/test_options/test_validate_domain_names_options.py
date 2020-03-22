import pytest

from wemake_python_styleguide.options.validation import (
    validate_domain_names_options,
)


@pytest.mark.parametrize(('allowed_names', 'forbidden_names'), [
    (['items'], []),
    ([], ['items']),
    (['item'], ['handle']),
])
def test_passes_when_any_option_not_passed(allowed_names, forbidden_names):
    """Ensures validation passes when any domain option not passed."""
    validate_domain_names_options(allowed_names, forbidden_names)


def test_passes_when_names_no_intersect():
    """Ensures validation passes when names no intersect."""
    validate_domain_names_options(['node'], ['visitor'])


def test_raises_valueerror_when_names_intersect():
    """Ensures `ValueError` exception is raised  when names intersect."""
    with pytest.raises(ValueError, match='visitor'):
        validate_domain_names_options(['visitor', 'handle'], ['visitor'])
