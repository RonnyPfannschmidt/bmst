import py
import collections
import json

class BaseStore(collections.MutableMapping):

    def __delitem__(self, key):
        raise TypeError('delete not supported')

class FileStore(BaseStore):
    def __init__(self, root, subdir=None):
        if subdir:
            self.path = root.join(subdir)
        else:
            self.path = root

    def __setitem__(self, key, data):
        self.path.join(key).write(data)

    def __getitem__(self, key):
        try:
            return self.path.join(key).read()
        except py.error.ENOENT:
            raise KeyError(key)

    def __contains__(self, key):
        return self.path.join(key).check()

    def __len__(self):
        return len(self.path.listdir())

    def __iter__(self):
        for item in self.path.listdir():
            yield item.basename

class MappingStore(BaseStore):
    def __init__(self, mapping, prefix=None, update=False):
        self.prefix = prefix
        if update:
            self.mapping = {}
            self.update(mapping)
        else:
            self.mapping = mapping

    def __setitem__(self, key, value):
        self.mapping[self.prefix, key] = value

    def __getitem__(self, key):
        return self.mapping[self.prefix, key]

    def __contains__(self, key):
        return (self.prefix, key) in self.mapping

    def __iter__(self):
        for prefix, key in self.mapping:
            if prefix is self.prefix:
                yield key

    def __len__(self):
        #XXX wrong
        return len(self.mapping)


class Httplib2Store(BaseStore):
    def __init__(self, base, prefix=None):
        import httplib2
        self.http = httplib2.Http()
        if prefix is None:
            self.url = base
        else:
            self.url = '%s/%s/' % (base, prefix)

    def __getitem__(self, key):
        headers, content = self.http.request(self.url+key)
        if headers['status'] == '404':
            raise KeyError(key)
        return content

    def __setitem__(self, key, value):
        self.http.request(
            self.url+key,
            method='PUT',
            body=value,
        )

    def __iter__(self):
        headers, content = self.http.request(self.url)
        #XXX: check headers
        return iter(json.loads(content))

    def __len__(self):
        pass
