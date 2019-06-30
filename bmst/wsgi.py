import json
import attr
from werkzeug.routing import Map, Rule, NotFound
from werkzeug.wrappers import Request, Response


url_map = Map([
    Rule("/<any(meta,blobs):kind>/", methods=("GET",), endpoint="list"),
    Rule("/<any(meta,blobs):kind>/<key>", methods=("GET",), endpoint="load"),
    Rule("/<any(meta,blobs):kind>/<key>", methods=("PUT",), endpoint="save"),
])


@attr.s
class WsgiApp:
    bmst = attr.ib()

    def _store(self, kind):
        return getattr(self.bmst, kind)

    @Request.application
    def __call__(self, request):
        urls = url_map.bind_to_environ(request.environ)
        endpoint, args = urls.match()
        method = getattr(self, endpoint)
        return method(request, self._store(args.pop("kind")), **args)

    def list(self, request, store):
        return Response(
            json.dumps(list(store)),
            mimetype="application/json")

    def load(self, request, store, key):
        try:
            return Response(store[key])
        except KeyError:
            raise NotFound()

    def save(self, request, store, key):
        store[key] = request.data
        return Response("", status=204)
