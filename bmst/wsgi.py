import json
from .managed import BMST


import flask

app = flask.Flask('bmst')


@app.route('/<any(meta,blobs):kind>/', methods=('GET',))
def listing(kind):
    store = getattr(app.bmst, kind)
    return json.dumps(store.keys())


@app.route('/<any(meta,blobs):kind>/<key>', methods=('GET', 'PUT',))
def data(kind, key):
    store = getattr(app.bmst, kind)
    print store, flask.request.method
    if flask.request.method == 'GET':
        try:
            return store[key]
        except KeyError:
            flask.abort(404)
    else:
        store[key] = flask.request.data
        return '', 204
