from .Action import SkiffAction
from .Image import SkiffImage
from .Size import SkiffSize
from .Kernel import SkiffKernel
from .Region import SkiffRegion
from .Network import SkiffNetwork
from .Key import SkiffKey
from . import Domain

skiff = None


def setSkiff(s):
    global skiff
    skiff = s


def destroy_droplet(did):
    return skiff.delete('/droplets/' + str(did))


class SkiffDroplet(object):
    """SkiffDroplet"""
    def __init__(self, options=None, **kwargs):
        super(SkiffDroplet, self).__init__()
        if not options:
            options = kwargs

        self._json = options
        # create instance methods for everything in options
        self.__dict__.update(options)
        # droplet snapshots, backups, actions, networks
        # @TODO: make this cleaner?
        self.region = SkiffRegion(options['region'])
        self.image = SkiffImage(options['image'])
        self.size = SkiffSize(options['size'])
        self.kernel = SkiffKernel(options['kernel'])
        for network_type, networks in options['networks'].iteritems():
            setattr(self, network_type, [SkiffNetwork(n) for n in networks])

        # aliases
        self.restart = self.reboot
        self.action = self.get_action
        self.reset_password = self.password_reset
        self.refresh = self.reload

    def __repr__(self):
        return '<%s (#%d) %s - %s - %s' % (self.name, self.id, self.region.slug, self.image.name, self.size.slug)

    def do_action(self, action, options=None):
        if not options:
            options = {}

        if isinstance(action, SkiffAction):
            action = action.type

        options['type'] = action

        r = skiff.post('/droplets/%s/actions' % (self.id), data=options)
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return SkiffAction(r['action'])

    def destroy(self):
        return destroy_droplet(self.id)

    def kernels(self):
        r = skiff.get('/droplets/%s/kernels' % (self.id))
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return [SkiffKernel(a) for a in r['kernels']]

    def snapshots(self):
        r = skiff.get('/droplets/%s/snapshots' % (self.id))
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return [SkiffImage(a) for a in r['snapshots']]

    def backups(self):
        r = skiff.get('/droplets/%s/backups' % (self.id))
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return [SkiffImage(a) for a in r['backups']]

    def actions(self):
        r = skiff.get('/droplets/%s/actions' % (self.id))
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return [SkiffAction(a) for a in r['actions']]

    def reboot(self):
        return self.do_action('reboot')

    def power_cycle(self):
        return self.do_action('power_cycle')

    def shutdown(self):
        return self.do_action('shutdown')

    def power_off(self):
        return self.do_action('power_off')

    def power_on(self):
        return self.do_action('power_on')

    def password_reset(self):
        return self.do_action('password_reset')

    def resize(self, slug):
        # if is of class SkiffSize, grab its property
        if isinstance(slug, SkiffSize):
            slug = slug.slug
        return self.do_action('resize', {'size': slug})

    def restore(self, backup):
        # if is of class SkiffImage, grab its property
        if isinstance(backup, SkiffImage):
            backup = backup.id
        return self.do_action('resize', {'image': backup})

    def rebuild(self, image=None):
        # if is of class SkiffImage, grab its property
        if image and isinstance(image, SkiffImage):
            image = image.id
        elif not image:
            image = self.image.id
        return self.do_action('rebuild', {'image': image})

    def rename(self, new_name):
        r = self.do_action('rename', {'name': new_name})
        self.name = new_name
        return r

    def change_kernel(self, kernel):
        # if kernel is of class SkiffKernel, grab its property
        if isinstance(kernel, SkiffKernel):
            kernel = kernel.id
        return self.do_action('change_kernel', {'kernel': kernel})

    def enable_ipv6(self):
        return self.do_action('enable_ipv6')

    def disable_backups(self):
        return self.do_action('disable_backups')

    def enable_private_networking(self):
        return self.do_action('enable_private_networking')

    def get_action(self, action_id):
        r = skiff.get('/droplets/%s/actions/%s' % (self.id, action_id))
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return SkiffAction(r['action'])

    # UTILITY METHODS
    def has_action_in_progress(self):
        for action in self.actions():
            if action.status == 'in-progress':
                return True

        return False

    def reload(self):
        return get(self.id)

    def wait_till_done(self, t=5):
        import time
        while self.has_action_in_progress():
            time.sleep(t)

    def create_domain(self, domain_name):
        return Domain.create(name=domain_name, ip_address=self.v4[0].ip_address)


def get(did):
    if type(did).__name__ == 'int':
        # is droplet id, get it
        r = skiff.get('/droplets/%s' % (did))
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return SkiffDroplet(r['droplet'])
    else:
        # is droplet name, search
        # @TODO: use fuzzy search or something more intelligent
        ds = all()
        for d in ds:
            if did in d.name:
                return d

        raise ValueError('No Suitable Droplet Found for Search: %s' % did)


def create(options=None, **kwargs):
    if not options:
        options = kwargs

    for key, val in options.iteritems():
        if key == 'region' and isinstance(val, SkiffRegion):
            options['region'] = val.slug
        elif key == 'size' and isinstance(val, SkiffSize):
            options['size'] = val.slug
        elif key == 'image' and isinstance(val, SkiffImage):
            options['image'] = val.id
        elif key == 'ssh_keys':
            for i, ssh_key in enumerate(val):
                if isinstance(ssh_key, SkiffKey):
                    options['ssh_keys'][i] = ssh_key.id

    r = skiff.post('/droplets', data=options)
    if 'message' in r:
        raise ValueError(r['message'])
    else:
        return SkiffDroplet(r['droplet'])


# alias new to create
new = create


def all(params=None, **kwargs):
    if not params:
        params = kwargs

    r = skiff.get('/droplets', params)
    if 'message' in r:
        # @TODO: Better error?
        raise ValueError(r['message'])
    else:
        # create new Droplets for each droplet
        return [SkiffDroplet(d) for d in r['droplets']]
