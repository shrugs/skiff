import requests
from .utils import DO_BASE_URL, DO_HEADERS


class SkiffBackup(object):
    """SkiffBackup"""
    def __init__(self, options=None, **kwargs):
        super(SkiffBackup, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)
