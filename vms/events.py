import csv, time
from datetime import datetime
from .config import EVENT_DIR, SNAPSHOT_DIR

CSV_PATH = EVENT_DIR / "subject_events.csv"
FIELDS = ["timestamp","camera","track_id","class","confidence","snapshot"]

def save_event(camera, detection, frame):
    import cv2
    stamp=datetime.now().astimezone().isoformat(timespec="seconds")
    filename=f'{int(time.time()*1000)}_{camera}_id{detection["track_id"]}.jpg'
    path=SNAPSHOT_DIR/filename
    cv2.imwrite(str(path),frame)
    row={"timestamp":stamp,"camera":camera,"track_id":detection["track_id"],
         "class":detection["class"],"confidence":round(detection["confidence"],3),
         "snapshot":str(path.relative_to(EVENT_DIR.parent.parent))}
    exists=CSV_PATH.exists()
    with CSV_PATH.open("a",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS)
        if not exists: writer.writeheader()
        writer.writerow(row)
    return row
