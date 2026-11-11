from ultralytics import YOLO
import cv2

class SubjectDetector:
    def __init__(self, weights="yolov8n.pt", confidence=0.35):
        self.model = YOLO(weights)
        self.confidence = confidence

    def detect_and_track(self, frame):
        # persist=True retains tracker state between sequential frames from one camera.
        result = self.model.track(frame, persist=True, conf=self.confidence,
                                  tracker="bytetrack.yaml", verbose=False)[0]
        output = []
        if result.boxes is None:
            return output
        names = result.names
        for box in result.boxes:
            if box.id is None:
                continue
            x1,y1,x2,y2 = map(int, box.xyxy[0].tolist())
            cls_id = int(box.cls[0])
            output.append({
                "track_id": int(box.id[0]), "class": names.get(cls_id, str(cls_id)),
                "confidence": float(box.conf[0]), "bbox": (x1,y1,x2,y2)
            })
        return output

def annotate(frame, detections):
    for item in detections:
        x1,y1,x2,y2 = item["bbox"]
        label=f'{item["class"]} | ID {item["track_id"]} | {item["confidence"]:.2f}'
        cv2.rectangle(frame,(x1,y1),(x2,y2),(30,220,90),2)
        cv2.putText(frame,label,(x1,max(20,y1-8)),cv2.FONT_HERSHEY_SIMPLEX,
                    0.48,(30,220,90),2,cv2.LINE_AA)
    return frame
