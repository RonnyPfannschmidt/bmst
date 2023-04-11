import pytest

from bmst.managed import BMST
from bmst.managed import find_missing_items


@pytest.fixture
def store(request):
    return BMST(storage={})


def should_fail_put_meta_on_missing_item(store):
    with pytest.raises(LookupError) as excinfo:
        store.store_meta(mapping={"items": {"test": "123"}})
    assert excinfo.value.args[0] == {"test": "123"}


def should_put_meta_on_existing_blob(store):
    blob = store.store_blob(data=b"test")
    store.store_meta(mapping={"items": {"test": blob}})


def should_find_missing_blobs(store):
    missing = find_missing_items({"test": "foo"}, store.storage)

    assert missing == {"test": "foo"}


def should_not_find_existing_blobs(store):
    ref = store.store_blob(data=b"test")
    missing = find_missing_items(expected={"test": ref}, store=store.storage)
    assert missing == {}
