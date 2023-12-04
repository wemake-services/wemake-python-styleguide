from importlib import metadata as importlib_metadata


def get_version(distribution_name: str) -> str:
    """Our helper to get version of a package."""
    return importlib_metadata.version(distribution_name)
