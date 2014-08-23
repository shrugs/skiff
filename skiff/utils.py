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

    def get(self, url, action, params=None):
        if not params:
            params = {
                'page': True
            }

        collection = []
        r = requests.get(DO_BASE_URL + url, params=params, headers=self.DO_HEADERS).json()

        if 'message' in r:
            raise ValueError(r['message'])
        else:
            collection.extend(action(r))
            if 'links' in r and 'pages' in r['links'] and 'next' in r['links']['pages'] and params and params['page']:
                # should recursively page through results
                collection.extend(self.page_collection(r['links']['pages']['next'], action))

            return collection

        return None

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

    def page_collection(self, link, action):
        """Given a link to a collection of something (Images, Droplets, etc),
        collect all the items available via the API by paging through it if needed.

        The `action` parameter should be a callable that creates a list from the
        results of each intermediate API call every item found.

        via https://github.com/fhats
        """
        collection = []

        r = requests.get(link, headers=self.DO_HEADERS).json()

        if 'message' in r:
            raise ValueError(r['message'])
        else:
            collection.extend(action(r))
            if 'links' in r and 'pages' in r['links'] and 'next' in r['links']['pages']:
                collection.extend(self.page_collection(r['links']['pages']['next'], action))

        return collection


def rig(token):
    return SkiffClass(token)
