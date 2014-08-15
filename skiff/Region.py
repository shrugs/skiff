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

        self.__dict__.update(options)

    def __repr__(self):
        return '<%s (%s)>' % (self.name, self.slug)


def all():
    r = skiff.get('/regions')
    return [SkiffRegion(a) for a in r['regions']]


def get(r):
    regions = all()
    for region in regions:
        if r in region.slug:
            return region
    raise ValueError('No Suitable Region Found')
