"""
Represents a color object.
"""

from dataclasses import dataclass, field


@dataclass
class Color:
    """
    A class to represent a color.
    """

    primary: str = field(default="#000000")
    secondary: str = field(default="#000000")
    text: str = field(default="#000000")


def parse_color(data: dict) -> Color:
    """
    Parse the color data.

    Args:
        data (dict): The color data.

    Returns:
        Color: The color object.
    """
    return Color(
        primary=data.get("primary", "#000000"),
        secondary=data.get("secondary", "#000000"),
        text=data.get("text", "#000000"),
    )
