from enum import Enum


class Color(Enum):
    NoColor = 0
    Red = 1
    Green = 2
    Blue = 3
    Yellow = 4

    @classmethod
    def get_from(cls, color_string: str):
        if color_string == 'rouge':
            return Color.Red
        elif color_string == 'vert':
            return Color.Green
        elif color_string == 'bleu':
            return Color.Blue
        elif color_string == 'orange':
            return Color.Yellow
        else:
            return Color.NoColor
