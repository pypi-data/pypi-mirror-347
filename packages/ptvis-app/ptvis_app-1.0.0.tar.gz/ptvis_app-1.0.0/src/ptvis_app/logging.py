"""Logging utilities."""

from __future__ import annotations

import datetime
import logging
from typing import TYPE_CHECKING

import dateutil.tz

if TYPE_CHECKING:
    from logging import Logger, LogRecord


__all__ = ["Formatter", "reset_logger"]


class Formatter(logging.Formatter):
    """Log record formatter.

    The ``asctime`` attribute of the `LogRecord` object is formatted by the
    `datetime.datetime.strftime` method. The default is the ISO 8601 format.
    """

    def formatTime(self, record: LogRecord, datefmt: str | None = None) -> str:
        """Format a creation time of a log record."""
        dt = datetime.datetime.fromtimestamp(record.created, tz=dateutil.tz.tzlocal())
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.isoformat(timespec="milliseconds")


def reset_logger(name: str, level: int | str = logging.WARNING) -> Logger:
    """Reset a logger.

    Parameters
    ----------
    name : str
        Name of a logger.
    level : int or str, optional
        Logging level set to a logger.

    Returns
    -------
    logging.Logger
        Logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # remove all filters
    while logger.filters:
        logger.removeFilter(logger.filters[0])

    # remove all handlers
    while logger.handlers:
        logger.removeHandler(logger.handlers[0])

    logger.propagate = True

    return logger
