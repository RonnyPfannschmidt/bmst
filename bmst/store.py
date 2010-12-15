import collections


class BaseStore(collections.MutableMapping):

    def __delitem__(self, key):
        raise TypeError('delete not supported')

class FileStore(BaseStore):
    def __init__(self, path):
        self.path = path

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
    def __init__(self, mapping):
        self.mapping = mapping

    def __setitem__(self, key, value):
        self.mapping[key] = value

    def __getitem__(self, key):
        return self.mapping[key]

    def __contains__(self, key):
        return key in self.mapping

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)
