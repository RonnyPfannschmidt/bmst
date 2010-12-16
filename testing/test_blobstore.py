import py
from bmst import FileStore, MappingStore, Httplib2Store
from bmst.wsgi import StoreApp

def setup_module(mod):
    from wsgi_intercept.httplib2_intercept import install
    install()



key = py.std.hashlib.sha1('test').hexdigest()

def pytest_generate_tests(metafunc):
    if 'store' in metafunc.funcargnames:
        metafunc.addcall(id='file', param=file)
        metafunc.addcall(id='map', param=map)
        metafunc.addcall(id='http', param=None)

def pytest_funcarg__store(request):
    if request.param is file:
        return FileStore(request.getfuncargvalue('tmpdir'))
    if request.param is map:
        return MappingStore({})
    if request.param is None:
        store = MappingStore({})
        app = StoreApp(store)
        import wsgi_intercept
        wsgi_intercept.add_wsgi_intercept('test_host', 80, lambda: app)
        return Httplib2Store('http://test_host/')

    
def should_save(store):
    store[key] = 'test'
    assert key in store

def should_fail_on_del(store):
    with py.test.raises(TypeError):
        del store[key]

def should_load(store):
    should_save(store)
    assert store[key] == 'test'


def should_list_items(store, tmpdir):
    should_save(store)

    assert list(store) == [key]
