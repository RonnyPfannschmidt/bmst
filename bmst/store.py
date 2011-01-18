"""
    Basic Store APIS
    ~~~~~~~~~~~~~~~~

    in general a store is a mutable mapping that will not allow delete
"""
import py
import collections
import json


def dumb_sync(source, target):
    """
    sync items from source store to target store
    """
    to_sync = set(source) - set(target)
    for item in to_sync:
        target[item] = source[item]


class BaseStore(collections.MutableMapping):
    """
    convience base class implementing osme defualt methods for stores
    """
    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        return iter(self.keys())

    def __delitem__(self, key):
        raise TypeError


class FileStore(BaseStore):
    """
    stores items within a directory

    :param path: a `py.path.local` instance of the directory
    """
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
    """
    http using store

    uses get/put

    :param url: the url to use
    """
    def __init__(self, url):
        import httplib2
        self.http = httplib2.Http()
        self.url = url

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
