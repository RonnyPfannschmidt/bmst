from __future__ import annotations

from dataclasses import dataclass

import orjson
from werkzeug.exceptions import NotFound
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response

from .managed import BMST

url_map = Map(
    [
        Rule("/", methods=("GET",), endpoint="list"),
        Rule("/<key>", methods=("GET",), endpoint="load"),
        Rule("/<key>", methods=("PUT",), endpoint="save"),
    ]
)


@dataclass
class WsgiApp:
    bmst: BMST

    @Request.application  # type: ignore
    def __call__(self, request):
        urls = url_map.bind_to_environ(request.environ)
        endpoint, args = urls.match()
        method = getattr(self, endpoint)
        return method(request, self.bmst.storage, **args)

    def list(self, request, store):
        return Response(orjson.dumps(list(store)), mimetype="application/json")

    def load(self, request, store, key):
        try:
            return Response(store[key])
        except KeyError:
            raise NotFound()

    def save(self, request, store, key):
        store[key] = request.data
        return Response(b"", status=204)
