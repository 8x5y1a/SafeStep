import cv2
from ultralytics import YOLO
import httpx
from backend.services.gemini import prompt_gemini
import backend.speech.action as action
import os

# setup
os.environ["YOLOV8_LOG_LEVEL"] = "ERROR"
model = YOLO("yolov8n.pt")

timeout = httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=10.0)

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera error")
    exit()


async def describe_scene(seen_objects):
    if not seen_objects:
        return (
            "Sorry, it seems like your camera might not be working. Can you try again?"
        )
    else:
        print("objects found")

    objects_str = ", ".join(seen_objects)
    prompt = f"I will provide a list of items that you can see in an image. Please describe the scene to the user as if he is a blind user requesting help to see what is in front of him. {objects_str}."
    answer = await action.prompt_gemini(prompt)
    return answer


async def observe_camera():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("AI Vision", frame)  # show raw frame continuously

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        results = model(frame)  # analyze current frame

        annotated_frame = results[0].plot()  # draw predictions
        cv2.imshow("AI Vision", annotated_frame)

        objects = results[0].boxes.cls.tolist()
        names = results[0].names
        seen = {names[int(o)] for o in objects}
        print("I see:", ", ".join(seen))
        # TODO: add a timer time out after 5 seconds
        if len(seen) > 0:
            data = await describe_scene(seen)
            cap.release()
            cv2.destroyAllWindows()
            return data
