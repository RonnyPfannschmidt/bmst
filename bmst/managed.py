import json
from bmst.metastore import find_missing_blobs
import bz2
import hashlib

class Combined(object):
    def __init__(self, compression, store, root):
        self.meta = store(root, 'meta')
        self.blobs = store(root, 'blobs')
        self.compression = compression


    def put_meta(self, key, mapping):
        missing = find_missing_blobs(mapping, self.blobs)
        if missing:
            raise LookupError(missing)

        raw_data = json.dumps(mapping, indent=2, sort_keys=True)
