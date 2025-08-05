"""
Extra utilities used by the cli
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from pathlib import Path

from bmst.managed import BMST
from bmst.store import BaseStore, FileStore, HttpxStore, dumb_sync


def get_bmst(path: str) -> BMST:
    """
    make a simple bmst instance by choosing between http/paths
    and joining them with blobs/meta for the subitems
    """
    store: BaseStore
    if path.startswith("http"):
        path = path.rstrip("/")
        store = HttpxStore(path + "/")
    else:
        root = Path(path)
        root.mkdir(exist_ok=True, parents=True)
        store = FileStore.ensure(root)
    return BMST(storage=store)


def sync(target: BMST, sources: list[str]) -> None:
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
        dumb_sync(source=other.storage, target=target.storage)
        # Note: Original code expects separate meta/blobs stores


def extract(bmst: BMST, key: str, target: str) -> None:
    """
    load the metadata at key and extract it to target
    """
    print("extracting to", target)
    target_path = Path(target)
    meta = bmst.load_meta(key=key)
    for name, key in meta["items"].items():
        data = bmst.load_blob(key=key)
        target_file = target_path / name
        target_file.parent.mkdir(exist_ok=True, parents=True)
        target_file.write_bytes(data)
