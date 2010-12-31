

def fullmeta(root):
    guessed = guessmeta(root)
    items = load_tree(root)

    item_meta = {}
    blobs = []
    for k, (hash, content) in items.iteritems():
        item_meta[k] = hash
        blobs.append((hash, content))

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
