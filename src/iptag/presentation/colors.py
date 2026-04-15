"""Deterministic color assignment for category labels."""

import hashlib

# Curated palette: readable on both dark and light terminals, and distinct
# enough when rendered as HTML background colors.
_PALETTE: tuple[tuple[str, str], ...] = (
    ("bright_cyan", "#8ecae6"),
    ("bright_magenta", "#ffafcc"),
    ("bright_green", "#b7e4c7"),
    ("bright_yellow", "#ffe066"),
    ("bright_blue", "#a0c4ff"),
    ("bright_red", "#ffadad"),
    ("cyan", "#90e0ef"),
    ("magenta", "#cdb4db"),
    ("green", "#a7c957"),
    ("yellow", "#fcbf49"),
)


def _palette_index(label: str) -> int:
    digest = hashlib.sha1(label.encode("utf-8")).digest()
    return digest[0] % len(_PALETTE)


def terminal_color(label: str) -> str:
    """Return a stable `rich` color name for a category label."""
    return _PALETTE[_palette_index(label)][0]


def html_color(label: str) -> str:
    """Return a stable hex color for a category label."""
    return _PALETTE[_palette_index(label)][1]


def css_class(label: str) -> str:
    """Return a CSS-safe class name for a category label."""
    safe = "".join(c if c.isalnum() else "-" for c in label.lower())
    return f"cat-{safe}"
