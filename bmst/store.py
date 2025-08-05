"""
Basic Store APIS
~~~~~~~~~~~~~~~~

in general a store is a mutable mapping that will not allow delete
"""

from __future__ import annotations

import collections.abc
import pathlib
from collections.abc import Iterator, KeysView
from dataclasses import dataclass
from typing import Any

import orjson


def dumb_sync(
    source: collections.abc.MutableMapping[str, bytes],
    target: collections.abc.MutableMapping[str, bytes],
) -> None:
    """
    sync items from source store to target store
    """
    to_sync = set(source) - set(target)
    for item in to_sync:
        target[item] = source[item]


class BaseStore(collections.abc.MutableMapping[str, bytes]):
    """
    convenience base class implementing basic methods for stores
    """

    def __len__(self) -> int:
        return len(self.keys())

    def __iter__(self) -> Iterator[str]:
        return iter(self.keys())

    def __delitem__(self, key: str) -> None:
        raise TypeError


@dataclass
class FileStore(BaseStore):
    """
    stores items within a directory

    :param path: path of the directory
    """

    path: pathlib.Path

    @classmethod
    def ensure(cls, path: pathlib.Path) -> FileStore:
        path.mkdir(exist_ok=True, parents=True)
        return cls(path=path)

    def _itempath(self, key: str) -> pathlib.Path:
        return self.path / key

    def __setitem__(self, key: str, data: bytes) -> None:
        self._itempath(key).write_bytes(data)

    def __getitem__(self, key: str) -> bytes:
        try:
            return self._itempath(key).read_bytes()
        except FileNotFoundError:
            raise KeyError(key)

    def __contains__(self, key: object) -> bool:
        if isinstance(key, str):
            return self._itempath(key).is_file()
        return False

    def keys(self) -> KeysView[str]:
        from collections.abc import KeysView as KeysViewImpl

        return KeysViewImpl({x.name: None for x in self.path.iterdir()})


class HttpxStore(BaseStore):
    """
    http using store

    uses get/put

    :param url: the url to use
    """

    def __init__(self, base_url: str, **kw: Any) -> None:
        import httpx

        self.http = httpx.Client(base_url=base_url, **kw)

    def __getitem__(self, key: str) -> bytes:
        response = self.http.get(key)
        if response.status_code == 404:
            raise KeyError(key)
        return response.content

    def __setitem__(self, key: str, value: bytes) -> None:
        r = self.http.put(key, content=value)
        r.raise_for_status()

    def keys(self) -> KeysView[str]:
        r = self.http.get("")
        r.raise_for_status()
        # XXX: check headers
        keys_list = orjson.loads(r.content)
        from collections.abc import KeysView as KeysViewImpl

        return KeysViewImpl({k: None for k in keys_list})
