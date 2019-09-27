import json
from pathlib import Path

import click
import click_log

from bmst import log
from bmst.backup_app import make_backup
from bmst.managed import check_bmst
from bmst.utils import extract as internal_extract
from bmst.utils import get_bmst
from bmst.utils import sync as internal_sync


key_arg = click.argument("key")


@click.group()
@click_log.simple_verbosity_option(log)
@click.argument("store")
@click.pass_context
def main(ctx, store):
    ctx.obj = get_bmst(store)


@main.command()
@click.pass_obj
def check(obj):
    check_bmst(obj)


@main.command()
@click.pass_obj
@click.argument("target", nargs=-1)
def sync(obj, target):
    internal_sync(obj, target)


@main.command()
@click.pass_obj
def show(obj):
    import pprint

    pprint.pprint(list(obj.meta))


@main.command()
@click.pass_obj
@key_arg
@click.argument("target")
def extract(obj, key, target):
    internal_extract(obj, key, target)


@main.command()
@click.pass_obj
@click.argument("backup", nargs=-1)
def backup(obj, backup):
    for to_backup in backup:
        path = Path(to_backup)
        make_backup(root=path, bmst=obj)


@main.command()
@click.pass_obj
@key_arg
def ls(obj, key):
    print(json.dumps(obj.load_meta(key=key), indent=2, sort_keys=True))


@main.command()
def archive():
    raise NotImplementedError()


@main.command()
@click.pass_obj
@click.option("--listen", default="0.0.0.0:5000")
def serve(obj, listen):
    from bmst.wsgi import WsgiApp
    from waitress import serve

    app = WsgiApp(obj)
    serve(app, listen=listen)
