import cv2
from ultralytics import YOLO
import asyncio
import httpx
from backend.services.gemini import prompt_gemini
import backend.speech.action as action
import os

# --- Setup ---
os.environ["YOLOV8_LOG_LEVEL"] = "ERROR"
model = YOLO("yolov8n.pt", verbose=False)


timeout = httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=10.0)


async def describe_scene(seen_objects):
    # look image once

    if not seen_objects:
        return "I don't see anything specific right now."

    objects_str = ", ".join(seen_objects)
    prompt = f"I am looking at a camera feed. I see: {objects_str}. Describe this scene naturally in one sentence."
    await prompt_gemini(prompt)


async def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    current_description = "Press SPACE to describe the scene"

    print("AI Vision Started. Press 'SPACE' to describe, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 1. AI sees the frame
        results = model(frame, verbose=False)
        annotated_frame = results[0].plot()

        # 2. Extract detected object names
        objects = results[0].boxes.cls.tolist()
        names = results[0].names
        seen = {names[int(o)] for o in objects}

        # 3. Handle Keyboard Input
        key = cv2.waitKey(1) & 0xFF

        # print(action.isVisionRequested)
        # If SPACEBAR is pressed (ASCII 32)
        if key == 32 or action.isVisionRequested:
            print("Spacebar pressed! Asking Gemini...")
            action.isVisionRequested = False
            current_description = "Thinking..."

            # Create a background task so the video doesn't lag
            task = asyncio.create_task(describe_scene(seen))

            # Update the description once the task finishes
            def update_text(t):
                nonlocal current_description
                current_description = t.result()

            task.add_done_callback(update_text)

        # 4. Press 'q' to quit
        elif key == ord("q"):
            break

        # 5. UI Overlay
        # Draw a black bar at the bottom for the text
        cv2.rectangle(annotated_frame, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
        cv2.putText(
            annotated_frame,
            current_description,
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Spacebar to Describe", annotated_frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.run(main())
