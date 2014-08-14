import json

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

        self.Droplet.setSkiff(self)

    def get(self, url):
        r = requests.get(DO_BASE_URL + url, headers=DO_HEADERS)
        return r.json()

    def post(self, url, data=None):
        if not data:
            data = {}

        r = requests.post(DO_BASE_URL + url, data=json.dumps(data), headers=DO_HEADERS)
        return r.json()

    def delete(self, url):
        if not data:
            data = {}

        r = requests.delete(DO_BASE_URL + url, headers=DO_DELETE_HEADERS)
        return r.status_code == 204

    def put(self, url, data=None):
        if not data:
            data = {}

        r = requests.put(DO_BASE_URL + url, data=json.dumps(data), headers=DO_HEADERS)
        return r.json()


def rig(token):
    return SkiffClass(token)
