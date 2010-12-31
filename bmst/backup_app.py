

def load_tree(root):
    results = {}
    for x in root.visit():
        if x.check(file=1):
            results[x.relto(root)] = x.computehash('sha1'), x.read()
    return results
    results = {}
