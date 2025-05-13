from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("mb-rngpy")
except PackageNotFoundError:
    pass
