import bmst.metastore


def should_find_missing_blobs():
    missing = bmst.metastore.find_missing_blobs({
        'items': {
            'test': 'foo',
        },
    }, {})

    assert missing == {'test': 'foo'}


def should_not_find_existing_blobs():
    missing = bmst.metastore.find_missing_blobs({
        'items': {
            'test': 'foo',
        },
    }, {'foo': 'yay'})
    assert missing is None
