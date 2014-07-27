import requests
from .utils import DO_BASE_URL, DO_HEADERS
from .utils import page_collection


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
    paging_action = lambda r: [SkiffAction(a) for a in r["actions"]]
    return page_collection(DO_BASE_URL + '/actions', paging_action)


def get(aid):
    r = requests.get(DO_BASE_URL + '/actions/' + str(aid), headers=DO_HEADERS)
    r = r.json()
    return SkiffAction(r["action"])
