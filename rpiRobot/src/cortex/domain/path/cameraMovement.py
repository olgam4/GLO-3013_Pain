from coordinate.cameraCoordinate import CameraCoordinate


class CameraMovement:
    def __init__(self, start: CameraCoordinate, stop: CameraCoordinate) -> None:
        self._start = start
        self._stop = stop

    @property
    def start(self) -> CameraCoordinate:
        return self._start

    @property
    def stop(self) -> CameraCoordinate:
        return self._stop

    def __repr__(self) -> str:
        return "{}({}=>{})".format(CameraMovement.__name__, self.start, self.stop)
