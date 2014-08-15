skiff = None


def setSkiff(s):
    global skiff
    skiff = s


class SkiffImage(object):
    """SkiffImage"""
    def __init__(self, options=None, **kwargs):
        super(SkiffImage, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)

    def __repr__(self):
        return '<%s (#%s) %s>' % (self.name, self.id, self.distribution)

    def do_action(self, action, options=None):
        if not options:
            options = {}

        if isinstance(action, SkiffAction):
            action = action.type

        options['type'] = action

        r = skiff.post('/images/%s/actions' % (self.id), data=options)
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return SkiffAction(r['action'])

    def transfer(self, region):
        if isinstance(region, SkiffRegion):
            region = region.slug

        return self.do_action('transfer', {'region': region})

    def delete(self):
        return skiff.delete('/images/%s' % (self.id))

    def update(self, new_name):
        options = {
            'name': new_name
        }

        r = skiff.put('/images/%s' % (self.id), data=options)
        self.name = new_name
        return SkiffImage(r['image'])

    def actions(self):
        r = skiff.get('/images/%s/actions')
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return [SkiffAction(a) for a in r['actions']]

    def get_action(self, action_id):
        if isinstance(action_id, SkiffAction):
            action_id = action.id

        r = skiff.get('/images/%s/actions/%s' % (self.id, str(action)))
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return SkiffAction(r['action'])


def get(iid):
    # same endpoint works with ids and slugs
    r = skiff.get('/images/%s' % (iid))
    if 'message' in r:
        # could not find, try basic search
        images = all()
        for img in images:
            if iid in img.name:
                return img
        raise ValueError(r['message'])
    else:
        return SkiffImage(r['image'])


def all():
    r = skiff.get('/images')
    if 'message' in r:
        raise ValueError(r['message'])
    else:
        return [SkiffImage(d) for d in r['images']]
