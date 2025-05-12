from __future__ import annotations

import datetime
import logging

from ptvis_app.logging import Formatter


class TestFormatter:

    def test_default_datefmt(self) -> None:
        formatter = Formatter(fmt="%(asctime)s")
        asctime = formatter.format(logging.LogRecord("", 0, "", 1, "", None, None))

        datetime.datetime.fromisoformat(asctime)
