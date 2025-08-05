import pprint
from pathlib import Path
from typing import Any

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
@click_log.simple_verbosity_option(log)  # type: ignore[misc]
@click.argument("store")
@click.pass_context
def main(ctx: click.Context, store: str) -> None:
    ctx.obj = get_bmst(store)


@main.command()
@click.pass_obj
def check(obj: Any) -> None:
    check_bmst(obj)


@main.command()
@click.pass_obj
@click.argument("target", nargs=-1)
def sync(obj: Any, target: tuple[str, ...]) -> None:
    internal_sync(obj, list(target))


@main.command()
@click.pass_obj
def show(obj: Any) -> None:
    pprint.pprint(list(obj.storage))


@main.command()
@click.pass_obj
@key_arg
@click.argument("target")
def extract(obj: Any, key: str, target: str) -> None:
    internal_extract(obj, key, target)


@main.command()
@click.pass_obj
@click.argument("backup", nargs=-1)
def backup(obj: Any, backup: tuple[str, ...]) -> None:
    for to_backup in backup:
        path = Path(to_backup)
        make_backup(root=path, bmst=obj)


@main.command()
@click.pass_obj
@key_arg
def ls(obj: Any, key: str) -> None:
    pprint.pprint(obj.load_meta(key=key))


@main.command()
def archive() -> None:
    raise NotImplementedError()


@main.command()
@click.pass_obj
@click.option("--listen", default="0.0.0.0:5000")
def serve(obj: Any, listen: str) -> None:
    from waitress import serve

    from bmst.wsgi import WsgiApp

    app = WsgiApp(obj)
    serve(app, listen=listen)  # type: ignore[arg-type]
