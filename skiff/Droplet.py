import requests
import json
from .utils import DO_BASE_URL, DO_HEADERS, DO_DELETE_HEADERS


class SkiffDroplet(object):
    """SkiffDroplet"""
    def __init__(self, options):
        super(SkiffDroplet, self).__init__()
        # create instance methods for everything in options
        self.__dict__.update(options)

    def destroy(self):
        r = requests.delete(do_url + "/droplets/" + str(self.id), headers=DO_DELETE_HEADERS)
        return r.status_code == 204

    def snapshots(self):
        pass

    def backups(self):
        pass

    def actions(self):
        pass

    def reboot(self):
        pass

    def power_cycle(self):
        pass

    def restart(self):
        # alias for reboot
        self.reboot()

    def shutdown(self):
        pass

    def power_off(self):
        pass

    def power_on(self):
        pass

    def reset_password(self):
        pass

    def resize(self, slug):
        pass

    def restore(self, image_id):
        pass

    def rebuild(self, image_id):
        pass

    def rename(self, new_name):
        pass

    def change_kernel(self, kernel_id):
        pass

    def enable_ipv6(self):
        pass

    # def set_backups(self, backup_state):
    def disable_backups(self):
        pass

    def enable_private_networking(self):
        pass


def get(did):
    if type(did).__name__ == 'int':
        # is droplet id, get it
        print did
    elif type(did).__name__ == 'str':
        # is droplet name, fuzzy search
        print did
    else:
        raise ValueError("Bad Argument")


def create(options=None, **kwargs):
    if not options:
        options = kwargs

    r = requests.post(DO_BASE_URL + '/droplets', data=json.dumps(options), headers=DO_HEADERS).json()
    return SkiffDroplet(r["droplet"])


def all():
    r = requests.get(DO_BASE_URL + '/droplets', headers=DO_HEADERS).json()
    if 'message' in r:
        # @TODO: Better error?
        raise ValueError(r['message'])
    else:
        # create new Droplets for each droplet
        droplets = []
        for d in r['droplets']:
            droplets.append(SkiffDroplet(d))
        return droplets


def kernels():
    pass
