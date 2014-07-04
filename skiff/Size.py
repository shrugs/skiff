import requests
from .utils import DO_BASE_URL, DO_HEADERS


class SkiffSize(object):
    """SkiffSize"""
    def __init__(self, options=None, **kwargs):
        super(SkiffSize, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)


def all():
    r = requests.get(DO_BASE_URL + '/sizes', headers=DO_HEADERS)
    r = r.json()
    return [SkiffSize(a) for a in r["sizes"]]


def get(size):
    return all()[size]
