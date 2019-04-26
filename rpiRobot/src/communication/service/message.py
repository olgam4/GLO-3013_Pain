import json
from typing import Any


class Message:
    def __init__(self, title: str, **kwargs) -> None:
        self._title = title
        self._data = {}
        for key, value in kwargs.items():
            self._data[key] = value

    @property
    def title(self) -> str:
        return self._title

    def get_data(self, key: str) -> Any:
        return self._data[key]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Message):
            return False
        if self.title != other.title:
            return False
        for key, value in self._data.items():
            if other.get_data(key) != value:
                return False
        return True

    def serialize(self) -> str:
        data = {"title": self._title}
        for key, value in self._data.items():
            data[key] = value
        return json.dumps(data)

    @classmethod
    def deserialize(cls, data_dump: str):
        data = json.loads(data_dump)
        title = data["title"]
        data.pop("title")
        return cls(title, **data)
