def find_missing_blobs(data, blobstore):
    keys = set(blobstore.keys())
    missing = {}
    for name, value in data['items'].items():
        if value not in keys:
            missing[name] = value
    if missing:
        # cause we want None else
        return missing
