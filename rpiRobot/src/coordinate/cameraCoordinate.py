class CameraCoordinate:
    def __init__(self, x_pos: float, y_pos: float):
        self._x_pos = x_pos
        self._y_pos = y_pos

    @property
    def x(self) -> float:
        return self._x_pos

    @property
    def y(self) -> float:
        return self._y_pos

    def __repr__(self) -> str:
        return "{}({},{})".format(CameraCoordinate.__name__, self.x, self.y)
