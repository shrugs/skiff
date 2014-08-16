

class SkiffKernel(object):
    """SkiffKernel"""
    def __init__(self, options=None, **kwargs):
        super(SkiffKernel, self).__init__()
        if not options:
            options = kwargs

        self._json = options
        self.__dict__.update(options)

    def __repr__(self):
        return '<%s (#%s) %s>' % (self.name, self.id, self.version)
