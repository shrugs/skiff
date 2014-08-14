
DO_BASE_URL = "https://api.digitalocean.com/v2"


class SkiffClass(object):
    """docstring for SkiffClass"""

    from . import (Action, Domain, Droplet, Image, Kernel, Key, Region, Size)

    DO_HEADERS = {
        "Content-Type": "application/json"
    }
    DO_DELETE_HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    def __init__(self, token):
        super(SkiffClass, self).__init__()
        self.DO_TOKEN = DO_TOKEN
        self.DO_HEADERS['Authorization'] = "Bearer " + self.DO_TOKEN
        self.DO_DELETE_HEADERS['Authorization'] = "Bearer " + self.DO_TOKEN


def rig(token):
    return SkiffClass(token)
