import json
from bmst.metastore import find_missing_blobs
import bz2
import hashlib


def sha1(data):
    return hashlib.sha1(data).hexdigest()


class BMST(object):
    def __init__(self, blobs, meta):
        self.blobs = blobs
        self.meta = meta

    def put_meta(self, key=None, mapping=None):
        raw_data = json.dumps(mapping, indent=2, sort_keys=True)
        computed_key = sha1(raw_data)
        if key is None:
            key = computed_key
        elif computed_key != key:
            raise ValueError('%r != %r)' % (key, computed_key))

        missing = find_missing_blobs(mapping, self.blobs)
        if missing:
            raise LookupError(missing)

        self.meta[key] = bz2.compress(raw_data)

        return key

    def put_blob(self, key=None, data=None):
        computed_key = sha1(data)
        if key is None:
            key = computed_key
        elif computed_key != key:
            raise ValueError

        self.blobs[key] = bz2.compress(data)
        return key
