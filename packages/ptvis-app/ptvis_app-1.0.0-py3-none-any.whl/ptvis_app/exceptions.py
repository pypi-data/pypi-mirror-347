"""Exceptions."""

from __future__ import annotations


__all__ = [
    "ApplicationError",
    "ElementSymbolError",
    "NegativeValueError",
    "NonNumericalValueError",
    "NonUniqueElementError",
]


class ApplicationError(Exception):
    """Error in an application."""


class ElementSymbolError(ApplicationError):
    """Error for an invalid element symbol.

    Parameters
    ----------
    *args
        Passed to the initializer of the parent class.
    text : str, optional
        Invalid element symbol.
    """

    def __init__(self, *args: object, text: str | None = None) -> None:
        super().__init__(*args)
        self.text = text


class NonUniqueElementError(ApplicationError):
    """Error for a non-unique element collection."""


class NonNumericalValueError(ApplicationError):
    """Error for a non-numerical value."""


class NegativeValueError(ApplicationError):
    """Error for a nonnegative value."""
