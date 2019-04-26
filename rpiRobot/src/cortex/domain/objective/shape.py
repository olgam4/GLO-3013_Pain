from enum import Enum


class Shape(Enum):
    NoShape = 0
    Triangle = 1
    Square = 2
    Pentagon = 3
    Circle = 4
    
    @classmethod
    def get_from(cls, shape_string: str):
        if shape_string == 'triangle':
            return Shape.Triangle
        elif shape_string == 'carre':
            return Shape.Square
        elif shape_string == 'pentagone':
            return Shape.Pentagon
        elif shape_string == 'cercle':
            return Shape.Circle
        else:
            return Shape.NoShape
