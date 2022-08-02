"""
    Extra utilities used by the cli
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from pathlib import Path

from bmst.managed import BMST
from bmst.store import dumb_sync
from bmst.store import FileStore
from bmst.store import HttpxStore


def get_bmst(path):
    """
    make a simple bmst instance by choosing between http/paths
    and joining them with blobs/meta for the subitems
    """
    if path.startswith("http"):
        path = path.rstrip("/")
        blobs = HttpxStore(path + "/blobs/")
        meta = HttpxStore(path + "/meta/")
    else:
        root = Path(path)
        root.mkdir(exists_ok=True, parents=True)
        meta = FileStore.ensure(root / "meta")
        blobs = FileStore.ensure(root / "blobs")
    return BMST(meta=meta, blobs=blobs)


def sync(target, sources):
    """
    pull new meta items from all given sources

    it shouldnt be interupted, since it syncs meta items first
    unless the blobs get synced as well there will be missing references
    the idea behind this order is that orphan blobs after a complete sync
    are better than mising blobs
    """
    for source in sources:
        print("pulling from", source)
        other = get_bmst(source)
        dumb_sync(source=other.meta, target=target.meta)
        dumb_sync(source=other.blobs, target=target.blobs)


def extract(bmst, key, target):
    """
    load the metadata at key and extract it to target
    """
    print("extracting to", target)
    target = Path(target)
    meta = bmst.load_meta(key=key)
    for name, key in meta["items"].items():
        data = bmst.load_blob(key=key)
        target_file = target / name
        target_file.parent.mkdir(exists_ok=True, parent=True)
        target.write_bytes(data)
