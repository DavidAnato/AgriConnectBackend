import os
import threading
import time
import urllib.request
import urllib.error

_started = False


def _ping(url: str, timeout: int = 10) -> None:
    try:
        # 404 est acceptable: l’objectif est de générer une requête entrante
        with urllib.request.urlopen(url, timeout=timeout) as _:
            pass
    except Exception:
        # Silencieux: ne casse jamais le serveur
        pass


def start_keepalive(interval_seconds: int = 14 * 60) -> None:
    global _started
    if _started:
        return

    url = os.getenv("KEEPALIVE_URL") or os.getenv("RENDER_EXTERNAL_URL")
    if not url:
        return

    # Évite double slash
    url = url.rstrip("/") + "/"

    def worker() -> None:
        while True:
            _ping(url)
            time.sleep(interval_seconds)

    thread = threading.Thread(target=worker, name="keepalive-thread", daemon=True)
    thread.start()
    _started = True