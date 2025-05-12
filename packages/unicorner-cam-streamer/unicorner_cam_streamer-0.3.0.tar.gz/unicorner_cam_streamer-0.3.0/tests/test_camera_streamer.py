import pytest, cv2, numpy as np
from unicorner_cam_streamer.camera_streamer import CameraStreamer


def test_open_and_release(monkeypatch):
    # Fake backend that opens but returns one black frame
    dummy = np.zeros((10, 10, 3), np.uint8)

    class FakeCap:
        def __init__(self, src): pass
        def isOpened(self): return True
        def read(self): return True, dummy
        def set(self, *a): pass
        def release(self): self.released = True

    monkeypatch.setattr(cv2, "VideoCapture", FakeCap)
    cs = CameraStreamer(src=0).open()
    assert cs.read()                # has bytes
    cs.release()
    assert cs._cap is None


def test_frames_generator(monkeypatch):
    dummy = np.zeros((5, 5, 3), np.uint8)

    class FakeCap:
        def __init__(self, src): pass
        def isOpened(self): return True
        def read(self): return True, dummy
        def set(self, *a): pass
        def release(self): pass

    monkeypatch.setattr(cv2, "VideoCapture", FakeCap)
    cs = CameraStreamer(src=0, fps=1).open()
    gen = cs.frames()
    chunk = next(gen)
    assert chunk.startswith(b"--frame") and b"image/jpeg" in chunk
    cs.release()


def test_dynamic_setters(monkeypatch):
    dummy = np.zeros((5, 5, 3), np.uint8)

    class FakeCap:
        def __init__(self, src): pass
        def isOpened(self): return True
        def read(self): return True, dummy
        def set(self, prop, val): setattr(self, f"_{prop}", val)
        def release(self): pass

    monkeypatch.setattr(cv2, "VideoCapture", FakeCap)
    cs = CameraStreamer(src=0).open()
    cs.set_resolution(320, 240)
    cs.set_fps(15)
    cs.set_source(1)    # switches source but still works
    assert cs.read()
    cs.release()
