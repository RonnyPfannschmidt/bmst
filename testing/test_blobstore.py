import py
from bmst import FileStore, MappingStore

key = py.std.hashlib.sha1('test').hexdigest()

def pytest_generate_tests(metafunc):
    if 'store' in metafunc.funcargnames:
        metafunc.addcall(id='file', param=file)
        metafunc.addcall(id='map', param=map)

def pytest_funcarg__store(request):
    if request.param is file:
        return FileStore(request.getfuncargvalue('tmpdir'))
    if request.param is map:
        return MappingStore({})

def test_store(store):
    store[key] = 'test'
    assert key in store



def test_get(store):
    test_store(store)
    assert store[key] == 'test'


def test_iter(store, tmpdir):
    test_store(store)

    assert list(store) == [key]
