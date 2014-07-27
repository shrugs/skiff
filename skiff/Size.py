import requests
from .utils import DO_BASE_URL, DO_HEADERS
from .utils import page_collection


class SkiffSize(object):
    """SkiffSize"""
    def __init__(self, options=None, **kwargs):
        super(SkiffSize, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)

    def __repr__(self):
        return '<' + self.slug + '>'


def all():
    paging_action = lambda r: [SkiffSize(a) for a in r["sizes"]]
    return page_collection(DO_BASE_URL + '/sizes', paging_action)


def get(s):
    s = str(s)
    sizes = all()
    for size in sizes:
        if s in size.slug:
            return size
    raise ValueError('Unknown Size')
