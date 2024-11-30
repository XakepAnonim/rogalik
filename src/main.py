"""
Rogalik.
"""

import click

from config.log_tools import logger


@click.group()
def main() -> None:
    """
    Rogalik.
    """


@click.command(help="Start the server")
@click.option("--release", is_flag=True, help="Run in release mode")
@click.option("--log-level", default="info", help="Log level")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def server(release: str, log_level: str, reload: bool) -> None:
    """
    Start the server.
    """
    click.echo("Starting server...")
    logger.info("Starting server...")

    import uvicorn

    from config.settings import settings

    uvicorn_config = {
        "app": "config.app:server_init",
        "host": settings.host,
        "port": settings.port,
        "log_level": log_level,
        "reload": reload,
        "factory": True,
    }

    uvicorn.run(**uvicorn_config)


@click.command(help="Start the game client")
def client() -> None:
    """
    Start the Pygame client.
    """
    click.echo("Starting client...")
    logger.info("Starting client...")

    import asyncio

    import client.game

    asyncio.run(client.game.main())


@click.command(help="Run the tests")
@click.option("--enable-warnings", is_flag=True, help="Enable warnings")
def tests(enable_warnings: bool) -> None:
    """
    Run the tests.
    """
    click.echo("Running tests...")
    logger.info("Running tests...")

    import pytest

    args = ["-v", "tests"]
    if not enable_warnings:
        args.append("--disable-warnings")
    pytest.main(args)


main.add_command(server)
main.add_command(client)
main.add_command(tests)


if __name__ == "__main__":
    main()
