

class FileStore(object):
    def __init__(self, path):
        self.path = path

    def put(self, key, data):
        self.path.join(key).write(data)

    def get(self, key):
        return self.path.join(key).read()


