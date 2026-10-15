from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto


class EventType(Enum):
    MARKET = auto()
    SIGNAL = auto()
    ORDER = auto()
    FILL = auto()


class Event(ABC):
    __slots__ = ()

    @property
    @abstractmethod
    def event_type(self) -> EventType: ...

    @property
    @abstractmethod
    def timestamp(self) -> datetime: ...


@dataclass(frozen=True, slots=True)
class BarEvent(Event):
    symbol: str
    timestamp: datetime = field()
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int

    @property
    def event_type(self) -> EventType:
        return EventType.MARKET

    def __post_init__(self) -> None:
        if not self.symbol.strip():
            raise ValueError("Symbol cannot be empty or whitespace.")

        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise ValueError("Timestamp must be timezone-aware.")

        prices = {
            "open_price": self.open_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "close_price": self.close_price,
        }
        for name, value in prices.items():
            if value <= 0:
                raise ValueError(f"{name} cannot be non-positive.")

        if self.volume < 0:
            raise ValueError(f"Volume ({self.volume}) cannot be negative.")

        if self.high_price < self.low_price:
            raise ValueError(f"High price ({self.high_price}) cannot be less than low price ({self.low_price}).")

        if self.open_price < self.low_price or self.open_price > self.high_price:
            raise ValueError(f"Open price ({self.open_price}) must be between low price ({self.low_price}) and high price ({self.high_price}).")

        if self.close_price < self.low_price or self.close_price > self.high_price:
            raise ValueError(f"Close price ({self.close_price}) must be between low price ({self.low_price}) and high price ({self.high_price}).")
