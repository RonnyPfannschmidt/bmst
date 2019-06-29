import bz2
import json

from bmst.backup_app import fullmeta
from bmst.backup_app import load_tree
from bmst.backup_app import make_backup
from bmst.managed import BMST


def test_load(tmpdir):
    assert load_tree(tmpdir) == ({}, 0)

    tmpdir.ensure("a/b").write("test\n")

    assert load_tree(tmpdir) == (
        {"a/b": ("4e1243bd22c66e76c2ba9eddc1f91394e57f9f83", "test\n")},
        tmpdir.join("a/b").mtime(),
    )


def test_fullmeta(tmpdir):
    root = tmpdir.ensure("root", dir=1)
    root.join("test").write("test\n")
    meta, blobs = fullmeta(root)
    assert meta == {
        "project": "root",
        "tags": ["backup"],
        "timestamp": meta["timestamp"],  # steal timestamp
        "items": {"test": "4e1243bd22c66e76c2ba9eddc1f91394e57f9f83"},
    }

    assert blobs == {"4e1243bd22c66e76c2ba9eddc1f91394e57f9f83": b"test\n"}


def test_makebackup(tmpdir):
    test_fullmeta(tmpdir)
    bmst = BMST(blobs={}, meta={})
    make_backup(tmpdir.join("root"), bmst)
    assert bmst.blobs == {
        "4e1243bd22c66e76c2ba9eddc1f91394e57f9f83": (
            b"BZh91AY&SY\xcc\xc3q\xd4\x00\x00\x02A\x80\x00\x10\x02\x00\x0c\x00"
            b' \x00!\x9ah3M\x19\x97\x8b\xb9"\x9c(Hfa\xb8\xea\x00'
        )
    }
    key, = bmst.meta.keys()
    data = bz2.decompress(bmst.meta[key])
    meta = json.loads(data)
    assert meta == {
        "project": "root",
        "tags": ["backup"],
        "timestamp": meta["timestamp"],  # steal timestamp
        "items": {"test": "4e1243bd22c66e76c2ba9eddc1f91394e57f9f83"},
    }
