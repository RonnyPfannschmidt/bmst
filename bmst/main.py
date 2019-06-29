import argparse
import json
import shlex

import py

from bmst.backup_app import make_backup
from bmst.managed import check_bmst
from bmst.utils import archive
from bmst.utils import extract
from bmst.utils import get_bmst
from bmst.utils import sync

parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
parser.convert_arg_line_to_args = shlex.split

parser.add_argument("-s", "--store", required=True)
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument("-c", "--check", action="store_true")
parser.add_argument("--backup", default=[], action="append")
parser.add_argument("--serve", action="store_true")
parser.add_argument("--show", action="store_true")
parser.add_argument("--sync", default=[], action="append")
parser.add_argument("--ls", action="store_true")
parser.add_argument("--archive", action="store_true")
parser.add_argument("--extract", action="store_true")
parser.add_argument("key", default=None, nargs="?")
parser.add_argument("target", default=None, nargs="?")


def main():
    opts = parser.parse_args()
    if opts.debug:
        print(opts)
    print("using store", opts.store)
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
        assert opts.key, "omg key missing"
        print(json.dumps(bmst.load_meta(key=opts.key), indent=2, sort_keys=True))

    if opts.extract:
        extract(bmst, opts.key, opts.target)

    if opts.archive:
        archive(bmst, opts.key, opts.target)

    if opts.serve:
        from bmst.wsgi import app

        app.bmst = bmst
        app.run()
