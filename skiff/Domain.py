import requests
from .utils import DO_BASE_URL, DO_HEADERS


class SkiffDomain(object):
    """SkiffDomain"""
    def __init__(self, options=None, **kwargs):
        super(SkiffDomain, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)

    def delete(self):
        r = requests.delete(DO_BASE_URL + "/domains/" + str(self.id), headers=DO_DELETE_HEADERS)
        return r.status_code == 204


def all():
    r = requests.get(DO_BASE_URL + '/domains', headers=DO_HEADERS)
    r = r.json()
    return [SkiffDomain(a) for a in r["domains"]]


def create(options=None, **kwargs):
    if not options:
        options = kwargs

    r = requests.post(DO_BASE_URL + '/domains', data=options, headers=DO_HEADERS)
    r = r.json()
    if "message" in r:
        raise ValueError(r["message"])
    else:
        return SkiffDomain(r["domain"])


def get(domain):
    r = requests.get(DO_BASE_URL + '/domains/' + str(domain), headers=DO_HEADERS)
    r = r.json()
    return SkiffDomain(r["domain"])
