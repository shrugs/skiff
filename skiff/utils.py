import json
import requests

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
        self.DO_TOKEN = token
        self.DO_HEADERS['Authorization'] = "Bearer %s" % (self.DO_TOKEN)
        self.DO_DELETE_HEADERS['Authorization'] = "Bearer %s" % (self.DO_TOKEN)

        self.Action.setSkiff(self)
        self.Domain.setSkiff(self)
        self.Droplet.setSkiff(self)
        self.Image.setSkiff(self)
        self.Key.setSkiff(self)
        self.Region.setSkiff(self)
        self.Size.setSkiff(self)

    def get(self, url):
        r = requests.get(DO_BASE_URL + url, headers=self.DO_HEADERS)
        return r.json()

    def post(self, url, data=None):
        if not data:
            data = {}

        r = requests.post(DO_BASE_URL + url, data=json.dumps(data), headers=self.DO_HEADERS)
        return r.json()

    def delete(self, url):
        r = requests.delete(DO_BASE_URL + url, headers=self.DO_DELETE_HEADERS)
        return r.status_code == 204

    def put(self, url, data=None):
        if not data:
            data = {}

        r = requests.put(DO_BASE_URL + url, data=json.dumps(data), headers=self.DO_HEADERS)
        return r.json()


def rig(token):
    return SkiffClass(token)
