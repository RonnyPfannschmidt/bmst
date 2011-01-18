from __future__ import print_function
import argparse
import shlex
import py
import json

parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.convert_arg_line_to_args = shlex.split

parser.add_argument('-s', '--store', required=True)
parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('-c', '--check', action='store_true')
parser.add_argument('--backup', default=[], action='append')
parser.add_argument('--serve', action='store_true')
parser.add_argument('--show', action='store_true')
parser.add_argument('--sync', default=[], action='append')
parser.add_argument('--ls', action='store_true')
parser.add_argument('--archive', action='store_true')
parser.add_argument('--extract', action='store_true')
parser.add_argument('key', default=None, nargs='?')
parser.add_argument('target', default=None, nargs='?')


from bmst.backup_app import make_backup
from bmst.managed import BMST, check_bmst, dumb_sync
from bmst.store import FileStore, Httplib2Store


def main():
    opts = parser.parse_args()
    if opts.debug:
        print(opts)
    print('using store', opts.store)
    bmst = get_bmst(opts.store)

    if opts.sync:
        sync(bmst, opts.sync)

    if opts.check:
        check_bmst(bmst)

    for to_backup in opts.backup:
        path = py.path.local(to_backup)
        make_backup(root=path, bmst=bmst)

    import pprint
    if opts.show:
        pprint.pprint(list(bmst.meta))

    if opts.ls:
        assert opts.key, 'omg key missing'
        print(json.dumps(
            bmst.load_meta(key=opts.key),
            indent=2,
            sort_keys=True,
        ))

    if opts.extract:
        extract(bmst, opts.key, opts.target)

    if opts.archive:
        archive(bmst, opts.key, opts.target)

    if opts.serve:
        from bmst.wsgi import app
        app.bmst = bmst
        app.run()


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
