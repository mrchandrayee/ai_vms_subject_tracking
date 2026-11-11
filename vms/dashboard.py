import streamlit as st
import cv2, time, pandas as pd
from pathlib import Path
from .detector import SubjectDetector, annotate
from .camera import open_source
from .events import save_event, CSV_PATH
from .config import SNAPSHOT_DIR

def _map_panel(lat, lon):
    try:
        import folium
        from streamlit_folium import st_folium
        m=folium.Map(location=[lat,lon],zoom_start=14)
        folium.Marker([lat,lon],tooltip="Last known subject location",
                      popup="Manually supplied GPS coordinate").add_to(m)
        st_folium(m,height=350,width=None)
    except Exception as exc:
        st.info(f"Map component unavailable: {exc}")

def run_app():
    st.title("AI VMS — Track Down a Subject")
    st.caption("Multi-camera detection • persistent track IDs • event snapshots • location map")
    with st.sidebar:
        st.header("Camera / video source")
        source=st.text_input("Video file, webcam index, or RTSP URL", value="0")
        weights=st.text_input("YOLO weights",value="yolov8n.pt")
        conf=st.slider("Detection confidence",0.05,0.95,0.35,0.05)
        frame_skip=st.number_input("Process every Nth frame",1,10,1)
        st.divider()
        st.subheader("Subject location (optional)")
        lat=st.number_input("Latitude",value=12.9716,format="%.6f")
        lon=st.number_input("Longitude",value=77.5946,format="%.6f")
    left,right=st.columns([1.7,1])
    with left:
        st.subheader("Live camera")
        video_slot=st.empty()
        status=st.empty()
    with right:
        st.subheader("Subject details")
        detail=st.empty()
        metrics=st.empty()
    run=st.button("▶ Start tracking",type="primary")
    stop=st.button("■ Stop")
    if run:
        try:
            detector=SubjectDetector(weights,conf)
            cap=open_source(source)
            frame_no=0; last_event={}
            status.info("Tracking started. Stop the run with the Stop button.")
            while cap.isOpened():
                ok,frame=cap.read()
                if not ok: break
                frame_no+=1
                if frame_no % int(frame_skip): continue
                detections=detector.detect_and_track(frame)
                canvas=annotate(frame.copy(),detections)
                video_slot.image(cv2.cvtColor(canvas,cv2.COLOR_BGR2RGB),channels="RGB",use_container_width=True)
                if detections:
                    selected=detections[0]
                    detail.json({k:v for k,v in selected.items() if k!="bbox"})
                    metrics.metric("Visible tracked objects",len(detections))
                    for det in detections:
                        key=(det["track_id"],det["class"])
                        if time.time()-last_event.get(key,0)>5:
                            save_event("CAM-01",det,frame)
                            last_event[key]=time.time()
                else:
                    detail.info("No tracked objects in this frame.")
                    metrics.metric("Visible tracked objects",0)
                # Prevent an exhausted video from spinning forever.
                time.sleep(0.001)
                if stop: break
            cap.release()
            status.success("Tracking session finished.")
        except Exception as exc:
            status.error(str(exc))
            st.exception(exc)
    st.divider()
    map_col,events_col=st.columns([1,1.4])
    with map_col:
        st.subheader("Map / last known location")
        st.caption("GPS is not inferred from ordinary CCTV. Enter coordinates in the sidebar or connect a camera-location feed.")
        _map_panel(lat,lon)
    with events_col:
        st.subheader("Detection event log")
        if CSV_PATH.exists():
            df=pd.read_csv(CSV_PATH)
            st.dataframe(df.tail(100),use_container_width=True,hide_index=True)
            st.download_button("Download event CSV",df.to_csv(index=False), "subject_events.csv","text/csv")
        else:
            st.info("No events recorded yet.")
    st.subheader("Captured snapshots")
    images=sorted(SNAPSHOT_DIR.glob("*.jpg"),key=lambda p:p.stat().st_mtime,reverse=True)[:8]
    if images:
        cols=st.columns(4)
        for i,path in enumerate(images):
            cols[i%4].image(str(path),caption=path.name,use_container_width=True)
