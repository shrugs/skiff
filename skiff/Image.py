import requests
import json
from .utils import DO_BASE_URL, DO_HEADERS, DO_DELETE_HEADERS


class SkiffImage(object):
    """SkiffImage"""
    def __init__(self, options=None, **kwargs):
        super(SkiffImage, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)

    def __repr__(self):
        return '<' + self.name + ' (#' + str(self.id) + ') ' + self.distribution + '>'

    # @TODO: make this work
    def do_action(self, action, options=None):
        if not options:
            options = {}

        if isinstance(action, SkiffAction):
            action = action.type

        options["type"] = action
        r = requests.post(DO_BASE_URL + '/images/' + str(self.id) + '/actions', data=json.dumps(options), headers=DO_HEADERS)
        r = r.json()
        if "message" in r:
            raise ValueError(r["message"])
        else:
            return SkiffAction(r["action"])

    def transfer(self, region):
        if isinstance(region, SkiffRegion):
            region = region.slug

        return self.do_action('transfer', {'region': region})

    def delete(self):
        r = requests.delete(DO_BASE_URL + "/images/" + str(self.id), headers=DO_DELETE_HEADERS)
        return r.status_code == 204

    def update(self, new_name):
        options = {
            'name': new_name
        }
        r = requests.put(DO_BASE_URL + '/images/' + str(self.id), data=json.dumps(options), headers=DO_HEADERS)
        r = r.json()
        return SkiffImage(r["image"])

    def actions(self):
        r = requests.get(DO_BASE_URL + '/images/' + str(self.id) + '/actions', headers=DO_HEADERS)
        r = r.json()
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return [SkiffAction(a) for a in r['actions']]

    def get_action(self, action):
        if isinstance(action, SkiffAction):
            action = action.id
        r = requests.get(DO_BASE_URL + '/images/' + str(self.id) + '/actions/' + str(action), headers=DO_HEADERS)
        r = r.json()
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return SkiffAction(r['action'])


def get(iid):
    # same endpoint works with ids and slugs
    r = requests.get(DO_BASE_URL + '/images/' + str(iid), headers=DO_HEADERS)
    r = r.json()
    if 'message' in r:
        raise ValueError(r['message'])
    else:
        return SkiffImage(r['image'])


def all():
    r = requests.get(DO_BASE_URL + '/images', headers=DO_HEADERS)
    r = r.json()
    if 'message' in r:
        # @TODO: Better error?
        raise ValueError(r['message'])
    else:
        # create new images for each image
        return [SkiffImage(d) for d in r["images"]]
