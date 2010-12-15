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
