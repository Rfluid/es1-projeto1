from typing import Protocol


class SpeechBackend(Protocol):
    """Protocol for text-to-speech playback.

    In the browser this is implemented via the Speech Synthesis API.
    In tests this is replaced by a mock/fake.
    """

    def speak(self, text: str) -> None: ...


class Announcer:
    """Announces combo/move names via voice synthesis (RN06).

    Delegates actual speech output to a SpeechBackend,
    keeping announcement logic testable without a browser.
    """

    def __init__(self, backend: SpeechBackend) -> None:
        self._backend = backend
        self._enabled = True

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value

    def announce(self, text: str) -> None:
        if not self._enabled:
            return
        cleaned = text.strip()
        if not cleaned:
            return
        self._backend.speak(cleaned)
