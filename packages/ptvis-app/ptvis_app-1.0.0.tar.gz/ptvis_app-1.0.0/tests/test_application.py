from __future__ import annotations

import contextlib
import io
from typing import TYPE_CHECKING

import pandas
from playwright.sync_api import expect
import pytest

from ptvis_app.application import Application, configure

if TYPE_CHECKING:
    from collections.abc import Iterator
    from contextlib import AbstractContextManager

    from panel.io.application import TViewable
    from playwright.sync_api import FilePayload, Locator, Page

    from conftest import ContextManagerFactory


@pytest.mark.gui
class TestApplication:

    @pytest.fixture(autouse=True)
    def setup(self, served_page: ContextManagerFactory[[TViewable], Page]) -> Iterator[None]:
        configure()
        app = Application()
        with served_page(app):
            yield

    @pytest.fixture
    def file_locator(self, page: Page) -> Locator:
        locator = page.get_by_label("Drag & Drop your files or Browse", exact=True)
        expect(locator).to_have_count(1)

        return locator

    @pytest.fixture
    def element_column_locator(self, page: Page) -> Locator:
        locator = page.get_by_role("combobox", name="Element column", exact=True)
        expect(locator).to_have_count(1)

        return locator

    @pytest.fixture
    def value_column_locator(self, page: Page) -> Locator:
        locator = page.get_by_role("combobox", name="Value column", exact=True)
        expect(locator).to_have_count(1)

        return locator

    @pytest.fixture
    def text_column_locator(self, page: Page) -> Locator:
        locator = page.get_by_role("combobox", name="Text column", exact=True)
        expect(locator).to_have_count(1)

        return locator

    @pytest.fixture
    def cell_type_locator(self, page: Page) -> Locator:
        locator = page.get_by_role("combobox", name="Cell type", exact=True)
        expect(locator).to_have_count(1)

        return locator

    @pytest.fixture
    def numerical_color_palette_locator(self, page: Page) -> Locator:
        locator = (
            page
            .get_by_text("Color palette for numerical values", exact=True)
            .locator("+ *")
        )
        expect(locator).to_have_count(1)

        return locator

    @pytest.fixture
    def non_numerical_color_palette_locator(self, page: Page) -> Locator:
        locator = (
            page
            .get_by_text("Color palette for non-numerical values", exact=True)
            .locator("+ *")
        )
        expect(locator).to_have_count(1)

        return locator

    @pytest.fixture
    def save_box_locator(self, page: Page) -> Locator:
        locator = page.locator("main .panel-widget-box", has_text="Save as")
        expect(locator).to_have_count(1)

        return locator

    @pytest.fixture
    def figure_locator(self, page: Page) -> Locator:
        locator = page.locator("main .plotly")
        expect(locator).to_have_count(1)

        return locator

    @pytest.fixture
    def error_locator(self, page: Page) -> Locator:
        locator = page.locator("main .alert")
        expect(locator).to_have_count(1)

        return locator

    @pytest.fixture
    def wait_for_figure_update(self, figure_locator: Locator) -> AbstractContextManager[None]:
        @contextlib.contextmanager
        def _factory() -> Iterator[None]:
            before = figure_locator.inner_html()

            yield

            figure_locator.page.wait_for_function(
                """
(before) => {
    const element =
        document
        .querySelector('main > div > div')
        .shadowRoot
        .querySelector('.bk-panel-models-plotly-PlotlyPlot')
        .shadowRoot
        .querySelector('.plotly');
    const after = element.innerHTML;
    return after !== before;
}
""",
                arg=before,
            )

        return _factory()

    def test_initial(
        self,
        file_locator: Locator,
        element_column_locator: Locator,
        value_column_locator: Locator,
        text_column_locator: Locator,
        save_box_locator: Locator,
        figure_locator: Locator,
        error_locator: Locator,
    ) -> None:
        expect(file_locator).to_have_value("")

        expect(element_column_locator.get_by_role("option")).to_have_count(1)
        expect(element_column_locator).to_have_value("")

        expect(value_column_locator.get_by_role("option")).to_have_count(1)
        expect(value_column_locator).to_have_value("")

        expect(text_column_locator.get_by_role("option")).to_have_count(1)
        expect(text_column_locator).to_have_value("")

        expect(save_box_locator).to_be_visible()
        expect(figure_locator).to_be_visible()
        expect(error_locator).not_to_be_visible()

    def test_upload(
        self,
        file_locator: Locator,
        element_column_locator: Locator,
        value_column_locator: Locator,
        text_column_locator: Locator,
        wait_for_figure_update: AbstractContextManager[None],
    ) -> None:
        name = "test.csv"
        df = pandas.DataFrame({"element": ["H"], "x": [0]})

        with wait_for_figure_update:
            # upload
            file_locator.set_input_files(self._make_input_file(name, df))

        expect(element_column_locator.get_by_role("option")).to_have_count(len(df.columns))
        expect(element_column_locator).to_have_value(df.columns[0])

        expect(value_column_locator.get_by_role("option")).to_have_count(len(df.columns))
        expect(value_column_locator).to_have_value(df.columns[0])

        expect(text_column_locator.get_by_role("option")).to_have_count(1+len(df.columns))
        expect(text_column_locator).to_have_value("")

    @pytest.mark.parametrize("cell_type", ["square", "circle", "bubble", "pie", "polar bar"])
    def test_numerical_value_cell_type(
        self,
        file_locator: Locator,
        element_column_locator: Locator,
        value_column_locator: Locator,
        cell_type_locator: Locator,
        save_box_locator: Locator,
        figure_locator: Locator,
        error_locator: Locator,
        wait_for_figure_update: AbstractContextManager[None],
        cell_type: str,
    ) -> None:
        name = "test.csv"
        element_column = "element"
        value_column = "value"
        df = pandas.DataFrame({element_column: ["H"], value_column: [0]})

        # upload
        file_locator.set_input_files(self._make_input_file(name, df))

        # select data columns
        element_column_locator.select_option(label=element_column)
        value_column_locator.select_option(label=value_column)

        cm = (
            wait_for_figure_update
            if cell_type != cell_type_locator.input_value() else
            contextlib.nullcontext()
        )
        with cm:
            # change a cell type
            cell_type_locator.select_option(label=cell_type)

        expect(save_box_locator).to_be_visible()
        expect(figure_locator).to_be_visible()
        expect(error_locator).not_to_be_visible()

    @pytest.mark.parametrize(
        ("cell_type", "expect_success"),
        [
            ("square", True),
            ("circle", True),
            ("bubble", False),
            ("pie", True),
            ("polar bar", False),
        ],
    )
    def test_non_numerical_value_cell_type(
        self,
        file_locator: Locator,
        element_column_locator: Locator,
        value_column_locator: Locator,
        cell_type_locator: Locator,
        save_box_locator: Locator,
        figure_locator: Locator,
        error_locator: Locator,
        wait_for_figure_update: AbstractContextManager[None],
        cell_type: str,
        expect_success: bool,
    ) -> None:
        name = "test.csv"
        element_column = "element"
        value_column = "value"
        df = pandas.DataFrame({element_column: ["H"], value_column: ["a"]})

        # upload
        file_locator.set_input_files(self._make_input_file(name, df))

        # select data columns
        element_column_locator.select_option(label=element_column)
        value_column_locator.select_option(label=value_column)

        cm = (
            wait_for_figure_update
            if expect_success and cell_type != cell_type_locator.input_value() else
            contextlib.nullcontext()
        )
        with cm:
            # change a cell type
            cell_type_locator.select_option(label=cell_type)

        if expect_success:
            expect(save_box_locator).to_be_visible()
            expect(figure_locator).to_be_visible()
            expect(error_locator).not_to_be_visible()
        else:
            expect(save_box_locator).not_to_be_visible()
            expect(figure_locator).not_to_be_visible()
            expect(error_locator).to_be_visible()

    def test_numerical_color_palette(
        self,
        file_locator: Locator,
        element_column_locator: Locator,
        value_column_locator: Locator,
        numerical_color_palette_locator: Locator,
        wait_for_figure_update: AbstractContextManager[None],
    ) -> None:
        name = "test.csv"
        element_column = "element"
        value_column = "value"
        df = pandas.DataFrame({element_column: ["H"], value_column: [0]})

        # upload
        file_locator.set_input_files(self._make_input_file(name, df))

        # select data columns
        element_column_locator.select_option(label=element_column)
        value_column_locator.select_option(label=value_column)

        with wait_for_figure_update:
            # change a color palette
            numerical_color_palette_locator.click()
            numerical_color_palette_locator.locator("+ * .bk-item").nth(1).click()

    def test_non_numerical_color_palette(
        self,
        file_locator: Locator,
        element_column_locator: Locator,
        value_column_locator: Locator,
        non_numerical_color_palette_locator: Locator,
        wait_for_figure_update: AbstractContextManager[None],
    ) -> None:
        name = "test.csv"
        element_column = "element"
        value_column = "value"
        df = pandas.DataFrame({element_column: ["H"], value_column: [0]})

        # upload
        file_locator.set_input_files(self._make_input_file(name, df))

        # select data columns
        element_column_locator.select_option(label=element_column)
        value_column_locator.select_option(label=value_column)

        with wait_for_figure_update:
            # change a color palette
            non_numerical_color_palette_locator.click()
            non_numerical_color_palette_locator.locator("+ * .bk-item").nth(1).click()

    @pytest.mark.parametrize(
        ("button_text", "ext"),
        [("HTML", ".html"), ("JPEG", ".jpg"), ("PDF", ".pdf"), ("PNG", ".png"), ("SVG", ".svg")],
    )
    def test_download(self, save_box_locator: Locator, button_text: str, ext: str) -> None:
        button_locator = save_box_locator.get_by_text(button_text, exact=True)
        expect(button_locator).to_have_count(1)

        with button_locator.page.expect_download(lambda d: d.suggested_filename.endswith(ext)):
            button_locator.click()

    def _make_input_file(self, name: str, df: pandas.DataFrame) -> FilePayload:
        with io.BytesIO() as f:
            df.to_csv(f, index=False)
            f.seek(0)
            return {"name": name, "mimeType": "text/csv", "buffer": f.read()}
