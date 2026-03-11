"""Helper utilities for the BetterStack Uptime API."""

from __future__ import annotations

from typing import Any, TypeVar

T = TypeVar("T")


def filter_on_attribute(objects: list[T], attribute: str, value: Any) -> list[T]:
    """Filter a list of objects by attribute value.

    This function filters a list of objects, returning only those where
    the specified attribute matches the given value.

    Args:
        objects: List of objects to filter.
        attribute: Name of the attribute to check.
        value: Value the attribute should match.

    Returns:
        A filtered list containing only objects where the attribute matches.

    Example:
        >>> monitors = [monitor1, monitor2, monitor3]
        >>> paused_monitors = filter_on_attribute(monitors, "paused", True)
    """
    return [obj for obj in objects if getattr(obj, attribute, None) == value]
