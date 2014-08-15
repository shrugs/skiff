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

        self.__dict__.update(options)

    def __repr__(self):
        return '<%s>' % (self.slug)


def all():
    r = skiff.get('/sizes')
    return [SkiffSize(a) for a in r['sizes']]


def get(s):
    s = str(s)
    sizes = all()
    for size in sizes:
        if s in size.slug:
            return size
    raise ValueError('Unknown Size')
