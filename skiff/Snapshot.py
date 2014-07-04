import requests
from .utils import DO_BASE_URL, DO_HEADERS


class SkiffSnapshot(object):
    """SkiffSnapshot"""
    def __init__(self, options=None, **kwargs):
        super(SkiffSnapshot, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)
