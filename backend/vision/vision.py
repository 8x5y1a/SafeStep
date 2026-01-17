import cv2
from ultralytics import YOLO

# yolo is ai
model = YOLO("yolov8n.pt")  

# open camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera error")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ai sees frame
    results = model(frame)

    # draw squares and what its seeing
    annotated_frame = results[0].plot()

    cv2.imshow("AI Vision", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    objects = results[0].boxes.cls.tolist()
    names = results[0].names

    seen = {names[int(o)] for o in objects}
    print("I see:", ", ".join(seen))

cap.release()
cv2.destroyAllWindows()
