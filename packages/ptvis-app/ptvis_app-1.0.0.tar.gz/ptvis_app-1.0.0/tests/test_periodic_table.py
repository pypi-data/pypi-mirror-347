from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

import pandas
import pytest

from ptvis_app.exceptions import NonNumericalValueError
from ptvis_app.periodic_table import PeriodicTable

if TYPE_CHECKING:
    from contextlib import AbstractContextManager


class TestPeriodicTable:

    def test_default(self) -> None:
        periodic_table = PeriodicTable()

        assert periodic_table.data.empty
        assert periodic_table.element_column == ""
        assert periodic_table.value_column == ""
        assert periodic_table.text_column == ""

    def test_data_initialization(self) -> None:
        df = pandas.DataFrame({"a": [0], "b": [1]})

        periodic_table = PeriodicTable(data=df)

        assert periodic_table.param.element_column.objects == df.columns.to_list()
        assert periodic_table.param.value_column.objects == df.columns.to_list()
        assert periodic_table.param.text_column.objects == ["", *df.columns]

    def test_data_assignment(self) -> None:
        df = pandas.DataFrame({"a": [0], "b": [1]})

        periodic_table = PeriodicTable()
        periodic_table.data = df

        assert periodic_table.param.element_column.objects == df.columns.to_list()
        assert periodic_table.param.value_column.objects == df.columns.to_list()
        assert periodic_table.param.text_column.objects == ["", *df.columns]

    @pytest.mark.parametrize("cell_type", ["square", "circle", "bubble", "pie", "polar-bar"])
    def test_numerical_value_figure(self, cell_type: str) -> None:
        periodic_table = PeriodicTable(
            data=pandas.DataFrame({"element": ["H", "He"], "value": [0, 1]}),
            element_column="element",
            value_column="value",
            cell_type=cell_type,
        )

        periodic_table.figure()

    @pytest.mark.parametrize(
        ("cell_type", "expectation"),
        [
            ("square", contextlib.nullcontext()),
            ("circle", contextlib.nullcontext()),
            ("bubble", pytest.raises(NonNumericalValueError)),
            ("pie", contextlib.nullcontext()),
            ("polar-bar", pytest.raises(NonNumericalValueError)),
        ],
    )
    def test_non_numerical_value_figure(
        self,
        cell_type: str,
        expectation: AbstractContextManager[Exception | None],
    ) -> None:
        periodic_table = PeriodicTable(
            data=pandas.DataFrame({"element": ["H", "He"], "value": ["a", "b"]}),
            element_column="element",
            value_column="value",
            cell_type=cell_type,
        )

        with expectation:
            periodic_table.figure()
