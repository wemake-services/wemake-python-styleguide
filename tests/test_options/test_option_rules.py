from wemake_python_styleguide.options import config


def test_option_docs():
    """Ensures that all options are documented."""
    for option in config.Configuration._options:  # noqa: WPS437
        option_name = '``{0}``'.format(option.long_option_name[2:])
        assert option_name in config.__doc__


def test_option_help():
    """Ensures that all options has help."""
    for option in config.Configuration._options:  # noqa: WPS437
        assert len(option.help) > 10
        assert '%(default)s' in option.help
        assert option.help.split(' Defaults to:')[0].endswith('.')


def test_option_asdict_no_none():
    """Ensure that `None` is not returned from `asdict_no_none()`."""
    opt = config._Option(  # noqa: WPS437
        '--foo',
        default=False,
        action='store_true',
        type=None,
        help='',
    )
    assert 'type' not in opt.asdict_no_none()
