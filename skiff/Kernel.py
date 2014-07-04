

class SkiffKernel(object):
    """SkiffKernel"""
    def __init__(self, options=None, **kwargs):
        super(SkiffKernel, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)
