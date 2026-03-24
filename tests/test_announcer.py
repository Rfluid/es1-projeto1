from src.audio.announcer import Announcer


class FakeSpeechBackend:
    """Records all speak calls for assertion."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def speak(self, text: str) -> None:
        self.calls.append(text)


class TestAnnouncer:
    def test_announce_delegates_to_backend(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.announce("Combo 1")
        assert backend.calls == ["Combo 1"]

    def test_announce_strips_whitespace(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.announce("  lateral step  ")
        assert backend.calls == ["lateral step"]

    def test_announce_empty_string_ignored(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.announce("")
        assert backend.calls == []

    def test_announce_whitespace_only_ignored(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.announce("   ")
        assert backend.calls == []

    def test_announce_disabled(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.enabled = False
        announcer.announce("Combo 1")
        assert backend.calls == []

    def test_announce_re_enabled(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.enabled = False
        announcer.announce("Combo 1")
        announcer.enabled = True
        announcer.announce("Combo 2")
        assert backend.calls == ["Combo 2"]

    def test_enabled_default_true(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        assert announcer.enabled is True

    def test_multiple_announcements(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.announce("jab")
        announcer.announce("cross")
        announcer.announce("hook")
        assert backend.calls == ["jab", "cross", "hook"]
