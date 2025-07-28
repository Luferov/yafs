import typer
from fast_clean.cli import use_cryptography, use_load_seed

from yafs.apps.storages.commands import add_s3_storage


def create_app() -> typer.Typer:
    app = typer.Typer()

    use_cryptography(app)
    use_load_seed(app)

    app.command()(add_s3_storage)

    return app
