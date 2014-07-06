import requests
import json
from .utils import DO_BASE_URL, DO_HEADERS, DO_DELETE_HEADERS
from .Action import SkiffAction
from .Image import SkiffImage
from .Size import SkiffSize
from .Kernel import SkiffKernel
from .Region import SkiffRegion
from .Network import SkiffNetwork
from . import Domain


def destroy_droplet(did):
    r = requests.delete(DO_BASE_URL + "/droplets/" + str(did), headers=DO_DELETE_HEADERS)
    return r.status_code == 204


class SkiffDroplet(object):
    """SkiffDroplet"""
    def __init__(self, options):
        super(SkiffDroplet, self).__init__()
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

    def __repr__(self):
        return '<' + self.name + ' (#' + str(self.id) + ') ' + self.region.slug + ' - ' + self.image.name + ' - ' + self.size.slug + '>'

    def do_action(self, action, options=None):
        if not options:
            options = {}

        if isinstance(action, SkiffAction):
            action = action.type

        options["type"] = action
        r = requests.post(DO_BASE_URL + '/droplets/' + str(self.id) + '/actions', data=json.dumps(options), headers=DO_HEADERS)
        r = r.json()
        if "message" in r:
            raise ValueError(r["message"])
        else:
            return SkiffAction(r["action"])

    def destroy(self):
        return destroy_droplet(self.id)

    def snapshots(self):
        r = requests.get(DO_BASE_URL + '/droplets/' + str(self.id) + '/snapshots', headers=DO_HEADERS)
        # for each snapshot, create a SkiffImage and return
        r = r.json()
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return [SkiffImage(a) for a in r['snapshots']]

    def backups(self):
        r = requests.get(DO_BASE_URL + '/droplets/' + str(self.id) + '/backups', headers=DO_HEADERS)
        # for each backup, create a SkiffImage and return
        r = r.json()
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return [SkiffImage(a) for a in r['backups']]

    def actions(self):
        r = requests.get(DO_BASE_URL + '/droplets/' + str(self.id) + '/actions', headers=DO_HEADERS)
        # for each action, create a SkiffAction and return
        r = r.json()
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return [SkiffAction(a) for a in r['actions']]

    def kernels(self):
        r = requests.get(DO_BASE_URL + '/droplets/' + str(self.id) + '/kernels', headers=DO_HEADERS)
        # for each kernel, create a SkiffKernel and return
        r = r.json()
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return [SkiffKernel(a) for a in r['kernels']]

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
        r = requests.get(DO_BASE_URL + '/droplets/' + str(self.id) + '/actions/' + str(action_id), headers=DO_HEADERS)
        r = r.json()
        if "message" in r:
            raise ValueError(r["message"])
        else:
            return SkiffAction(r["action"])

    # UTILITY METHODS
    def has_action_in_progress(self):
        for action in self.actions():
            if action.status == 'in-progress':
                return True

        return False

    def create_domain(self, domain_name):
        return Domain.create(name=domain_name, ip_address=self.v4[0].ip_address)


def get(did):
    if type(did).__name__ == 'int':
        # is droplet id, get it
        r = requests.get(DO_BASE_URL + '/droplets/' + str(did), headers=DO_HEADERS)
        r = r.json()
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

        raise ValueError("No Suitable Droplet Found for Search: %s" % str(did))


def create(options=None, **kwargs):
    if not options:
        options = kwargs

    # @TODO: if things in options are of my classes, use those properties

    r = requests.post(DO_BASE_URL + '/droplets', data=json.dumps(options), headers=DO_HEADERS)
    return SkiffDroplet(r.json()["droplet"])


# alias new to create
new = create


def all():
    r = requests.get(DO_BASE_URL + '/droplets', headers=DO_HEADERS)
    r = r.json()
    if 'message' in r:
        # @TODO: Better error?
        raise ValueError(r['message'])
    else:
        # create new Droplets for each droplet
        return [SkiffDroplet(d) for d in r["droplets"]]
