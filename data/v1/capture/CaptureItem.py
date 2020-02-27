from attr import dataclass


@dataclass
class CaptureItem:
    url: str
    startTime: int
    endTime: int
    subtitle: str