"""Utility functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping
    from typing import Any

    from param import Dict, List


__all__ = ["extend_list_param", "update_dict_param"]


def extend_list_param(p: List, it: Iterable[Any]) -> None:
    """Extend a list parameter.

    This function triggers dependencies on the given parameter.

    Parameters
    ----------
    p : param.List
        List parameter.
    it : iterable
        Extending items.
    """
    value = getattr(p.owner, p.name)
    value = value.copy() if value is not None else []

    value.extend(it)

    setattr(p.owner, p.name, value)


def update_dict_param(p: Dict, m: Mapping[Any, Any]) -> None:
    """Update a dict parameter.

    This function triggers dependencies on the given parameter.

    Parameters
    ----------
    p : param.Dict
        Dict parameter.
    m : mapping
        Updating items.
    """
    value = getattr(p.owner, p.name)
    value = value.copy() if value is not None else {}

    value.update(m)

    setattr(p.owner, p.name, value)
