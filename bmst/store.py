

class FileStore(object):
    def __init__(self, path):
        self.path = path

    def put(self, key, data):
        self.path.join(key).write(data)

    def get(self, key):
        return self.path.join(key).read()

    def __contains__(self, key):
        return self.path.join(key).check()

class MappingStore(object):
    def __init__(self, mapping):
        self.mapping = mapping

    def put(self, key, value):
        self.mapping[key] = value

    def get(self, key):
        return self.mapping[key]

    def __contains__(self, key):
        return key in self.mapping
