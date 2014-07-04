import requests
import json
from .utils import DO_BASE_URL, DO_HEADERS, DO_DELETE_HEADERS
from.Action import SkiffAction


class SkiffDroplet(object):
    """SkiffDroplet"""
    def __init__(self, options):
        super(SkiffDroplet, self).__init__()
        # create instance methods for everything in options
        self.__dict__.update(options)
        # possibly mutate dicts into Skiff Objects for things like
        # droplet snapshots, backups, actions, networks

    def do_action(self, action, options):
        options["type"] = action
        r = requests.post(DO_BASE_URL + '/droplets/' + str(self.id) + '/actions', data=options, headers=DO_HEADERS)
        r = r.json()
        if "message" in r:
            raise ValueError(r["message"])
        else:
            return SkiffAction(r["action"])

    def destroy(self):
        r = requests.delete(DO_BASE_URL + "/droplets/" + str(self.id), headers=DO_DELETE_HEADERS)
        return r.status_code == 204

    def snapshots(self):
        r = requests.get(DO_BASE_URL + '/droplets/' + str(self.id) + '/snapshots', headers=DO_HEADERS)
        # @TODO: for each snapshot, create a SkiffSnapshot and return
        return r.json()

    def backups(self):
        r = requests.get(DO_BASE_URL + '/droplets/' + str(self.id) + '/backups', headers=DO_HEADERS)
        # @TODO: for each snapshot, create a SkiffBackup and return
        return r.json()

    def actions(self):
        r = requests.get(DO_BASE_URL + '/droplets/' + str(self.id) + '/actions', headers=DO_HEADERS)
        # @TODO: for each snapshot, create a SkiffAction and return
        return r.json()

    def kernels(self):
        r = requests.get(DO_BASE_URL + '/droplets/' + str(self.id) + '/kernels', headers=DO_HEADERS)

    def reboot(self):
        return self.do_action('reboot')

    def power_cycle(self):
        return self.do_action('power_cycle')

    def restart(self):
        # alias for reboot
        self.reboot()

    def shutdown(self):
        return self.do_action('shutdown')

    def power_off(self):
        return self.do_action('power_off')

    def power_on(self):
        return self.do_action('power_on')

    def reset_password(self):
        return self.do_action('reset_password')

    def resize(self, slug):
        # @TODO: if is of class SkiffSize, grab its property
        return self.do_action('resize', {'size': slug})

    def restore(self, image_id):
        # @TODO: if is of class SkiffImage, grab its property
        return self.do_action('resize', {'image': image_id})

    def rebuild(self, image_id=None):
        return self.do_action('rebuild', {'image': image_id})

    def rename(self, new_name):
        return self.do_action('rename', {'name': new_name})

    def change_kernel(self, kernel_id):
        # @TODO: if kernel is of class SkiffKernel, grab its property
        return self.do_action('change_kernel', {'kernel': kernel_id})

    def enable_ipv6(self):
        return self.do_action('enable_ipv6')

    # def set_backups(self, backup_state):
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

    def action(self, action_id):
        # alias for get_action
        return self.get_action(action_id)


def get(did):
    if type(did).__name__ == 'int':
        # is droplet id, get it
        r = requests.get(DO_BASE_URL + '/droplets/' + str(did), headers=DO_HEADERS)
        return SkiffDroplet(r.json())
    elif type(did).__name__ == 'str':
        # is droplet name, fuzzy search
        print did
    else:
        raise ValueError("Bad Argument")


def create(options=None, **kwargs):
    if not options:
        options = kwargs

    r = requests.post(DO_BASE_URL + '/droplets', data=json.dumps(options), headers=DO_HEADERS)
    return SkiffDroplet(r.json()["droplet"])


def all():
    r = requests.get(DO_BASE_URL + '/droplets', headers=DO_HEADERS)
    r = r.json()
    if 'message' in r:
        # @TODO: Better error?
        raise ValueError(r['message'])
    else:
        # create new Droplets for each droplet
        droplets = []
        for d in r['droplets']:
            droplets.append(SkiffDroplet(d))
        return droplets
