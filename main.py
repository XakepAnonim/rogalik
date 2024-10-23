import click


@click.group()
def cli():
    """
    CLI.
    """


@click.command(help="Start the server")
@click.option("--release", is_flag=True, help="Run in release mode")
@click.option("--log-level", default="info", help="Log level")
def server(release: bool, log_level: str):
    """
    Start the server.
    """
    click.echo("Starting server...")

    import uvicorn

    from rogalik.server import create_server

    app = create_server(debug=not release)
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level=log_level,
    )


@click.command(help="Run the game client")
def client():
    """
    Run the Pygame client.
    """
    click.echo("Starting client...")

    import pygame_client.game

    pygame_client.game.main()


@click.command(help="Run the tests")
@click.option("--enable-warnings", is_flag=True, help="Enable warnings")
def tests(enable_warnings: bool):
    """
    Run the tests.
    """
    click.echo("Running tests...")

    import pytest

    args = ["-v", "tests"]
    if not enable_warnings:
        args.append("--disable-warnings")
    pytest.main(args)


cli.add_command(server)
cli.add_command(client)
cli.add_command(tests)

if __name__ == "__main__":
    cli()
