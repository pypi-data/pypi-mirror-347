# Optional v1.1 watchdog-based file watching
from collections.abc import Callable
from pathlib import Path

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
except ImportError:
    Observer = None


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[str, str], None]):
        self.callback = callback

    def on_any_event(self, event):
        self.callback(event.event_type, event.src_path)


def start_watch(path: Path, callback: Callable[[str, str], None]):
    if Observer is None:
        raise RuntimeError("watchdog not installed")
    obs = Observer()
    handler = ChangeHandler(callback)
    obs.schedule(handler, str(path), recursive=True)
    obs.start()
    return obs
