"""
    Extra utilities used by the cli
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from __future__ import print_function
import json
import py
from bmst.managed import BMST
from bmst.store import FileStore, Httplib2Store, dumb_sync


def get_bmst(path):
    """
    make a simple bmst inance by choosing between http/paths and joining them with blibs/meta for the subitems
    """
    if path.startswith('http'):
        path = path.rstrip('/')
        blobs = Httplib2Store(path + '/blobs/')
        meta = Httplib2Store(path + '/meta/')
    else:
        root = py.path.local(path)
        root.ensure(dir=1)
        meta = FileStore(root.ensure('meta', dir=1))
        blobs = FileStore(root.ensure('blobs', dir=1))
    return BMST(meta=meta, blobs=blobs)


def sync(target, sources):
    """
    pull new meta items from all given sources

    it shouldnt be interupted, since it syncs meta items first
    unless the blobs get synced as well there will be missing references
    the idea behind this order is that orphan blobs after a complete sync are better than mising blobs
    """
    for source in sources:
        print('pulling from', source)
        other = get_bmst(source)
        dumb_sync(source=other.meta, target=target.meta)
        dumb_sync(source=other.blobs, target=target.blobs)


def extract(bmst, key, target):
    """
    load the metadata at key and extract it to target
    """
    print('extracting to', target)
    target = py.path.local(target)
    meta = bmst.load_meta(key=key)
    for name, key in meta['items'].items():
        data = bmst.load_blob(key=key)
        target.ensure(name).write(data)


def archive(bmst, key, target):
    """
    create the archive `target` from the iems of the metadata stored at `key`
    """
    from mercurial import archival
    kind = archival.guesskind(target)
    if kind is None:
        print('unknown archive type for', target)
        return
    archiver = archival.archivers[kind]
    #XXX should it use the project + data s prefix?
    prefix = archival.tidyprefix(target, kind, '')

    def write(name, data):
        archiver.addfile('%s/%s' % (prefix, name), 0755, False, data)

    meta = bmst.load_meta(key=key)
    print('archiving to', target)
    archiver = archiver(target, meta['timestamp'])
    write('.bmst', json.dumps(meta, indent=2, sort_keys=1))
    for name, key in meta['items'].items():
        data = bmst.load_blob(key=key)
        write(name, data)

    archiver.done()
