"""
UNICORNER • CameraStreamer
--------------------------
Thread-based frame grabber + JPEG encoder with live-tunable settings.

API
~~~
    cam = CameraStreamer(src=0, width=640, height=480, fps=30).open()

    jpg_bytes = cam.read()          # latest JPEG frame (thread-safe)
    for chunk in cam.frames():      # HTTP multipart generator
        ...

    cam.set_resolution(800, 600)    # change on the fly
    cam.set_fps(15)
    cam.set_source(1)               # switch camera / video / URL

    cam.release()                   # graceful shutdown
"""

from __future__ import annotations
import cv2, threading, time
from typing import Optional, Generator, Tuple


class CameraStreamer:
    def __init__(
        self,
        src:        int | str = 0,
        *,
        width:      Optional[int] = None,
        height:     Optional[int] = None,
        fps:        Optional[int] = None,
        jpeg_q:     int = 80,
    ) -> None:
        self.src, self.width, self.height, self.fps = src, width, height, fps
        self.jpeg_params = [cv2.IMWRITE_JPEG_QUALITY, jpeg_q]

        self._cap: Optional[cv2.VideoCapture] = None
        self._lock = threading.Lock()
        self._latest_frame: Optional[bytes] = None
        self._running = False
        self._t: Optional[threading.Thread] = None

    # ───────── public control ────────────────────────────────────────────────
    def open(self) -> "CameraStreamer":
        """Open the source, prime first frame, then start background reader."""
        self._cap = cv2.VideoCapture(self.src)
        if not self._cap.isOpened():
            raise RuntimeError(f"Cannot open video source: {self.src}")

        # apply optional capture settings
        if self.width  is not None: self._cap.set(cv2.CAP_PROP_FRAME_WIDTH,  self.width)
        if self.height is not None: self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        if self.fps    is not None: self._cap.set(cv2.CAP_PROP_FPS,          self.fps)

        # prime first frame
        ok, frame = self._cap.read()
        if not ok or frame is None:
            raise RuntimeError("Failed to read first frame from source")

        _, buf = cv2.imencode(".jpg", frame, self.jpeg_params)
        self._latest_frame = buf.tobytes()

        # start background reader
        self._running = True
        self._t = threading.Thread(target=self._reader, daemon=True)
        self._t.start()
        return self

    def release(self) -> None:
        """Stop reader thread & release capture."""
        self._running = False
        if self._t and self._t.is_alive():
            self._t.join(timeout=1)
        if self._cap:
            self._cap.release()
            self._cap = None

    # ───────── live setters ──────────────────────────────────────────────────
    def set_resolution(self, width: int, height: int) -> None:
        """Change capture resolution (best-effort)."""
        self.width, self.height = width, height
        if self._cap:
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH,  width)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def set_fps(self, fps: int) -> None:
        """Change requested FPS (best-effort)."""
        self.fps = fps
        if self._cap:
            self._cap.set(cv2.CAP_PROP_FPS, fps)

    def set_source(self, src: int | str) -> None:
        """Switch to a new camera / file / URL without dropping the thread."""
        self.release()
        self.src = src
        self.open()

    # ───────── frame accessors ───────────────────────────────────────────────
    def read(self) -> bytes:
        """
        Return the latest JPEG-encoded frame bytes.
        Raises if not yet running or no frame captured.
        """
        with self._lock:
            if not self._running or self._latest_frame is None:
                raise RuntimeError("No frame available. Did you call .open()?")
            return self._latest_frame

    def frames(self) -> Generator[bytes, None, None]:
        """HTTP-multipart generator suitable for Flask/Django streaming."""
        boundary = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
        while self._running:
            try:
                jpg = self.read()
            except RuntimeError:
                time.sleep(0.01)
                continue
            yield boundary + jpg + b"\r\n"
            time.sleep(0)  # yield to event loop

    # ───────── background loop ───────────────────────────────────────────────
    def _reader(self) -> None:
        while self._running and self._cap:
            ok, frame = self._cap.read()
            if not ok or frame is None:
                time.sleep(0.01)
                continue
            _, buf = cv2.imencode(".jpg", frame, self.jpeg_params)
            with self._lock:
                self._latest_frame = buf.tobytes()
