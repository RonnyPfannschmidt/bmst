

def fullmeta(root):
    guessed = guessmeta(root)
    items = load_tree(root)

    item_meta = {}
    blobs = {}
    for k, (hash, content) in items.iteritems():
        item_meta[k] = hash
        # asume collisions are unlikely enough
        blobs[hash] = content

    guessed['items'] = item_meta
    return guessed, blobs


def guessmeta(root):
    return {
        'project': root.basename,
        'tags': ['backup'],
    }


def load_tree(root):
    results = {}
    for x in root.visit():
        if x.check(file=1):
            results[x.relto(root)] = x.computehash('sha1'), x.read()
    return results
    results = {}


def make_backup(root, bmst):
    meta, blobs = fullmeta(root)
    try:
        return bmst.put_meta(mapping=meta)
    except LookupError as e:
        missing_mapping = e.args[0]
        for key in missing_mapping.itervalues():
            bmst.put_blob(key=key, data=blobs[key])

        return bmst.put_meta(mapping=meta)
