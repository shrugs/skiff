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


def get(iid):
    if type(iid).__name__ == 'int':
        r = requests.get(DO_BASE_URL + '/images/' + str(iid), headers=DO_HEADERS)
        r = r.json()
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return SkiffImage(r['image'])
    else:
        # search in string
        images = all()
        for img in images:
            if (iid in img.name) or (iid in img.slug):
                return img
        raise ValueError('No Suitable Image Found')


def all():
    r = requests.get(DO_BASE_URL + '/images', headers=DO_HEADERS)
    r = r.json()
    if 'message' in r:
        # @TODO: Better error?
        raise ValueError(r['message'])
    else:
        # create new images for each image
        return [SkiffImage(d) for d in r["images"]]
