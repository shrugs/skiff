import requests
import json
from .utils import DO_BASE_URL, DO_HEADERS, DO_DELETE_HEADERS
from .utils import page_collection


class SkiffKey(object):
    """SkiffKey"""
    def __init__(self, options=None, **kwargs):
        super(SkiffKey, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)
        self.delete = self.destroy

    def __repr__(self):
        return '<' + self.name + '(#' + (str(self.id) or '??') + ')>'

    def update(self, new_name):
        options = {
            'name': new_name
        }
        r = requests.put(DO_BASE_URL + '/account/keys/' + str(self.id), data=json.dumps(options), headers=DO_HEADERS)
        r = r.json()
        return SkiffKey(r["ssh_key"])

    def destroy(self):
        r = requests.delete(DO_BASE_URL + "/account/keys/" + str(self.id), headers=DO_DELETE_HEADERS)
        return r.status_code == 204


def get(kid):
    r = requests.get(DO_BASE_URL + '/account/keys/' + str(kid), headers=DO_HEADERS)
    r = r.json()
    if 'message' in r:
        # try searching
        keys = all()
        for key in keys:
            if kid in key.name:
                return key
        raise ValueError(r['message'])
    else:
        return SkiffKey(r['ssh_key'])


def create(options=None, **kwargs):
    if not options:
        options = kwargs
    r = requests.post(DO_BASE_URL + '/account/keys', data=json.dumps(options), headers=DO_HEADERS)
    return SkiffKey(r.json()["key"])


# alias new to create
new = create


def all():
    paging_action = lambda r: [SkiffKey(d) for d in r["ssh_keys"]]
    return page_collection(DO_BASE_URL + '/account/keys', paging_action)

