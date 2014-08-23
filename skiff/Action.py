
skiff = None


def setSkiff(s):
    global skiff
    skiff = s


class SkiffAction(object):
    """SkiffAction"""
    def __init__(self, options):
        super(SkiffAction, self).__init__()

        self._json = options
        self.__dict__.update(options)
        self.refresh = self.reload

    def __repr__(self):
        return '<%s (#%s) %s>' % (self.type, self.id, self.status)

    def reload(self):
        return get(self.id)


def all(params=None, **kwargs):
    if not params:
        params = kwargs

    return skiff.get('/actions', (lambda r: [SkiffAction(a) for a in r['actions']]), params)


def get(aid):
    r = skiff.get('/actions/%s' % (aid))
    if 'message' in r:
        raise ValueError(r['message'])
    else:
        return SkiffAction(r['action'])
