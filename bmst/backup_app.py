import py


def fullmeta(root):
    guessed = guessmeta(root)
    items = load_tree(root)

    item_meta = {}
    blobs = {}
    for k, (hash, content) in items.items():
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
            results[x.relto(root)] = x.computehash('sha1'), x.read('rb')
    return results
    results = {}


def make_backup(root, bmst):
    meta, blobs = fullmeta(root)
    try:
        return bmst.put_meta(mapping=meta)
    except LookupError as e:
        missing_mapping = e.args[0]
        for key in missing_mapping.values():
            bmst.put_blob(key=key, data=blobs[key])

        return bmst.put_meta(mapping=meta)


def main():
    if len(sys.argv) == 2:
        config = py.iniconfig.IniConfig(sys.argv[1])
    else:
        config = py.iniconfig.IniConfig('bmst.ini')
