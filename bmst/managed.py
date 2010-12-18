import json
from bmst.metastore import find_missing_blobs
import bz2
import hashlib


def sha1(data):
    return hashlib.sha1(data).hexdigest()


class BMST(object):
    def __init__(self, compression, store, root):
        self.meta = store(root, 'meta')
        self.blobs = store(root, 'blobs')
        self.compression = compression

    def put_meta(self, key=None, mapping=None):
        raw_data = json.dumps(mapping, indent=2, sort_keys=True)
        computed_key = sha1(raw_data)
        if key is None:
            key = computed_key
        elif computed_key != key:
            raise ValueError

        missing = find_missing_blobs(mapping, self.blobs)
        if missing:
            raise LookupError(missing)

        self.meta[key] = self.compression.compress(raw_data)

        return key

    def put_blob(self, key=None, data=None):
        computed_key = sha1(data)
        if key is None:
            key = computed_key
        elif computed_key != key:
            raise ValueError

        self.blobs[key] = self.compression.compress(data)
        return key
