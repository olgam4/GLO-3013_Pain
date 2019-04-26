class TimeDTO:
    def __init__(self, time_value: float) -> None:
        self._time_value = time_value

    @property
    def value(self) -> str:
        return str(self._time_value)

    def __str__(self) -> str:
        timestamp = int(self._time_value)
        hours = timestamp // 3600
        timestamp -= hours * 3600
        minutes = timestamp // 60
        timestamp -= minutes * 60
        seconds = timestamp
        return "{}:{:02}:{:02}".format(hours, minutes, seconds)
