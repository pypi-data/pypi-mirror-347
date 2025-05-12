"""Command-line interface."""

from __future__ import annotations

import argparse
import logging
import os.path
import sys
from typing import TYPE_CHECKING

import panel

from ._version import __version__
from .application import Application, configure
from .logging import Formatter, reset_logger

if TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Sequence


__all__ = ["main", "parse_arguments"]


def main(args: Sequence[str] | None = None) -> int:
    """Run a command.

    Parameters
    ----------
    args : sequence of str, optional
        Command-line arguments. If not specified, then `sys.argv` is used.

    Returns
    -------
    int
        Exit status.
    """
    ns = parse_arguments(args)

    configure_logging(ns.verbose)

    # prepare an application
    configure(theme=("dark" if ns.theme == "dark" else "default"))
    app = Application()

    # launch a server
    server = panel.serve(app, address=ns.address, port=ns.port, start=False, show=ns.open)
    print("Press Ctrl+C to stop server")
    server.start()
    server.io_loop.start()

    return 0


def parse_arguments(args: Sequence[str] | None = None) -> Namespace:
    """Parse command-line arguments.

    Parameters
    ----------
    args : sequence of str, optional
        Command-line arguments. If not specified, then `sys.argv` is used.

    Returns
    -------
    argparse.Namespace
        Result of parsing.
    """
    command_name = "ptvis-app"

    if os.path.basename(sys.argv[0]) == "__main__.py":
        package_name = __name__.split(".")[0]
        prog = f"python -m {package_name}"
    else:
        prog = command_name

    parser = argparse.ArgumentParser(
        prog=prog,
        allow_abbrev=False,
        add_help=False,
        description="Launch a web application for visualizing data on the periodic table.",
    )
    parser.add_argument("-a", "--address", help="Specify a hostname or IP address.")
    parser.add_argument("-h", "--help", action="help", help="Show this message and exit.")
    parser.add_argument(
        "--no-open",
        dest="open",
        action="store_false",
        help="Do not open an application after launching a server.",
    )
    parser.add_argument("-p", "--port", type=int, default=0, help="Specify a port number.")
    parser.add_argument(
        "-t",
        "--theme",
        choices=["dark", "light"],
        default="light",
        help="Specify a theme. The default is '%(default)s'.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help=(
            "Output log messages to the standard error. The verbosity level increases as the "
            "number of this option."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{command_name} {__version__}",
        help="Show the version number and exit.",
    )

    return parser.parse_args(args)


def configure_logging(verbose: int = 0) -> None:
    if verbose == 0:
        root_level = bokeh_level = panel_level = logging.WARNING
    elif verbose == 1:
        root_level = logging.WARNING
        bokeh_level = panel_level = logging.INFO
    elif verbose == 2:
        root_level = bokeh_level = panel_level = logging.INFO
    else:
        root_level = bokeh_level = panel_level = logging.DEBUG

    logging.basicConfig(level=root_level)

    for handler in logging.getLogger().handlers:
        handler.setFormatter(Formatter(fmt="[%(asctime)s] %(levelname)-8s: %(name)s: %(message)s"))

    reset_logger("bokeh", level=bokeh_level)
    reset_logger("panel", level=panel_level)
