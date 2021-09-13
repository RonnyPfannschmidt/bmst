"""
    Basic utilities for the combined blob+metadata store
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from __future__ import annotations

import bz2
import hashlib
import logging
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

import attr
import orjson

log = logging.getLogger(__name__)

MANIFEST = "!manifest"


def find_missing_items(expected, store) -> Optional[Dict]:
    """
    utility to check if any blobs for a meta item are missing
    """
    keys = set(store.keys())
    missing = {}
    for name, value in expected.items():
        if value not in keys:
            missing[name] = value
    if missing:
        return missing
    else:
        return None


def sha1(data: bytes) -> str:
    """
    shortcut to get a hex-digest sha1 of some data
    """
    return hashlib.sha1(data).hexdigest()


def check_store(bmst: BMST) -> List[str]:
    """
    check hash consistency of the store `kind` in `bmst`
    """
    log.info(
        "checking storage",
    )
    store = bmst.storage
    errors = []
    for item, compressed in store.items():
        raw = bz2.decompress(compressed)
        sha = sha1(raw)
        if sha != item:
            log.warning("E: item %s got hash %s instead", item, hash)
            errors.append(item)
    return errors


def check_references(bmst: BMST):
    """
    check if all blobs required for the mea items exist
    """
    print("checking references")
    all_missing = {}

    manifest = bmst.load_meta("!manifest")

    for item in manifest["items"]:
        data = bmst.load_meta(item)
        missing = find_missing_items(data["items"], bmst.storage)
        if missing:
            print("E: missing blobs for meta, item", item)
            all_missing[item] = missing
    return all_missing


def find_orphans(bmst: BMST):
    """
    search for unreferenced blobs
    """
    print("searching orphan data")
    known = set(bmst.storage)

    manifest = bmst.load_meta(MANIFEST)

    for item in manifest["items"]:
        data = bmst.load_meta(item)
        known -= set(data["items"].values())
    if known:
        print("E: found %s orphans" % len(known))
    return known


checks = [
    check_store,
    # XXX meta items valid json test is missing
    check_references,
    find_orphans,
]


def check_bmst(bmst: BMST):

    results = []
    for check in checks:

        results.append(check(bmst))


def encode_data(raw_data: bytes, key):
    """
    utility function to check or generate the key of a data item
    and compress it in one step
    """
    computed_key = sha1(raw_data)
    if key is not None and computed_key != key:
        if key[0] != "!":
            # todo: real ref storage
            raise ValueError(f"{key!r} != {computed_key!r})")
    return computed_key, bz2.compress(raw_data)


@attr.s
class BMST:
    """
    this class combines a store for meta items and a store for blobs
    to something that can store backups or whatever else desired

    it takes care of checking keys, encoding metadata to json
    and bz2 compressing data before storing

    :param blobs: the store for the blobs
    :param meta: the store for meta item
    """

    storage = attr.ib()

    @classmethod
    def ensure_path(cls, path: Path):
        from .store import FileStore

        return cls(storage=FileStore.ensure(path))

    def store_meta(self, key: Optional[str] = None, mapping: Optional[dict] = None):
        """
        :param key: the expected sha1 id
        :param mapping: the json compatible data for this item

        store a new meta item
        """
        if mapping is not None and isinstance(mapping["items"], dict):
            missing = find_missing_items(mapping["items"], self.storage)
            if missing:
                raise LookupError(missing)

        raw_data = orjson.dumps(
            mapping, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
        )
        key_, encoded = encode_data(raw_data, key)
        self.storage[key if key is not None else key_] = encoded

        return key if key is not None else key_

    def load_meta(self, key):
        """
        load and json-deserialize a metadata item
        """
        return orjson.loads(bz2.decompress(self.storage[key]))

    def store_blob(self, key=None, data=None):
        """
        store a compressed blob
        """
        key, encoded = encode_data(data, key)
        self.storage[key] = encoded
        return key

    def load_blob(self, key):
        """load and decompress a blob"""
        return bz2.decompress(self.storage[key])

    def add_root(self, key):
        try:
            manifest = self.load_meta("!manifest")
        except KeyError:
            manifest = {"items": []}
        manifest["items"].append(key)
        self.store_meta("!manifest", manifest)
