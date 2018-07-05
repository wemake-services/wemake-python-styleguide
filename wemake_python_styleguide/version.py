# -*- coding: utf-8 -*-

#__version__ = '0.0.2'  # noqa
# TODO: resolve after https://github.com/sdispater/poetry/issues/273

def get_user_agent_default(pkg_name='poetry'):

	version = '0.0.2'

	try:
        import pkg_resources
        version = pkg_resources.get_distribution(pkg_name).version
    except pkg_resources.DistributionNotFound:
        pass
    except ImportError:
        pass

    return 'poetry' __version__ = '0.0.2'

# or so it is better ?

#import pkg_resources

#my_version = pkg_resources.get_distribution('poetry').version