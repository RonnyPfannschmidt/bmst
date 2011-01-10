import py
from bmst.managed import BMST
import bz2


def pytest_funcarg__store(request):
    return BMST(blobs={}, meta={})


def should_fail_put_meta_on_missing_blob(store):

    with py.test.raises(LookupError) as excinfo:
        store.put_meta(mapping={
            'items': {
                'test': '123',
            },
        })


def should_put_meta_on_existing_blob(store):
    blob = store.put_blob(data=b'test')
    store.put_meta(mapping={
        'items': {
            'test': blob,
        },
    })
