"""FightDrill — Entry point for PyScript."""

from src.audio.announcer import Announcer
from src.audio.audio_engine import AudioEngine
from src.audio.web_backends import WebAudioPlayer, WebSpeechBackend
from src.persistence.app_state import AppState
from src.persistence.storage_manager import StorageManager
from src.persistence.web_backend import LocalStorageBackend
from src.ui.app_context import AppContext
from src.ui.pages import (
    ComboDrillPage,
    ComboLibraryPage,
    CustomWorkoutPage,
    FootworkDrillPage,
    FootworkMovePage,
    HomePage,
    RoundTimerPage,
    TimingDrillPage,
)
from src.ui.router import Router

# --- Bootstrap ---

storage = StorageManager(LocalStorageBackend())
app_state = AppState(storage)
loaded = app_state.load()

audio_engine = AudioEngine(WebAudioPlayer())
announcer = Announcer(WebSpeechBackend())

router = Router("app")
ctx = AppContext(
    app_state=app_state, audio_engine=audio_engine, announcer=announcer, router=router
)

# --- Routes ---

router.register("/", lambda: HomePage(ctx))
router.register("/round-timer", lambda: RoundTimerPage(ctx))
router.register("/timing-drill", lambda: TimingDrillPage(ctx))
router.register("/combo-drill", lambda: ComboDrillPage(ctx))
router.register("/footwork-drill", lambda: FootworkDrillPage(ctx))
router.register("/combo-library", lambda: ComboLibraryPage(ctx))
router.register("/footwork-moves", lambda: FootworkMovePage(ctx))
router.register("/custom-workouts", lambda: CustomWorkoutPage(ctx))

# --- Start ---

if not loaded and app_state.load_error:
    from js import window  # type: ignore[import-not-found]

    window.alert(
        f"Dados corrompidos no localStorage. Estado resetado.\n\n{app_state.load_error}"
    )

router.start()
