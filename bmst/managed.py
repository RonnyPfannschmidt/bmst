"""
    Basic utilities for the combined blob+metadata store
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import json
import bz2
import hashlib


def find_missing_blobs(expected, store):
    """
    utility to check if any blobs for a meta item are missing
    """
    keys = set(store.keys())
    missing = {}
    for name, value in expected.items():
        if value not in keys:
            missing[name] = value
    if missing:
        # cause we want None else
        return missing


def sha1(data):
    """
    shortcut to get a hexdigest sha1 of some data
    """
    return hashlib.sha1(data).hexdigest()


def check_store(bmst, kind):
    """
    check hash consistency of the store `kind` in `bmst`
    """
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
    """
    check if all blobs required for the mea items exist
    """
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
    """
    search for unreferenced blobs
    """
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
    """
    utility function to check or generate the key of a data item and compress it in one step
    """
    computed_key = sha1(raw_data)
    if key is not None and computed_key != key:
        raise ValueError('%r != %r)' % (key, computed_key))
    return computed_key, bz2.compress(raw_data)


class BMST(object):
    """
    this class combines a store for meta items and a store for blobs
    to something that can store backups or whatever else desired

    it takes care of checking keys, encoding metadata to json
    and bz2 compressing data before storing

    :param blobs: the store for the blobs
    :param meta: the store for meta item
    """

    def __init__(self, blobs, meta):
        self.blobs = blobs
        self.meta = meta

    def store_meta(self, key=None, mapping=None):
        """
        :param key: the expected sha1 id
        :param mapping: the json compatible data for this item

        store a new meta item
        """

        missing = find_missing_blobs(mapping['items'], self.blobs)
        if missing:
            raise LookupError(missing)

        raw_data = json.dumps(mapping, indent=2, sort_keys=True)
        raw_data = raw_data.encode('utf-8')
        key, encoded = encode_data(raw_data, key)
        self.meta[key] = encoded

        return key

    def load_meta(self, key):
        """
        load and json-deserialize a metadata item
        """
        return json.loads(bz2.decompress(self.meta[key]))

    def store_blob(self, key=None, data=None):
        """
        store a compressed blob
        """
        key, encoded = encode_data(data, key)
        self.blobs[key] = encoded
        return key

    def load_blob(self, key):
        """load and decompress a blob"""
        return bz2.decompress(self.blobs[key])
