import sys
import py
import bmst
from bmst.managed import BMST


def fullmeta(root):
    meta, blobs = basemeta(root)
    meta.update(guessmeta(root))
    return meta, blobs


def basemeta(root):
    items, mtime = load_tree(root)

    item_meta = {}
    blobs = {}
    for k, (hash, content) in items.items():
        item_meta[k] = hash
        # asume collisions are unlikely enough
        blobs[hash] = content

    return {
        'items': item_meta,
        'timestamp': mtime,
    }, blobs


def guessmeta(root):
    return {
        'project': root.basename,
        'tags': ['backup'],
    }


def load_tree(root):
    results = {}
    mtime = 0
    for x in root.visit():
        if x.check(file=1):
            results[x.relto(root)] = x.computehash('sha1'), x.read('rb')
        mtime = max(mtime, x.mtime())

    return results, mtime


def make_backup(root, bmst):
    meta, blobs = fullmeta(root)
    try:
        return bmst.store_meta(mapping=meta)
    except LookupError as e:
        missing_mapping = e.args[0]
        for key in missing_mapping.values():
            bmst.store_blob(key=key, data=blobs[key])

        return bmst.store_meta(mapping=meta)
