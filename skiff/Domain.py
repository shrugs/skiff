import requests
from .utils import DO_BASE_URL, DO_HEADERS


class SkiffDomain(object):
    """SkiffDomain"""
    def __init__(self, options=None, **kwargs):
        super(SkiffDomain, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)


def all():
    r = requests.get(DO_BASE_URL + '/domains', headers=DO_HEADERS)
    r = r.json()
    return [SkiffDomain(a) for a in r["domains"]]


def create():
    pass


def get(aid):
    r = requests.get(DO_BASE_URL + '/domains/' + str(aid), headers=DO_HEADERS)
    r = r.json()
    return SkiffDomain(r["domain"])
