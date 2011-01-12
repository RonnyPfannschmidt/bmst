import argparse
import shlex
import py

parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.convert_arg_line_to_args = shlex.split

parser.add_argument('-s', '--store', required=True)
parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('--backup', default=[], action='append')

import bmst
from bmst.backup_app import make_backup
from bmst.managed import BMST


def main():
    opts = parser.parse_args()
    if opts.debug:
        print opts
    bmst = py.path.local(opts.store)
    bmst = get_bmst(bmst)
    for to_backup in opts.backup:
        path = py.path.local(to_backup)
        make_backup(root=path, bmst=bmst)


def get_bmst(root):
    root.ensure(dir=1)
    meta = bmst.FileStore(root.ensure('meta', dir=1))
    blobs = bmst.FileStore(root.ensure('blobs', dir=1))
    return BMST(meta=meta, blobs=blobs)
