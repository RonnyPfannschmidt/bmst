import py
from bmst.store import FileStore, Httplib2Store
from bmst.managed import BMST

key = py.std.hashlib.sha1("test").hexdigest()


def setup_module(mod):
    from wsgi_intercept.httplib2_intercept import install

    install()


def pytest_generate_tests(metafunc):
    if "store" in metafunc.funcargnames:
        metafunc.addcall(id="file", param=file)
        metafunc.addcall(id="map", param=dict)
        metafunc.addcall(id="http", param=None)


def pytest_funcarg__store(request):
    if request.param is file:
        return FileStore(request.getfuncargvalue("tmpdir"))
    if request.param is dict:
        return {}
    if request.param is None:
        from bmst.wsgi import app

        app.bmst = BMST(meta={}, blobs={})
        import wsgi_intercept

        wsgi_intercept.add_wsgi_intercept("test_host", 80, lambda: app)
        return Httplib2Store("http://test_host/blobs/")


def should_save(store):
    store[key] = "test"
    assert key in store


def should_fail_on_del(store):
    if type(store) is dict:
        py.test.skip("del cant fail on dict")
    with py.test.raises(TypeError):
        del store[key]


def should_load(store):
    should_save(store)
    assert store[key] == "test"


def should_list_items(store, tmpdir):
    should_save(store)

    assert list(store) == [key]


def should_fail_on_get_unknown(store):
    with py.test.raises(KeyError):
        store[key]
