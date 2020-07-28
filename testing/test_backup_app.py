import bz2

import pytest

from bmst.backup_app import fullmeta
from bmst.backup_app import load_tree
from bmst.backup_app import make_backup
from bmst.managed import BMST
from bmst.managed import check_bmst
from bmst.managed import MANIFEST
from bmst.managed import sha1
from bmst.store import FileStore

CONTENT = b"test\n"
CONTENT_HASH = sha1(CONTENT)
CONTENT_COMPRESSED = bz2.compress(CONTENT)


@pytest.fixture(params=[dict, FileStore])
def bmst(request, tmp_path):
    if request.param is dict:
        return BMST({})
    elif request.param is FileStore:
        return BMST.ensure_path(tmp_path / "bmst")


def test_load(tmp_path):
    assert load_tree(tmp_path) == ({}, 0)

    create = tmp_path / "a/b"
    create.parent.mkdir()
    create.write_bytes(CONTENT)

    assert load_tree(tmp_path) == (
        {"a/b": (CONTENT_HASH, CONTENT)},
        tmp_path.joinpath("a/b").stat().st_mtime,
    )


def test_fullmeta(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    root.joinpath("test").write_bytes(b"test\n")
    meta, blobs = fullmeta(root)
    assert meta == {
        "project": "root",
        "tags": ["backup"],
        "timestamp": meta["timestamp"],  # steal timestamp
        "items": {"test": CONTENT_HASH},
    }

    assert blobs == {CONTENT_HASH: CONTENT}


def test_makebackup(tmp_path, bmst):
    test_fullmeta(tmp_path)
    make_backup(tmp_path / "root", bmst)
    manifest_data = bmst.storage[MANIFEST]

    manifest = bmst.load_meta(MANIFEST)

    (item,) = manifest["items"]

    item_raw = bmst.storage[item]

    assert dict(bmst.storage.items()) == {
        CONTENT_HASH: CONTENT_COMPRESSED,
        item: item_raw,
        MANIFEST: manifest_data,
    }

    meta = bmst.load_meta(item)
    assert meta == {
        "project": "root",
        "tags": ["backup"],
        "timestamp": meta["timestamp"],  # steal timestamp
        "items": {"test": CONTENT_HASH},
    }


def test_checj(tmp_path, bmst):
    test_makebackup(tmp_path, bmst)

    check_bmst(bmst)
