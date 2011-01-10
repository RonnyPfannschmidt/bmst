
import collections


def find_missing_blobs(data, blobstore):
    missing = {}
    for name, value in data['items'].items():
        if value not in blobstore:
            missing[name] = value
    if missing:
        # cause we want None else
        return missing
