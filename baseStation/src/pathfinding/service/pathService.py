from pathfinding.domain.path import Path


class PathService:
    def __init__(self) -> None:
        self._path = Path([])

    def set_path(self, data: str) -> None:
        self._path = Path.deserialize(data)

    def get_path(self) -> Path:
        return self._path
