import asyncio

import typer

from sidekick import config, session, ui
from sidekick.repl import repl
from sidekick.setup import setup
from sidekick.utils.system import check_for_updates

app = typer.Typer(help=config.NAME)


@app.command()
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit."),
    logfire_enabled: bool = typer.Option(False, "--logfire", help="Enable Logfire tracing."),
    no_telemetry: bool = typer.Option(
        False, "--no-telemetry", help="Disable telemetry collection."
    ),
    run_setup: bool = typer.Option(False, "--setup", help="Run setup process."),
):
    if version:
        asyncio.run(ui.version())
        return

    asyncio.run(ui.banner())

    has_update, latest_version = check_for_updates()
    if has_update:
        asyncio.run(ui.show_update_message(latest_version))

    if no_telemetry:
        session.telemetry_enabled = False

    try:
        asyncio.run(setup(run_setup))
        asyncio.run(repl())
    except Exception as e:
        asyncio.run(ui.error(str(e)))


if __name__ == "__main__":
    app()
