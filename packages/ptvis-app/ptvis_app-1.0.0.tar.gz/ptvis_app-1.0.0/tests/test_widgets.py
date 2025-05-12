from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import expect
import pytest

from ptvis_app.widgets import FileDropperWithTooltip

if TYPE_CHECKING:
    from panel.io.application import TViewable
    from playwright.sync_api import Locator, Page

    from conftest import ContextManagerFactory


@pytest.mark.gui
class TestFileDropperWithTooltip:

    def test_name(self, served_page: ContextManagerFactory[[TViewable], Page]) -> None:
        widget = FileDropperWithTooltip(name="initial")

        with served_page(widget) as page:
            self._assert_name(page, widget.name)

            # update
            widget.name = "updated"
            page.reload()

            self._assert_name(page, widget.name)

    def test_description(self, served_page: ContextManagerFactory[[TViewable], Page]) -> None:
        widget = FileDropperWithTooltip(description="initial")

        with served_page(widget) as page:
            tooltip_icon_locator = self._tooltip_icon_locator(page)

            # hover
            tooltip_icon_locator.hover()

            locator = self._tooltip_content_locator(page)
            expect(locator).to_have_text(widget.description)

            # unhover
            page.locator("body").hover()

            # update
            widget.description = "updated"

            # hover
            tooltip_icon_locator.hover()

            locator = self._tooltip_content_locator(page)
            expect(locator).to_have_text(widget.description)

    def test_upload(self, served_page: ContextManagerFactory[[TViewable], Page]) -> None:
        widget = FileDropperWithTooltip()

        with served_page(widget) as page:
            file_input_locator = self._file_input_locator(page)

            # upload
            file_name = "test.txt"
            file_input_locator.set_input_files(
                {"name": file_name, "mimeType": "text/plain", "buffer": b""}
            )

            expect(file_input_locator).to_have_value(fr"C:\fakepath\{file_name}")

    def test_accepted_filetypes(
        self,
        served_page: ContextManagerFactory[[TViewable], Page],
    ) -> None:
        widget = FileDropperWithTooltip(accepted_filetypes=["text/html"])

        with served_page(widget) as page:
            file_input_locator = self._file_input_locator(page)

            expect(file_input_locator).to_have_attribute(
                "accept",
                ",".join(widget.accepted_filetypes),
            )

            # update
            widget.accepted_filetypes = ["text/css"]
            page.reload()

            expect(file_input_locator).to_have_attribute(
                "accept",
                ",".join(widget.accepted_filetypes),
            )

    def test_stylesheets(self, served_page: ContextManagerFactory[[TViewable], Page]) -> None:
        selector = ".bk-description"
        property_name = "background-color"

        property_value = "rgb(255, 0, 0)"
        widget = FileDropperWithTooltip(
            stylesheets=[f"{selector} {{ {property_name}: {property_value}; }}"],
        )

        with served_page(widget) as page:
            name_locator = page.locator(selector)
            expect(name_locator).to_have_count(1)

            expect(name_locator).to_have_css(property_name, property_value)

            # update
            property_value = "rgb(0, 255, 0)"
            widget.stylesheets = [f"{selector} {{ {property_name}: {property_value}; }}"]
            page.reload()

            expect(name_locator).to_have_css(property_name, property_value)

    def _tooltip_icon_locator(self, page: Page) -> Locator:
        locator = page.locator(".bk-description")
        expect(locator).to_have_count(1)

        return locator

    def _tooltip_content_locator(self, page: Page) -> Locator:
        locator = page.locator(".bk-tooltip-content")
        expect(locator).to_have_count(1)

        return locator

    def _file_input_locator(self, page: Page) -> Locator:
        locator = page.locator(".filepond--browser")
        expect(locator).to_have_count(1)

        return locator

    def _assert_name(self, page: Page, expected: str) -> None:
        page.locator("div > div > div > label:has(.bk-description)").wait_for()
        page.wait_for_function(
            """
(expected) => {
    const element =
        document
        .querySelector('div > div')
        .shadowRoot
        .querySelector('div')
        .shadowRoot
        .querySelector('label:has(.bk-description)');
    const actual = window.getComputedStyle(element, '::before')['content'].slice(1, -1)
    return actual === expected;
}
""",
            arg=expected,
        )
