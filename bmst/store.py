import collections


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
        return self.path.join(key).read()

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
        return len(self.mapping)
