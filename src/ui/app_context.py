from dataclasses import dataclass

from src.audio.announcer import Announcer
from src.audio.audio_engine import AudioEngine
from src.persistence.app_state import AppState


@dataclass
class AppContext:
    app_state: AppState
    audio_engine: AudioEngine
    announcer: Announcer
    router: "object | None" = None  # set after Router is created
