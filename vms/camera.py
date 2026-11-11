import cv2

def open_source(source):
    # Numeric source means local webcam; otherwise source is a file path or RTSP/HTTP URL.
    if isinstance(source,str) and source.isdigit():
        source=int(source)
    cap=cv2.VideoCapture(source)
    if not cap.isOpened():
        cap.release()
        raise RuntimeError(f"Cannot open camera/source: {source}")
    return cap
