
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

    def __repr__(self):
        return '<%s (#%s) %s>' % (self.type, self.id, self.status)


def all(params=None, **kwargs):
    if not params:
        params = kwargs

    r = skiff.get('/actions', params)
    return [SkiffAction(a) for a in r['actions']]


def get(aid):
    r = skiff.get('/actions/%s' % (aid))
    if 'message' in r:
        raise ValueError(r['message'])
    else:
        return SkiffAction(r['action'])
