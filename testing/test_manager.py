import pytest

from bmst.managed import BMST
from bmst.managed import find_missing_blobs


@pytest.fixture
def store(request):
    return BMST(blobs={}, meta={})


def should_fail_put_meta_on_missing_blob(store):

    with pytest.raises(LookupError) as excinfo:
        store.store_meta(mapping={"items": {"test": "123"}})
    assert excinfo.value[0] == {"test": "123"}


def should_put_meta_on_existing_blob(store):
    blob = store.store_blob(data=b"test")
    store.store_meta(mapping={"items": {"test": blob}})


def should_find_missing_blobs():
    missing = find_missing_blobs({"test": "foo"}, {})

    assert missing == {"test": "foo"}


def should_not_find_existing_blobs():
    missing = find_missing_blobs(expected={"test": "foo"}, store={"foo": "yay"})
    assert missing is None
