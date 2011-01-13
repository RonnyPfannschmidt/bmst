from __future__ import print_function
import argparse
import shlex
import py

parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.convert_arg_line_to_args = shlex.split

parser.add_argument('-s', '--store', required=True)
parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('--backup', default=[], action='append')

from bmst.backup_app import make_backup
from bmst.managed import BMST
from bmst.store import FileStore


def main():
    opts = parser.parse_args()
    if opts.debug:
        print(opts)
    bmst = py.path.local(opts.store)
    print('using store', bmst)
    bmst = get_bmst(bmst)

    for to_backup in opts.backup:
        path = py.path.local(to_backup)
        make_backup(root=path, bmst=bmst)


def get_bmst(root):
    root.ensure(dir=1)
    meta = FileStore(root.ensure('meta', dir=1))
    blobs = FileStore(root.ensure('blobs', dir=1))
    return BMST(meta=meta, blobs=blobs)
