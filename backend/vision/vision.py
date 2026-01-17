import cv2
from ultralytics import YOLO

# Load AI model
model = YOLO("yolov8n.pt")  # small & fast

# Open camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera error")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 👁️ AI looks at the frame
    results = model(frame)

    # Draw AI predictions on the image
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
