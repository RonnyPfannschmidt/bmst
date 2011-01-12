import json
import bz2
import hashlib


def find_missing_blobs(expected, store):
    keys = set(store.keys())
    missing = {}
    for name, value in expected.items():
        if value not in keys:
            missing[name] = value
    if missing:
        # cause we want None else
        return missing


def sha1(data):
    return hashlib.sha1(data).hexdigest()


def encode_data(raw_data, key):
    computed_key = sha1(raw_data)
    if key is not None and computed_key != key:
        raise ValueError('%r != %r)' % (key, computed_key))
    return computed_key, bz2.compress(raw_data)


class BMST(object):
    def __init__(self, blobs, meta):
        self.blobs = blobs
        self.meta = meta

    def store_meta(self, key=None, mapping=None):

        missing = find_missing_blobs(mapping['items'], self.blobs)
        if missing:
            raise LookupError(missing)

        raw_data = json.dumps(mapping, indent=2, sort_keys=True)
        raw_data = raw_data.encode('utf-8')
        key, encoded = encode_data(raw_data, key)
        self.meta[key] = encoded

        return key

    def store_blob(self, key=None, data=None):
        key, encoded = encode_data(data, key)
        self.blobs[key] = encoded
        return key
