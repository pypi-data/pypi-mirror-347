"""Periodic table."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pandas
import param
import plotly
import ptvis

from .exceptions import (
    ElementSymbolError,
    NegativeValueError,
    NonNumericalValueError,
    NonUniqueElementError,
)

if TYPE_CHECKING:
    from typing import Any


__all__ = ["PeriodicTable"]


class PeriodicTable(param.Parameterized):
    """Periodic table model."""

    data = param.DataFrame(default=pandas.DataFrame(), doc="Underlying data.")
    element_column = param.Selector(
        objects=[""],
        default="",
        doc="Name of a column containing element symbols.",
    )
    value_column = param.Selector(
        objects=[""],
        default="",
        doc="Name of a column containing target values.",
    )
    text_column = param.Selector(
        objects=[""],
        default="",
        doc="Name of a column containing texts for target values.",
    )
    template = param.ClassSelector(
        class_=plotly.graph_objects.layout.Template,
        default=None,
        doc="Figure template.",
    )
    cell_type = param.Selector(
        objects={
            "square": "square",
            "circle": "circle",
            "bubble": "bubble",
            "pie": "pie",
            "polar bar": "polar-bar",
        },
        default="square",
        doc="Type of a periodic table cell.",
    )
    numerical_color_palette = param.List(
        item_type=str,
        bounds=(2, None),
        default=plotly.colors.sequential.Viridis,
        doc="Color palette for numerical target values.",
    )
    non_numerical_color_palette = param.List(
        item_type=str,
        default=plotly.colors.qualitative.D3,
        doc="Color palette for non-numerical target values.",
    )
    text_colorway = param.List(item_type=str, default=None, doc="Colorway for texts.")

    def __init__(self, **params: Any) -> None:
        super().__init__()
        if "data" in params:
            self.data = params.pop("data")
        self.param.update(**params)

    @param.depends(  # type: ignore[misc]
        "element_column",
        "value_column",
        "text_column",
        "template",
        "cell_type",
        "numerical_color_palette",
        "non_numerical_color_palette",
        "text_colorway",
        # The 'data' parameter is not specified here not to trigger this method twice. A change of
        # the 'data' parameter triggers the '_update_column' method, where parameters on which this
        # method depends are changed.
    )
    def figure(self) -> plotly.graph_objects.Figure:
        """Make a figure of a periodic table."""
        fig = plotly.graph_objects.Figure()
        fig.update_layout(
            legend={"itemclick": False, "itemdoubleclick": False, "y": 0.5, "yanchor": "middle"},
        )
        if self.template is not None:
            fig.update_layout(template=self.template)
        fig.update_xaxes(constrain="domain")
        fig.update_yaxes(scaleanchor="x", scaleratio=1, constrain="domain")

        na_color = fig.layout.template.layout.plot_bgcolor

        if self.data is None or self.data.empty:
            elements = list(ptvis.Element)
            ptvis.attach_plain_cells(
                fig,
                elements,
                texts=[element.symbol for element in elements],
                text_colorway=self.text_colorway,
                colors=[na_color]*len(elements),
                color_conversion=ptvis.color.IdentityColorConversion(),
                tooltip={"color": False},
            )
            return fig

        is_valid_symbol = self.data[self.element_column].isin(
            {element.symbol for element in ptvis.Element}
        )
        if not is_valid_symbol.all():
            index = (~is_valid_symbol).idxmax()
            s = self.data[self.element_column].iat[index]
            raise ElementSymbolError(f"invalid element symbol '{s}'", text=s)

        elements = self.data[self.element_column].map(ptvis.Element.from_symbol).to_list()

        if self.value_column:
            values = self.data[self.value_column].to_list()
        else:
            values = [float("nan")] * len(elements)

        if self.text_column:
            texts = self.data[self.text_column].to_list()
        else:
            texts = [""] * len(elements)

        missing_elements = set(ptvis.Element) - set(elements)
        elements.extend(missing_elements)
        values.extend([float("nan")]*len(missing_elements))
        texts.extend([""]*len(missing_elements))

        is_numerical = pandas.api.types.is_any_real_numeric_dtype(pandas.Series(values))

        color_conversion: ptvis.color.BaseColorConversion
        if is_numerical:
            color_conversion = ptvis.color.ContinuousColorConversion(
                colors=self.numerical_color_palette,
                na_color=na_color,
            )
            color_guide = {
                "len": 360,
                "lenmode": "pixels",
                "outlinewidth": 0,
                "ticks": "outside",
            }
        else:
            color_conversion = ptvis.color.CategoricalColorConversion(
                missing_colors=self.non_numerical_color_palette,
                na_color=na_color,
            )
            color_guide = {
                "size": 12,
                "symbol": "square",
            }

        if self.cell_type in {"square", "circle"}:
            if not self.data[self.element_column].is_unique:
                raise NonUniqueElementError(
                    f"elements must be unique for cell type '{self.cell_type}'"
                )
            ptvis.attach_plain_cells(
                fig,
                elements,
                shape=self.cell_type,
                texts=[
                    f"{element.symbol}<br>{text}" if text else element.symbol
                    for element, text in zip(elements, texts)
                ],
                text_colorway=self.text_colorway,
                colors=values,
                color_conversion=color_conversion,
                color_guide=color_guide,
                tooltip={
                    "color": bool(self.value_column) and self.value_column != self.element_column,
                },
                labels={"color": self.value_column},
            )
        elif self.cell_type == "bubble":
            if not self.data[self.element_column].is_unique:
                raise NonUniqueElementError(
                    f"elements must be unique for cell type '{self.cell_type}'"
                )
            if not is_numerical:
                raise NonNumericalValueError(
                    f"value must be numerical for cell type '{self.cell_type}'"
                )
            if not all(0 <= v or math.isnan(v) for v in values):
                raise NegativeValueError(
                    f"value must be nonnegative for cell type '{self.cell_type}'"
                )
            ptvis.attach_plain_cells(
                fig,
                elements,
                shape="circle",
                areas=values,
                texts=[
                    f"{element.symbol}<br>{text}" if text else element.symbol
                    for element, text in zip(elements, texts)
                ],
                text_colorway=self.text_colorway,
                colors=values,
                color_conversion=color_conversion,
                color_guide=color_guide,
                tooltip={
                    "area": bool(self.value_column) and self.value_column != self.element_column,
                    "color": False,
                },
                labels={"area": self.value_column},
            )
        elif self.cell_type == "pie":
            if is_numerical:
                if not all(0 <= v or math.isnan(v) for v in values):
                    raise NegativeValueError(
                        f"numerical value must be nonnegative for cell type '{self.cell_type}'"
                    )
                ptvis.attach_pie_cells(
                    fig,
                    elements,
                    angles=values,
                    hole_diameter=1/3,
                    hole_texts={element: element.symbol for element in elements},
                    texts=texts,
                    text_colorway=self.text_colorway,
                    colors=values,
                    color_conversion=color_conversion,
                    color_guide=color_guide,
                    tooltip={
                        "angle": (
                            bool(self.value_column)
                            and self.value_column != self.element_column
                        ),
                        "color": False,
                    },
                    labels={"angle": self.value_column},
                    formats={"proportion": ":.1%"},
                )
            else:
                ptvis.attach_pie_cells(
                    fig,
                    elements,
                    hole_diameter=1/3,
                    hole_texts={element: element.symbol for element in elements},
                    texts=texts,
                    text_colorway=self.text_colorway,
                    colors=values,
                    color_conversion=color_conversion,
                    color_guide=color_guide,
                    tooltip={
                        "color": (
                            bool(self.value_column)
                            and self.value_column != self.element_column
                        ),
                    },
                    labels={"color": self.value_column},
                )
        elif self.cell_type == "polar-bar":
            if not is_numerical:
                raise NonNumericalValueError(
                    f"value must be numerical for cell type '{self.cell_type}'"
                )
            ptvis.attach_polar_bar_cells(
                fig,
                elements,
                values,
                hole_diameter=1/3,
                hole_texts={element: element.symbol for element in elements},
                texts=texts,
                text_colorway=self.text_colorway,
                colors=values,
                color_conversion=color_conversion,
                color_guide=color_guide,
                tooltip={
                    "radius": bool(self.value_column) and self.value_column != self.element_column,
                    "color": False,
                },
                labels={"radius": self.value_column},
            )
        else:
            raise ValueError(f"unexpected 'cell_type': {self.cell_type}")

        return fig

    @param.depends("data", watch=True)  # type: ignore[misc]
    def _update_columns(self) -> None:
        columns = self.data.columns.to_list() if self.data is not None else []

        self.param.element_column.objects = columns or [""]
        self.param.value_column.objects = columns or [""]
        self.param.text_column.objects = ["", *columns]

        self.param.update(
            element_column=self.param.element_column.objects[0],
            value_column=self.param.value_column.objects[0],
            text_column=self.param.text_column.objects[0],
        )
