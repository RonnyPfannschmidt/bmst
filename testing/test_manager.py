import py
from bmst.managed import Combined
from bmst import MappingStore
import bz2


def pytest_funcarg__mapping(request):
    return {}


def pytest_funcarg__store(request):
    return Combined(compression=bz2,
                     store=MappingStore,
                     root=request.getfuncargvalue('mapping'))

def should_fail_put_meta_on_missing_blob(store):

    with py.test.raises(LookupError) as excinfo:
        store.put_meta(mapping={
            'items': {
                'test': '123',
            },
        })


def should_put_meta_on_existing_blob(store, mapping):
    blob = store.put_blob(data='test')
    store.put_meta(mapping={
        'items': {
            'test': blob,
        },
    })

