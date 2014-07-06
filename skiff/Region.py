import requests
from .utils import DO_BASE_URL, DO_HEADERS


class SkiffRegion(object):
    """SkiffRegion"""
    def __init__(self, options=None, **kwargs):
        super(SkiffRegion, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)

    def __repr__(self):
        return '<' + self.name + ' (' + self.slug + ')>'


def all():
    r = requests.get(DO_BASE_URL + '/regions', headers=DO_HEADERS)
    r = r.json()
    return [SkiffRegion(a) for a in r["regions"]]


def get(r):
    regions = all()
    for region in regions:
        if r in region.slug:
            return region
    raise ValueError('No Suitable REgion Found')
