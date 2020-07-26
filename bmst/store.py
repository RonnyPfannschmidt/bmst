"""
    Basic Store APIS
    ~~~~~~~~~~~~~~~~

    in general a store is a mutable mapping that will not allow delete
"""
from __future__ import annotations

import collections.abc
import json
import pathlib

import attr


def dumb_sync(source, target):
    """
    sync items from source store to target store
    """
    to_sync = set(source) - set(target)
    for item in to_sync:
        target[item] = source[item]


class BaseStore(collections.abc.MutableMapping):
    """
    convience base class implementing basic methods for stores
    """

    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        return iter(self.keys())

    def __delitem__(self, key):
        raise TypeError


@attr.s
class FileStore(BaseStore):
    """
    stores items within a directory

    :param path: path of the directory
    """

    path: pathlib.Path = attr.ib()

    @classmethod
    def ensure(cls, path: pathlib.Path) -> FileStore:
        path.mkdir(exist_ok=True, parents=True)
        return cls(path=path)

    def _itempath(self, key):
        return self.path / key

    def __setitem__(self, key, data):
        self._itempath(key).write_bytes(data)

    def __getitem__(self, key):
        try:
            return self._itempath(key).read_bytes()
        except FileNotFoundError:
            raise KeyError(key)

    def __contains__(self, key):
        return self._itempath(key).is_file()

    def keys(self):
        return [x.name for x in self.path.iterdir()]


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
        if headers["status"] == "404":
            raise KeyError(key)
        return content

    def __setitem__(self, key, value):
        self.http.request(self.url + key, method="PUT", body=value)

    def keys(self):
        headers, content = self.http.request(self.url)
        # XXX: check headers
        return json.loads(content)
