"""fileprompt CLI – launched with `fileprompt` (or `uvx fileprompt`)."""

from __future__ import annotations

import importlib
import threading
import time
import webbrowser

import typer
import uvicorn

APP_MODULE = "fileprompt"  # FastAPI instance lives at fileprompt:app
DEFAULT_HOST = "127.0.0.1"  # DO NOT expose on 0.0.0.0
DEFAULT_PORT = 8000

cli = typer.Typer(add_completion=False, help="Run the FilePrompt web UI.")


def _start_browser(url: str, delay: float = 1.0) -> None:
    def _open():
        time.sleep(delay)
        webbrowser.open(url)

    threading.Thread(target=_open, daemon=True).start()


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    port: int = typer.Option(DEFAULT_PORT, "-p", "--port", help=f"Port to bind to (host fixed to {DEFAULT_HOST})"),
    no_browser: bool = typer.Option(False, "--no-browser", help="Don't launch a browser tab."),
) -> None:
    """Launch the FastAPI server behind the FilePrompt UI."""
    if ctx.invoked_subcommand is not None:
        return  # another sub-command was called

    # Import routes so they register with the FastAPI app
    importlib.import_module("fileprompt.main")

    url = f"http://{DEFAULT_HOST}:{port}"
    if not no_browser:
        _start_browser(url)
    print(f"Running FilePrompt at {url}")
    uvicorn.run(
        APP_MODULE + ":app",
        host=DEFAULT_HOST,
        port=port,
        reload=False,
        log_level="warning",
    )
