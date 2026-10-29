import cv2
import mediapipe as mp
import numpy as np
import time
from pathlib import Path


class HandTracker:
    def __init__(self):
        model_path = Path(__file__).parent / "models" / "hand_landmarker.task"

        if not model_path.exists():
            raise FileNotFoundError(
                "Model not found. Download hand_landmarker.task "
                "and place it inside the models folder."
            )

        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        RunningMode = mp.tasks.vision.RunningMode

        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(model_path)),
            running_mode=RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.6,
            min_hand_presence_confidence=0.6,
            min_tracking_confidence=0.6
        )

        self.landmarker = HandLandmarker.create_from_options(options)
        self.start_time = time.monotonic()
        self.last_timestamp = -1

    def find_hand(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=np.ascontiguousarray(rgb)
        )

        timestamp = int(
            (time.monotonic() - self.start_time) * 1000
        )

        timestamp = max(timestamp, self.last_timestamp + 1)
        self.last_timestamp = timestamp

        result = self.landmarker.detect_for_video(image, timestamp)

        if not result.hand_landmarks:
            return frame, None

        landmarks = result.hand_landmarks[0]

        height, width = frame.shape[:2]

        points = []

        for landmark in landmarks:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            points.append((x, y))

            cv2.circle(
                frame,
                (x, y),
                4,
                (0, 255, 0),
                -1
            )

        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (5, 9), (9, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16),
            (13, 17), (17, 18), (18, 19), (19, 20),
            (0, 17)
        ]

        for start, end in connections:
            cv2.line(
                frame,
                points[start],
                points[end],
                (255, 0, 0),
                2
            )

        return frame, points

    def close(self):
        self.landmarker.close()