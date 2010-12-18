import bmst.metastore


def should_find_missing_blobs():
    store = bmst.MappingStore({})
    missing = bmst.metastore.find_missing_blobs({
        'items': {
            'test': 'foo',
        },
    }, store)

    assert missing == {'test': 'foo'}


def should_not_find_existing_blobs():
    store = bmst.MappingStore({'foo': 'yay'}, update=True)
    missing = bmst.metastore.find_missing_blobs({
        'items': {
            'test': 'foo',
        },
    }, store)
    assert missing is None
