import py
from bmst import FileStore

def pytest_funcarg__store(request):
    return FileStore(request.getfuncargvalue('tmpdir'))

def test_put(store, tmpdir):
    hash = py.std.hashlib.sha1('test').hexdigest()
    key = store.put(hash, 'test')
    assert tmpdir.join(hash).check()



def test_get(store, tmpdir):
    hash = py.std.hashlib.sha1('test').hexdigest()
    test_put(store, tmpdir)
    assert store.get(hash) == 'test'

