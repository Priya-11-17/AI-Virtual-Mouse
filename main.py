import cv2
import time
import pyautogui

from hand_tracking import HandTracker
from mouse_controller import MouseController


def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot access webcam")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    tracker = HandTracker()
    mouse = MouseController()

    previous_time = time.time()

    print("AI Virtual Mouse Started")
    print("Press Q to quit")

    try:
        while True:

            success, frame = cap.read()

            if not success:
                print("Failed to read webcam")
                break

            frame = cv2.flip(frame, 1)

            frame, points = tracker.find_hand(frame)

            height, width = frame.shape[:2]

            if points is not None:

                action = mouse.control(
                    points,
                    width,
                    height
                )

                cv2.putText(
                    frame,
                    f"Action: {action}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            else:

                mouse.reset()

                cv2.putText(
                    frame,
                    "No Hand Detected",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            current_time = time.time()

            elapsed = current_time - previous_time
            fps = 1 / elapsed if elapsed > 0 else 0

            previous_time = current_time

            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Press Q to Quit",
                (20, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.imshow("AI Virtual Mouse", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except pyautogui.FailSafeException:
        print("Mouse fail-safe activated. Exiting.")

    except KeyboardInterrupt:
        print("Application stopped.")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        tracker.close()


if __name__ == "__main__":
    main()