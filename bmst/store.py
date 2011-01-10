import py
import collections
import json


class BaseStore(collections.MutableMapping):
    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        return iter(self.keys())

    def __delitem__(self, key):
        raise TypeError


class FileStore(BaseStore):
    def __init__(self, path):
        self.path = path

    def __setitem__(self, key, data):
        self.path.join(key).write(data, 'wb')

    def __getitem__(self, key):
        try:
            return self.path.join(key).read()
        except py.error.ENOENT:
            raise KeyError(key)

    def __contains__(self, key):
        return self.path.join(key).check()

    def keys(self):
        return [x.basename for x in self.path.listdir()]


class Httplib2Store(BaseStore):
    def __init__(self, base):
        import httplib2
        self.http = httplib2.Http()
        self.url = base

    def __getitem__(self, key):
        headers, content = self.http.request(self.url + key)
        if headers['status'] == '404':
            raise KeyError(key)
        return content

    def __setitem__(self, key, value):
        self.http.request(
            self.url + key,
            method='PUT',
            body=value,
        )

    def keys(self):
        headers, content = self.http.request(self.url)
        #XXX: check headers
        return json.loads(content)
