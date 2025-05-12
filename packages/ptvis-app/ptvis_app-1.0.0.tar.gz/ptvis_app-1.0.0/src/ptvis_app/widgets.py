"""Widgets."""

from __future__ import annotations

from typing import TYPE_CHECKING

import panel.theme
import param

if TYPE_CHECKING:
    from typing import Any


__all__ = ["FileDropperWithTooltip"]


class FileDropperWithTooltip(panel.widgets.base.WidgetBase, panel.custom.PyComponent):
    """FileDropper with a tooltip."""

    name = param.String(default="", doc="Name of a widget.")
    description = param.String(default="", doc="Description shown in a tooltip.")
    accepted_filetypes = param.List(default=[], doc="Accepted file types.")
    value = param.Dict(default={}, doc="Uploaded files.")
    width = param.Integer(bounds=(0, None), allow_None=True, default=300, doc="Width of a widget.")

    _file_dropper = param.ClassSelector(class_=panel.widgets.FileDropper, allow_refs=False)

    def __init__(self, **params: Any) -> None:
        params.setdefault("margin", (5, 10))
        params["_file_dropper"] = panel.widgets.FileDropper(
            name="",
            width=None,
            margin=0,
            sizing_mode="stretch_width",
            design=panel.theme.Design,
        )
        super().__init__(**params)

        self._label = panel.widgets.TooltipIcon.from_param(
            self.param.description,
            margin=0,
            align="start",
        )

        self._update_label_stylesheets()
        self._update_file_dropper_accepted_filetypes()
        self._update_file_dropper_stylesheets()

    def __panel__(self) -> panel.Column:
        return panel.Column(self._label, self._file_dropper)

    @param.depends("name", "stylesheets", watch=True)  # type: ignore[misc]
    def _update_label_stylesheets(self) -> None:
        name = self.name or self.__class__.__name__
        self._label.stylesheets = [f"label::before {{ content: '{name}'; }}", *self.stylesheets]

    @param.depends("accepted_filetypes", watch=True)  # type: ignore[misc]
    def _update_file_dropper_accepted_filetypes(self) -> None:
        self._file_dropper.accepted_filetypes = self.accepted_filetypes

    @param.depends("_file_dropper.accepted_filetypes", watch=True)  # type: ignore[misc]
    def _update_accepted_filetypes(self) -> None:
        self.accepted_filetypes = self._file_dropper.accepted_filetypes

    @param.depends("_file_dropper.value", watch=True)  # type: ignore[misc]
    def _update_value(self) -> None:
        with param.parameterized.discard_events(self):
            self.value = self._file_dropper.value
        self.param.trigger("value")

    @param.depends("stylesheets", watch=True)  # type: ignore[misc]
    def _update_file_dropper_stylesheets(self) -> None:
        self._file_dropper.stylesheets = [
            """
.bk-input.filepond--root {
  background-color: var(--design-surface-color, var(--panel-surface-color, #f1f1f1));
}

.bk-input.filepond--root .filepond--drop-label {
  background-color: var(--design-surface-color, var(--panel-surface-color, #f1f1f1));
  color: var(--design-surface-text-color, var(--panel-on-surface-color, #000000));
}
""",
            *self.stylesheets,
        ]
