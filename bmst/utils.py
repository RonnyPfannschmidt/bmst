from __future__ import print_function
import json
import py
from bmst.managed import dumb_sync, BMST
from bmst.store import FileStore, Httplib2Store


def get_bmst(path):
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
    for source in sources:
        print('pulling from', source)
        other = get_bmst(source)
        dumb_sync(source=other.meta, target=target.meta)
        dumb_sync(source=other.blobs, target=target.blobs)


def extract(bmst, key, target):
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
