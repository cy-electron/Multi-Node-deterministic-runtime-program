from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from runtime.errors import RuntimeErrorReason
from .event import ExecutionEvent


@dataclass(frozen=True)
class LoggedEvent:
    sequence: int
    event: ExecutionEvent

    def canonical(self) -> dict[str, object]:
        data = self.event.canonical()
        data["sequence"] = self.sequence
        return data


class ExecutionLog:
    """Append-only execution history with deterministic sequence numbers."""

    def __init__(self) -> None:
        self._entries: list[LoggedEvent] = []
        self._sealed = False

    def append(self, event: ExecutionEvent) -> LoggedEvent:
        if self._sealed:
            raise RuntimeErrorReason("execution log is sealed")
        entry = LoggedEvent(sequence=len(self._entries) + 1, event=event)
        self._entries.append(entry)
        return entry

    def seal(self) -> None:
        self._sealed = True

    def __iter__(self) -> Iterator[LoggedEvent]:
        return iter(tuple(self._entries))

    def __len__(self) -> int:
        return len(self._entries)

    def entries(self) -> tuple[LoggedEvent, ...]:
        return tuple(self._entries)

    def events(self) -> tuple[ExecutionEvent, ...]:
        return tuple(entry.event for entry in self._entries)

    def canonical(self) -> list[dict[str, object]]:
        return [entry.canonical() for entry in self._entries]
