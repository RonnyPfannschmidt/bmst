import py
from bmst.managed import BMST, find_missing_blobs
import bz2


def pytest_funcarg__store(request):
    return BMST(blobs={}, meta={})


def should_fail_put_meta_on_missing_blob(store):

    with py.test.raises(LookupError) as excinfo:
        store.store_meta(mapping={
            'items': {
                'test': '123',
            },
        })
    assert excinfo.value[0] == {'test': '123'}


def should_put_meta_on_existing_blob(store):
    blob = store.store_blob(data=b'test')
    store.store_meta(mapping={
        'items': {
            'test': blob,
        },
    })


def should_find_missing_blobs():
    missing = find_missing_blobs({
        'items': {
            'test': 'foo',
        },
    }, {})

    assert missing == {'test': 'foo'}


def should_not_find_existing_blobs():
    missing = find_missing_blobs({
        'items': {
            'test': 'foo',
        },
    }, {'foo': 'yay'})
    assert missing is None
