skiff = None


def setSkiff(s):
    global skiff
    skiff = s


class SkiffRegion(object):
    """SkiffRegion"""
    def __init__(self, options=None, **kwargs):
        super(SkiffRegion, self).__init__()
        if not options:
            options = kwargs

        self._json = options
        self.__dict__.update(options)
        self.refresh = self.reload

    def __repr__(self):
        return '<%s (%s)>' % (self.name, self.slug)

    def reload(self):
        return get(self.slug)


def all(params=None, **kwargs):
    if not params:
        params = kwargs

    r = skiff.get('/regions', params)
    return [SkiffRegion(a) for a in r['regions']]


def get(r):
    regions = all()
    for region in regions:
        if r in region.slug:
            return region
    raise ValueError('No Suitable Region Found')
