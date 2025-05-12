"""Application."""

from __future__ import annotations

import importlib.resources
import io
import logging
import re
from typing import TYPE_CHECKING

import colorcet
import pandas
import panel
import param
import plotly
import wclr

from .exceptions import (
    ElementSymbolError,
    NegativeValueError,
    NonNumericalValueError,
    NonUniqueElementError,
)
from .periodic_table import PeriodicTable
from .utils import extend_list_param, update_dict_param
from .widgets import FileDropperWithTooltip

if TYPE_CHECKING:
    from typing import Any, Literal


__all__ = ["Application", "configure"]


_logger = logging.getLogger(__name__)


_FAVICON = importlib.resources.files("ptvis_app").joinpath("static").joinpath("favicon.svg")


def configure(theme: Literal["dark", "default"] = "default") -> None:
    """Configure applications.

    Parameters
    ----------
    theme : {'dark', 'default'}, optional
        Theme of an application.
    """
    panel.extension("filedropper", "plotly", theme=theme)


class Application(panel.viewable.Viewer):
    """Application viewer."""

    numerical_color_palettes = param.Dict(
        default={
            "bgy": colorcet.b_linear_bgy_10_95_c74,
            "kbgoy": colorcet.b_linear_kbgoy_20_95_c57,
            "kgy": colorcet.b_linear_kgy_5_95_c69,
            "gow": colorcet.b_linear_gow_65_90_c35,
            "bmw": colorcet.b_linear_bmw_5_95_c89,
            "bmy": colorcet.b_linear_bmy_10_95_c78,
            "kry": colorcet.b_linear_kry_5_95_c72,
            "kbw-cbs": colorcet.b_linear_protanopic_deuteranopic_kbw_5_95_c34,
            "bwr": colorcet.b_diverging_bwr_20_95_c54,
            "bjr": colorcet.b_diverging_linear_bjr_30_55_c53,
            "bkr": colorcet.b_diverging_bkr_55_10_c35,
            "bwy-cbs": colorcet.b_diverging_protanopic_deuteranopic_bwy_60_95_c32,
            "bjy": colorcet.b_diverging_linear_bjy_30_90_c45,
            "bjy-cbs": colorcet.b_diverging_linear_protanopic_deuteranopic_bjy_57_89_c34,
            "kbjyw-cbs": colorcet.b_linear_protanopic_deuteranopic_kbjyw_5_95_c25,
            "bky": colorcet.b_diverging_bky_60_10_c30,
            "bgymr": colorcet.b_diverging_rainbow_bgymr_45_85_c67,
            "bgyr": colorcet.b_rainbow_bgyr_10_90_c83,
            "kw": colorcet.b_linear_grey_10_95_c0,
        },
        doc="Color palettes for numerical values. A key is a label. A value is an array of colors.",
    )
    non_numerical_color_palettes = param.Dict(
        default={
            "category10": colorcet.b_glasbey_category10[:10],
            "hv": colorcet.b_glasbey_hv[:10],
            "dark": colorcet.glasbey_dark[:10],
            "warm": colorcet.glasbey_warm[:10],
            "cool": colorcet.glasbey_cool[:10],
            "cbs": ["#005aff", "#f6aa00", "#03af7a", "#804000", "#fff100", "#4dc4ff"],
        },
        doc=(
            "Color palettes for non-numerical values. A key is a label. A value is an array of "
            "colors."
        ),
    )
    color_swatch_width = param.Integer(
        bounds=(1, None),
        default=150,
        doc="Width of a color swatch in px.",
    )
    sidebar_width = param.Integer(bounds=(1, None), default=300, doc="Width of a sidebar in px.")

    _periodic_table = param.ClassSelector(class_=PeriodicTable)
    _upload_widget = param.ClassSelector(class_=FileDropperWithTooltip, allow_refs=False)

    def __init__(self, **params: Any) -> None:
        params["_periodic_table"] = PeriodicTable()
        params["_upload_widget"] = FileDropperWithTooltip(
            name="File",
            description="""
<ul>
  <li>Must be a CSV file encoded in UTF-8.</li>
  <li>The first line must consist of column names.</li>
</ul>
""",
            accepted_filetypes=["text/csv"],
        )
        super().__init__(**params)

        self._figure_pane = panel.pane.Plotly(
            plotly.graph_objects.Figure(),
            config={"displayModeBar": False, "doubleClick": False, "showAxisDragHandles": False},
        )

        self._error_pane = panel.pane.Alert("", alert_type="danger")

        download_box_label = panel.pane.HTML("Save as")

        download_widgets = []
        stem = "ptvis-app"
        download_widgets.append(
            panel.widgets.FileDownload(
                label="HTML",
                filename=f"{stem}.html",
                callback=(
                    lambda p=self._figure_pane: _figure_to_html_stream(p.object, config=p.config)
                ),
            ),
        )
        download_widgets.extend(
            panel.widgets.FileDownload(
                label=label,
                filename=f"{stem}{ext}",
                callback=lambda p=self._figure_pane, f=fmt: _figure_to_image_stream(p.object, f),
            )
            for label, ext, fmt in [
                ("JPEG", ".jpg", "jpeg"),
                ("PDF", ".pdf", "pdf"),
                ("PNG", ".png", "png"),
                ("SVG", ".svg", "svg"),
            ]
        )

        # The '_download_box' attribute must be assigned before updating the '_periodic_table'
        # parameter.
        self._download_box = panel.WidgetBox(
            download_box_label,
            *sorted(download_widgets, key=lambda widget: widget.label),
        )

        self._periodic_table.param.update(
            numerical_color_palette=next(iter(self.numerical_color_palettes.values())),
            non_numerical_color_palette=next(iter(self.non_numerical_color_palettes.values())),
            text_colorway=["#000000", "#ffffff"],
        )

        # components for data
        data_box_label = panel.pane.HTML("<h2>Data</h2>")
        element_column_widget = panel.widgets.Select.from_param(
            self._periodic_table.param.element_column,
            name="Element column",
            description="A column must consist of element symbols, e.g., H, He, and Li.",
        )
        value_column_widget = panel.widgets.Select.from_param(
            self._periodic_table.param.value_column,
            name="Value column",
            description=None,
        )
        text_column_widget = panel.widgets.Select.from_param(
            self._periodic_table.param.text_column,
            name="Text column",
            description=None,
        )

        # components for styles
        style_box_label = panel.pane.HTML("<h2>Style</h2>")
        cell_type_widget = panel.widgets.Select.from_param(
            self._periodic_table.param.cell_type,
            name="Cell type",
            description="""
<ul>
  <li>The <i>square</i> and <i>circle</i> types represent values as colors.</li>
  <li>The <i>bubble</i> type represents values as areas and colors.</li>
  <li>
    The <i>pie</i> type represents numerical values as angles and colors, and non-numerical values
    as colors.
  </li>
  <li>The <i>polar bar</i> type represents values as radii and colors.</li>
</ul>
""",
        )
        numerical_color_palette_widget = panel.widgets.ColorMap.from_param(
            self._periodic_table.param.numerical_color_palette,
            name="Color palette for numerical values",
            options=self.numerical_color_palettes,
            swatch_width=self.param.color_swatch_width,
        )
        non_numerical_color_palette_widget = panel.widgets.ColorMap.from_param(
            self._periodic_table.param.non_numerical_color_palette,
            name="Color palette for non-numerical values",
            options=self.non_numerical_color_palettes,
            swatch_width=self.param.color_swatch_width,
        )

        # structure components
        data_box = panel.WidgetBox(
            data_box_label,
            self._upload_widget,
            element_column_widget,
            value_column_widget,
            text_column_widget,
        )
        style_box = panel.WidgetBox(
            style_box_label,
            cell_type_widget,
            numerical_color_palette_widget,
            non_numerical_color_palette_widget,
        )
        self._main = [panel.FlexBox(self._download_box, self._figure_pane, self._error_pane)]
        self._sidebar = [data_box, style_box]

        # style a main box
        self._main[0].param.update(
            flex_direction="column",
            flex_wrap="nowrap",
            align_items="center",
            sizing_mode="stretch_both",
        )

        # style a download box
        self._download_box.param.update(horizontal=True, scroll=True, align="center")
        update_dict_param(self._download_box.param.styles, {"flex": "none"})

        # style a download box label
        download_box_label.align = "center"  # type: ignore[assignment]
        update_dict_param(download_box_label.param.styles, {"font-weight": "bold"})

        # style download widgets
        for widget in download_widgets:
            widget.align = "center"  # type: ignore[assignment]
            extend_list_param(widget.param.stylesheets, ["a { font-size: var(--font-size); }"])

        # style a figure pane
        self._figure_pane.sizing_mode = "stretch_both"

        # style an error pane
        self._error_pane.visible = False

        # style boxes in a sidebar area
        for box in {data_box, style_box}:
            box.margin = (5, 0)  # type: ignore[assignment]

        # style a data box label
        extend_list_param(data_box_label.param.stylesheets, ["h2 { margin: 0; }"])

        # style an upload widget
        self._upload_widget.param.update(
            description=re.sub(
                "<ul.*?>",
                "<ul style='padding-inline-start: 1em;'>",
                self._upload_widget.description,
            ),
            sizing_mode="stretch_width",
        )
        extend_list_param(
            self._upload_widget.param.stylesheets,
            [".bk-description { transform: scale(0.75); }"],
        )

        # style column widgets
        for widget in {element_column_widget, value_column_widget, text_column_widget}:
            widget.sizing_mode = "stretch_width"

        # style a style box label
        extend_list_param(style_box_label.param.stylesheets, ["h2 { margin: 0; }"])

        # style a cell type widget
        cell_type_widget.param.update(
            description=re.sub(
                "<ul.*?>",
                "<ul style='padding-inline-start: 1em;'>",
                cell_type_widget.description,
            ),
            sizing_mode="stretch_width",
        )

        # style color palette widgets
        for widget in {numerical_color_palette_widget, non_numerical_color_palette_widget}:
            widget.sizing_mode = "stretch_width"
            extend_list_param(
                widget.param.stylesheets,
                [".bk-input + div { background-color: var(--mdc-theme-background); }"],
            )

    def __panel__(self) -> Template:
        # clear an uploaded file so as to be consistent with the appearance of the widget
        self._upload_widget.value = {}

        view = Template(
            title="PTVis App",
            main=self._main,
            sidebar=self._sidebar,
            sidebar_width=self.sidebar_width,
        )

        is_dark_theme = panel.config.theme == "dark"

        background_color = "#212529" if is_dark_theme else "#ffffff"

        # CSS color variables
        view.config.raw_css = [
            # design variables
            f"""
:root {{
  --design-primary-color: #b0c6ff;
  --design-primary-text-color: #152e60;
  --design-secondary-color: #404659;
  --design-secondary-text-color: #dce2f9;
  --design-background-color: {background_color};
  --design-background-text-color: #ffffff;
  --design-surface-color: #121318;
  --design-surface-text-color: #e2e2e9;
}}
"""
            if is_dark_theme else
            f"""
:root {{
  --design-primary-color: #475d91;
  --design-primary-text-color: #ffffff;
  --design-secondary-color: #dce2f9;
  --design-secondary-text-color: #404659;
  --design-background-color: {background_color};
  --design-background-text-color: #212529;
  --design-surface-color: #faf8ff;
  --design-surface-text-color: #1a1b20;
}}
""",
            # menu icon
            """
#header .mdc-top-app-bar__navigation-icon {
  color: var(--header-color);
}
""",
            # title
            """
#header .title {
  color: var(--mdc-theme-on-surface);
  font-weight: bold;
}
""",
        ]

        # header area
        view.header_background = "#2e4578" if is_dark_theme else "#d9e2ff"
        view.header_color = "#d9e2ff" if is_dark_theme else "#2e4578"

        # busy indicator
        bgcolor, color = ("dark", "light") if is_dark_theme else ("light", "dark")
        view.busy_indicator.param.update(bgcolor=bgcolor, color=color)

        # figure template
        figure_template = plotly.graph_objects.layout.Template(
            plotly.io.templates["plotly_dark" if is_dark_theme else "plotly_white"],
        )
        figure_template.layout.update(
            paper_bgcolor=background_color,
            plot_bgcolor=background_color,
        )
        self._periodic_table.template = figure_template

        return view

    @param.depends("_upload_widget.value", watch=True)  # type: ignore[misc]
    def _update_periodic_table_data(self) -> None:
        self._periodic_table.data = _text_to_dataframe(
            next(iter(self._upload_widget.value.values()), "")
        )

    @param.depends("_periodic_table.figure", watch=True)  # type: ignore[misc]
    def _update_main_area(self) -> None:
        try:
            fig = self._periodic_table.figure()
        except Exception as exc:
            message = self._make_error_message(exc)
            if message is None:
                _logger.exception("unexpected error occured")
                message = "An unexpected error occured. See the log for details."

            with panel.io.hold():
                self._error_pane.object = f"<h2>Error</h2>\n{message}"
                self._figure_pane.visible = False
                self._error_pane.visible = True
                self._download_box.visible = False

            return

        fig.update_layout(margin={"l": 0, "r": 0, "b": 0, "t": 0}, dragmode=False)

        # convert colors to the rgb function style for downloaded files
        for trace in fig.select_traces(selector="scatter"):
            for parent_attr, color_attr in [
                (trace.textfont, "color"),
                (trace.hoverlabel, "bgcolor"),
                (trace.hoverlabel.font, "color"),
                (trace.hoverlabel, "bordercolor"),
            ]:
                colors = getattr(parent_attr, color_attr)
                if colors is not None:
                    setattr(
                        parent_attr,
                        color_attr,
                        [
                            wclr.Color.from_str(color).to_rgb_function_str(percentage=False)
                            for color in colors
                        ],
                    )

        with panel.io.hold():
            self._figure_pane.object = fig
            self._figure_pane.visible = True
            self._error_pane.visible = False
            self._download_box.visible = True

    def _make_error_message(self, exc: BaseException) -> str | None:
        """Make a displayed message for an error.

        Parameters
        ----------
        exc : BaseException
            Source of a message.

        Returns
        -------
        str or None
            Message. ``None`` for an unexpected `exc`.
        """
        if type(exc) is ElementSymbolError:
            if exc.text is not None:
                return (
                    f"An item '{exc.text}' in the '{self._periodic_table.element_column}' column "
                    "is not an element symbol."
                )
            else:
                return (
                    f"An item in the '{self._periodic_table.element_column}' column is not an "
                    "element symbol."
                )
        elif type(exc) is NonUniqueElementError:
            label = next(
                k
                for k, v in self._periodic_table.param.cell_type.objects.items()
                if v == self._periodic_table.cell_type
            )
            return f"The cell type must not be '{label}' for non-unique elements."
        elif type(exc) is NonNumericalValueError:
            label = next(
                k
                for k, v in self._periodic_table.param.cell_type.objects.items()
                if v == self._periodic_table.cell_type
            )
            return f"The cell type must not be '{label}' for non-numerical values."
        elif type(exc) is NegativeValueError:
            label = next(
                k
                for k, v in self._periodic_table.param.cell_type.objects.items()
                if v == self._periodic_table.cell_type
            )
            return f"The cell type must not be '{label}' for values containing negative numbers."
        else:
            return None


class Template(panel.template.MaterialTemplate):
    """Application template.

    A favicon is read from package resources.
    """

    def _update_vars(self, *args: Any) -> None:
        with importlib.resources.as_file(_FAVICON) as path:
            self.favicon = str(path)
            super()._update_vars(*args)


def _text_to_dataframe(text: str | bytes) -> pandas.DataFrame:
    """Convert a CSV text to pandas.DataFrame object.

    Parameters
    ----------
    text : str or bytes
        CSV text to be converted. The first line must consist of column names. If of type ``bytes``,
        then the UTF-8 encoding is assumed.

    Returns
    -------
    pandas.DataFrame
        Constructed object.
    """
    if isinstance(text, bytes):
        text = str(text, encoding="utf-8")

    try:
        with io.StringIO(text) as f:
            df = pandas.read_csv(f, header=0)
    except pandas.errors.EmptyDataError:
        df = pandas.DataFrame()

    return df


def _figure_to_html_stream(
    fig: plotly.graph_objects.Figure,
    config: dict[str, Any] | None = None,
) -> io.StringIO:
    """Convert a figure object to a HTML stream.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        Figure object to be converted.
    config : dict, optional
        Configuration options. Passed to the `plotly.graph_objects.Figure.write_html` method.

    Returns
    -------
    io.StringIO
        HTML stream. Positioned at the start of the stream.
    """
    fig = plotly.graph_objects.Figure(fig)
    fig.update_layout(width=None, height=None)

    stream = io.StringIO()
    fig.write_html(stream, config=config)

    stream.seek(0)

    return stream


def _figure_to_image_stream(fig: plotly.graph_objects.Figure, fmt: str) -> io.BytesIO:
    """Convert a figure object to an image stream.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        Figure object to be converted.
    fmt : str
        Format of an image.

    Returns
    -------
    io.BytesIO
        Image stream. Positioned at the start of the stream.
    """
    full_fig = fig.full_figure_for_development(warn=False)
    width = full_fig.layout.width
    height = (
        full_fig.layout.font.size
        + (
            (full_fig.layout.yaxis.domain[1]-full_fig.layout.yaxis.domain[0])
            * full_fig.layout.height
        )
    )

    colorbar_trace = next(
        fig.select_traces(selector=lambda trace: trace.marker.colorbar.len),
        None,
    )
    if colorbar_trace:
        height = max(height, colorbar_trace.marker.colorbar.len)

    stream = io.BytesIO()
    fig.write_image(stream, format=fmt, width=width, height=height)

    stream.seek(0)

    return stream
