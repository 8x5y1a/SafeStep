import cv2
from ultralytics import YOLO
import asyncio
import httpx
from backend.services.gemini import prompt_gemini
import backend.speech.action as action
import os

# setup
os.environ["YOLOV8_LOG_LEVEL"] = "ERROR"
model = YOLO("yolov8n.pt")  

timeout = httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=10.0)

# Open camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera error")
    exit()

async def describe_scene(seen_objects):
    if not seen_objects:
        return "I don't see anything specific right now."
    else:
        print("objects found")

    objects_str = ", ".join(seen_objects)
    prompt = f"I am looking at a camera feed. I see: {objects_str}. Describe this scene naturally in one sentence."
    await action.prompt_gemini(prompt)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("AI Vision", frame)  # show raw frame continuously

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('s'):  # press 's' to run YOLO analysis once
        results = model(frame)  # analyze current frame

        annotated_frame = results[0].plot()  # draw predictions
        cv2.imshow("AI Vision", annotated_frame)

        objects = results[0].boxes.cls.tolist()
        names = results[0].names
        seen = {names[int(o)] for o in objects}
        print("I see:", ", ".join(seen))

        describe_scene(seen)

cap.release()
cv2.destroyAllWindows()