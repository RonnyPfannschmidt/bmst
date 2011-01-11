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
        return bmst.put_meta(mapping=meta)
    except LookupError as e:
        missing_mapping = e.args[0]
        for key in missing_mapping.values():
            bmst.put_blob(key=key, data=blobs[key])

        return bmst.put_meta(mapping=meta)


def get_bmst(root):
    root.ensure(dir=1)
    meta = bmst.FileStore(root.ensure('meta', dir=1))
    blobs = bmst.FileStore(root.ensure('blobs', dir=1))
    return BMST(meta=meta, blobs=blobs)


def main():
    if len(sys.argv) == 2:
        config = py.iniconfig.IniConfig(sys.argv[1])
    else:
        config = py.iniconfig.IniConfig('bmst.ini')
    path = py.path.local().join(config.get('backup', 'store'), abs=1)
    bmst = get_bmst(path)
    import shlex
    roots = config.get('backup', 'roots', convert=shlex.split)
    for root in roots:
        path = py.path.local().join(root, abs=1)
        make_backup(path, bmst)
