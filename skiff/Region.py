import requests
from .utils import DO_BASE_URL, DO_HEADERS


class SkiffRegion(object):
    """SkiffRegion"""
    def __init__(self, options=None, **kwargs):
        super(SkiffRegion, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)


def all():
    r = requests.get(DO_BASE_URL + '/regions', headers=DO_HEADERS)
    r = r.json()
    return [SkiffRegion(a) for a in r["regions"]]


def get(region):
    return all()[region]
