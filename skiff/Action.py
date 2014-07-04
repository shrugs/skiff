import requests
from .utils import DO_BASE_URL, DO_HEADERS


class SkiffAction(object):
    """SkiffAction"""
    def __init__(self, options=None, **kwargs):
        super(SkiffAction, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)

    def __repr__(self):
        return '<' + self.type + ' (#' + str(self.id) + ') ' + self.status + '>'


def all():
    r = requests.get(DO_BASE_URL + '/actions', headers=DO_HEADERS)
    r = r.json()
    return [SkiffAction(a) for a in r["actions"]]


def get(aid):
    r = requests.get(DO_BASE_URL + '/actions/' + str(aid), headers=DO_HEADERS)
    r = r.json()
    return SkiffAction(r["action"])
