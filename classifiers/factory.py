import glob
import os
from config import SUPPORTED_MODELS
CACHED_PROVIDER = {}

def generate_factory(name):
    if name not in SUPPORTED_MODELS:
        raise ValueError(f'{name} is not supported.')
    if name not in CACHED_PROVIDER:
        module_path = f'classifiers.{name}.{name}'
        module = __import__(
            str(module_path), globals(), locals(), [name],
        )
        _cls = getattr(module, name)
        CACHED_PROVIDER[name] = _cls()
    return CACHED_PROVIDER[name]
