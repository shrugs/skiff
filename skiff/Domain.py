import requests
import json
from .utils import DO_BASE_URL, DO_HEADERS, DO_DELETE_HEADERS


class SkiffDomainRecord(object):
    """SkiffDomainRecord"""
    def __init__(self, domain, options=None, **kwargs):
        super(SkiffDomainRecord, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)
        self.domain = domain

    def __repr__(self):
        return '<' + self.type + ' (#' + str(self.id) + ') ' + self.name + ' -> ' + self.data + '>'

    def delete(self):
        return delete_record(self.id)


def delete_domain(did):
    r = requests.delete(DO_BASE_URL + "/domains/" + str(did), headers=DO_DELETE_HEADERS)
    return r.status_code == 204


class SkiffDomain(object):
    """SkiffDomain"""
    def __init__(self, options=None, **kwargs):
        super(SkiffDomain, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)
        self.record = self.get_record
        self.create = self.create_record

    def __repr__(self):
        return '<' + self.name + '>'

    def delete(self):
        return delete_domain(self.name)

    def records(self):
        r = requests.get(DO_BASE_URL + '/domains/' + str(self.name) + '/records', headers=DO_HEADERS)
        r = r.json()
        return [SkiffDomainRecord(record) for record in r["domain_records"]]

    def create_record(self, options=None, **kwargs):
        if not options:
            options = kwargs

        r = requests.post(DO_BASE_URL + '/domains/' + str(self.name) + '/records', data=json.dumps(options), headers=DO_HEADERS)
        r = r.json()
        if "message" in r:
            raise ValueError(r["message"])
        else:
            return SkiffDomainRecord(r["domain_record"])

    def delete_record(self, record):
        # @TODO: if is SkiffRecord, grab that property
        r = requests.delete(DO_BASE_URL + '/domains/' + str(self.name) + '/records/' + str(record), headers=DO_DELETE_HEADERS)
        return r.status_code == 204

    def get_record(self, record):
        # @TODO: if is SkiffRecord, grab that property
        r = requests.get(DO_BASE_URL + '/domains/' + str(self.name) + '/records' + str(record), headers=DO_HEADERS)
        r = r.json()
        return SkiffDomainRecord(r["domain_record"])

    def update_record(self, record, new_name):
        # @TODO: if is SkiffRecord, grab that property
        options = {
            "name": new_name
        }
        r = request.put(DO_BASE_URL + '/domains/' + str(self.name) + '/records/' + str(record), data=json.dumps(options), headers=DO_HEADERS)
        r = r.json()
        if "message" in r:
            raise ValueError(r["message"])
        else:
            return SkiffDomainRecord(r["domain_record"])


def all():
    r = requests.get(DO_BASE_URL + '/domains', headers=DO_HEADERS)
    r = r.json()
    return [SkiffDomain(a) for a in r["domains"]]


def create(options=None, **kwargs):
    if not options:
        options = kwargs

    r = requests.post(DO_BASE_URL + '/domains', data=json.dumps(options), headers=DO_HEADERS)
    r = r.json()
    if "message" in r:
        raise ValueError(r["message"])
    else:
        return SkiffDomain(r["domain"])


def get(d):
    if type(d).__name__ == 'int':
        r = requests.get(DO_BASE_URL + '/domains/' + str(d), headers=DO_HEADERS)
        r = r.json()
        return SkiffDomain(r["domain"])
    else:
        # search in string
        domains = all()
        for dom in domains:
            if d in dom.name:
                return dom
        raise ValueError('No Suitable Domain Found')
