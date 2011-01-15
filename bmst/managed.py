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


def dumb_sync(source, target):
    """
    sync items from source to target
    """
    to_sync = set(source) - set(target)
    for item in to_sync:
        target[item] = source[item]


def check_store(bmst, kind):
    print 'checking', kind
    store = getattr(bmst, kind)
    errors = []
    for item in store:
        raw = bz2.decompress(store[item])
        sha = sha1(raw)
        if sha != item:
            print 'E: item', item, 'got hash', sha, 'instead'
            errors.append(item)
    return errors


def check_references(bmst):
    print 'checking references'
    all_missing = {}
    for item in bmst.meta:
        data = bmst.load_meta(item)
        missing = find_missing_blobs(data['items'], bmst.blobs)
        if missing:
            print 'E: missing blobs for meta, item', item
            all_missing[item] = missing
    return all_missing

def find_orphans(bmst):
    print 'searching orphan blobs'
    known = set(bmst.blobs)
    for item in bmst.meta:
        data = bmst.load_meta(item)
        known -= set(data['items'].values())
    if known:
        print 'E: found %s orphans' % len(known)
    return known

checks = [
    (check_store, 'blobs'),
    (check_store, 'meta'),
    #XXX meta items vaid json test is missing
    (check_references,),
    (find_orphans, ),
]


def check_bmst(bmst):

    results = []
    for check in checks:
        fun = check[0]
        args = check[1:]

        results.append(fun(bmst, *args))

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

    def load_meta(self, key):
        return json.loads(bz2.decompress(self.meta[key]))

    def store_blob(self, key=None, data=None):
        key, encoded = encode_data(data, key)
        self.blobs[key] = encoded
        return key

    def load_blob(self, key):
        return bz2.decompress(self.blobs[key])
