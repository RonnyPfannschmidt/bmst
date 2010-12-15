import py
from bmst import FileStore, MappingStore


def pytest_generate_tests(metafunc):
    if 'store' in metafunc.funcargnames:
        metafunc.addcall(id='file', param=file)
        metafunc.addcall(id='map', param=map)

def pytest_funcarg__store(request):
    if request.param is file:
        return FileStore(request.getfuncargvalue('tmpdir'))
    if request.param is map:
        return MappingStore({})

def test_store(store, tmpdir):
    key = py.std.hashlib.sha1('test').hexdigest()
    store.put(key, 'test')
    assert key in store



def test_get(store, tmpdir):
    key = py.std.hashlib.sha1('test').hexdigest()
    test_store(store, tmpdir)
    assert store.get(key) == 'test'

