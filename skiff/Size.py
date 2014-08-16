skiff = None


def setSkiff(s):
    global skiff
    skiff = s


class SkiffSize(object):
    """SkiffSize"""
    def __init__(self, options=None, **kwargs):
        super(SkiffSize, self).__init__()
        if not options:
            options = kwargs

        self._json = options
        self.__dict__.update(options)
        self.refresh = self.reload

    def __repr__(self):
        return '<%s>' % (self.slug)

    def reload(self):
        return get(self.slug)


def all(params=None, **kwargs):
    if not params:
        params = kwargs

    r = skiff.get('/sizes', params)
    return [SkiffSize(a) for a in r['sizes']]


def get(s):
    s = str(s)
    sizes = all()
    for size in sizes:
        if s in size.slug:
            return size
    raise ValueError('Unknown Size')
