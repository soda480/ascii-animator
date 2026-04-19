from importlib import metadata as _metadata
import importlib
from os import getenv

__all__ = [
    'Animator',
    'Speed',
    'Animation',
    'AsciiAnimation',
]

def __getattr__(name):
    if name == 'Animator':
        from .animator import Animator
        return Animator
    if name == 'Speed':
        from .animator import Speed
        return Speed
    if name == 'Animation':
        from .animator import Animation
        return Animation
    if name == 'AsciiAnimation':
        from .animator import AsciiAnimation
        return AsciiAnimation

    # If the requested attribute isn't one of the known top-level symbols,
    # try to lazily import a submodule (e.g. `thread_order.scheduler`) so
    # attribute lookups such as those used by mocking/patching succeed.
    try:
        return importlib.import_module(f"{__name__}.{name}")
    except Exception:
        raise AttributeError(name)

try:
    __version__ = _metadata.version(__name__)
except _metadata.PackageNotFoundError:
    __version__ = '0.3.0'

if getenv('DEV'):
    __version__ = f'{__version__}+dev'
