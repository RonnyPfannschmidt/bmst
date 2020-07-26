import hashlib
from pathlib import Path

import pytest

from bmst.managed import BMST
from bmst.store import FileStore
from bmst.store import Httplib2Store

key = hashlib.sha1(b"test").hexdigest()


def setup_module(mod):
    from wsgi_intercept.httplib2_intercept import install

    install()


@pytest.fixture(
    params=[
        pytest.param(open, id="file"),
        pytest.param(dict, id="map"),
        pytest.param(None, id="http"),
    ]
)
def store(request, tmpdir):
    if request.param is open:
        return FileStore(Path(tmpdir))
    if request.param is dict:
        return {}
    if request.param is None:
        from bmst.wsgi import WsgiApp

        app = WsgiApp(BMST(meta={}, blobs={}))
        import wsgi_intercept

        wsgi_intercept.add_wsgi_intercept("test_host", 80, lambda: app)
        return Httplib2Store("http://test_host/blobs/")


def should_save(store):
    store[key] = b"test"
    assert key in store


def should_fail_on_del(store):
    if type(store) is dict:
        pytest.skip("del cant fail on dict")
    with pytest.raises(TypeError):
        del store[key]


def should_load(store):
    should_save(store)
    assert store[key] == b"test"


def should_list_items(store, tmpdir):
    should_save(store)

    assert list(store) == [key]


def should_fail_on_get_unknown(store):
    with pytest.raises(KeyError):
        store[key]
