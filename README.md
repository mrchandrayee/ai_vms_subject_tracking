# AI VMS — Track Down a Subject (Python reconstruction)

A runnable starter reconstruction of the visible video workflow: CCTV/video ingestion, YOLO object detection, ByteTrack IDs, annotated live view, event snapshots, CSV audit log, and a map panel for manually supplied camera/subject GPS coordinates.

## 1. Requirements
- Python 3.10 or 3.11 recommended
- For RTSP cameras, network access and valid camera credentials
- Optional NVIDIA CUDA setup for faster inference

## 2. Install
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Run
```bash
streamlit run main.py
```
Open the local Streamlit URL. Enter `0` for webcam, a video filename, or an RTSP URL. The first run downloads `yolov8n.pt` automatically if it is not present.

## 4. Multiple cameras
The dashboard UI runs one source at a time in this starter build. `cameras.example.json` shows the expected RTSP camera inventory format for extending it to a multi-camera grid. For independent simultaneous streams, run one worker per camera and merge event records by camera ID.

## 5. Outputs
- `data/events/subject_events.csv` — timestamp, camera, track ID, class and confidence
- `data/events/snapshots/` — event snapshots

## Important limitations
- This is a functional reconstruction from the visible screen and workflow, not a byte-for-byte extraction of the original source.
- The video does not provide original source files, private model weights, camera credentials, server/API configuration, or database schema.
- YOLO detects common COCO objects; it does not identify a particular person or perform cross-camera identity matching. Track IDs are local to a camera/session and can change.
- The map pin uses manually entered GPS coordinates. Standard CCTV video does not reveal geographic coordinates by itself.
- License-plate OCR, face recognition, cross-camera re-identification, and production-grade multi-camera orchestration are not included; they require dedicated models, lawful data handling, and additional integration.
