from .managed import sha1


def fullmeta(root):
    meta, blobs = basemeta(root)
    meta.update(guessmeta(root))
    return meta, blobs


def basemeta(root):
    items, mtime = load_tree(root)

    item_meta = {}
    blobs = {}
    for k, (hash, content) in items.items():
        item_meta[k] = hash
        # assume collisions are unlikely enough
        blobs[hash] = content

    return {"items": item_meta, "timestamp": mtime}, blobs


def guessmeta(root):
    return {"project": root.name, "tags": ["backup"]}


def load_tree(root):
    results = {}
    mtime = 0
    for x in root.rglob("*"):
        if x.is_file():
            data = x.read_bytes()
            content_hash = sha1(data)
            results[str(x.relative_to(root))] = content_hash, data
        mtime = max(mtime, x.stat().st_mtime)
    return results, mtime


def make_backup(root, bmst):
    key = inner_make_backup(root, bmst)
    bmst.add_root(key)


def inner_make_backup(root, bmst):
    print("backing up", root)
    meta, blobs = fullmeta(root)
    try:
        return bmst.store_meta(mapping=meta)
    except LookupError as e:
        missing_mapping = e.args[0]
        for key in missing_mapping.values():
            bmst.store_blob(key=key, data=blobs[key])

        return bmst.store_meta(mapping=meta)
