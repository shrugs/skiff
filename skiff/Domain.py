skiff = None


def setSkiff(s):
    global skiff
    skiff = s


class SkiffDomainRecord(object):
    """SkiffDomainRecord"""
    def __init__(self, domain, options=None, **kwargs):
        super(SkiffDomainRecord, self).__init__()
        if not options:
            options = kwargs

        self.__dict__.update(options)
        self.domain = domain
        self.destroy = self.delete
        self.refresh = self.reload

    def __repr__(self):
        return '<%s - %s (#%s) %s -> %s>' % (self.domain.name, self.type, self.id, self.name, self.data)

    def delete(self):
        return self.domain.delete_record(self.id)

    def update(self, new_name):
        self.name = new_name
        return self.domain.update_record(self.id, new_name)

    def reload(self):
        return get(self.id)


def delete_domain(did):
    return skiff.delete('/domains/%s' % (did))


class SkiffDomain(object):
    """SkiffDomain"""
    def __init__(self, options):
        super(SkiffDomain, self).__init__()

        self._json = options
        self.__dict__.update(options)
        self.record = self.get_record
        self.create = self.create_record
        self.destroy = self.delete

    def __repr__(self):
        return '<%s>' % (self.name)

    def reload(self):
        return get(self.name)

    def delete(self):
        return delete_domain(self.name)

    def records(self):
        r = skiff.get('/domains/%s/records' % (self.name))

        return [SkiffDomainRecord(self, record) for record in r['domain_records']]

    def create_record(self, options=None, **kwargs):
        if not options:
            options = kwargs

        r = skiff.post('/domains/%s/records' % (self.name), data=options)
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return SkiffDomainRecord(self, r['domain_record'])

    def delete_record(self, domain, record):
        # if is SkiffDomainRecord, grab that property
        if isinstance(record, SkiffDomainRecord):
            record = record.id

        return skiff.delete('/domains/%s/records/%s' % (self.name, record))

    def get_record(self, record):
        r = skiff.get('/domains/%s/records/%s' % (self.name, record))
        return SkiffDomainRecord(self, r['domain_record'])

    def update_record(self, record, new_name):
        if isinstance(record, SkiffDomainRecord):
            record = record.id

        options = {
            'name': new_name
        }

        r = skiff.put('/domains/%s/records/%s' % (self.name, record), data=options)
        if 'message' in r:
            raise ValueError(r['message'])
        else:
            return SkiffDomainRecord(self, r['domain_record'])


def all(params=None, **kwargs):
    if not params:
        params = kwargs

    r = skiff.get('/domains', params)
    return [SkiffDomain(a) for a in r['domains']]


def create(options=None, **kwargs):
    if not options:
        options = kwargs

    r = skiff.post('/domains', data=options)
    if 'message' in r:
        raise ValueError(r['message'])
    else:
        return SkiffDomain(r['domain'])


def get(d):
    if type(d).__name__ == 'int':
        r = skiff.get('/domains/%s' % (d))
        return SkiffDomain(r['domain'])
    else:
        # search in string
        domains = all()
        for dom in domains:
            if d in dom.name:
                return dom
        raise ValueError('No Suitable Domain Found')
