
try:
    from importlib import metadata  # noqa
    __version__ = metadata.version(__package__)
    del metadata
except Exception:
    __version__ = "dev"


from flowctl.commands import *  # noqa