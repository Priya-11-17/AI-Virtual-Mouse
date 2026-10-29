import pyautogui
import numpy as np
import time


class MouseController:

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

        self.previous_x = self.screen_width / 2
        self.previous_y = self.screen_height / 2

        self.smoothing = 5
        self.click_cooldown = 0.6

        self.last_click_time = 0
        self.last_scroll_y = None

        self.left_pinched = False
        self.right_pinched = False

        pyautogui.FAILSAFE = True

    def distance(self, p1, p2):
        return np.hypot(
            p1[0] - p2[0],
            p1[1] - p2[1]
        )

    def finger_up(self, points, tip, pip):
        return points[tip][1] < points[pip][1]

    def move_mouse(self, x, y, frame_width, frame_height):

        margin = 80

        x = np.clip(x, margin, frame_width - margin)
        y = np.clip(y, margin, frame_height - margin)

        screen_x = np.interp(
            x,
            [margin, frame_width - margin],
            [0, self.screen_width - 1]
        )

        screen_y = np.interp(
            y,
            [margin, frame_height - margin],
            [0, self.screen_height - 1]
        )

        current_x = self.previous_x + (
            screen_x - self.previous_x
        ) / self.smoothing

        current_y = self.previous_y + (
            screen_y - self.previous_y
        ) / self.smoothing

        pyautogui.moveTo(
            int(current_x),
            int(current_y)
        )

        self.previous_x = current_x
        self.previous_y = current_y

    def control(self, points, frame_width, frame_height):

        thumb = points[4]
        index = points[8]
        middle = points[12]

        index_up = self.finger_up(points, 8, 6)
        middle_up = self.finger_up(points, 12, 10)

        index_distance = self.distance(thumb, index)
        middle_distance = self.distance(thumb, middle)

        left_pinch = index_distance < 35
        right_pinch = middle_distance < 35

        current_time = time.time()

        # Left click: thumb and index finger
        if left_pinch and not self.left_pinched and not right_pinch:

            if current_time - self.last_click_time > self.click_cooldown:
                pyautogui.click()
                self.last_click_time = current_time
                action = "LEFT CLICK"
            else:
                action = "WAIT"

        # Right click: thumb and middle finger
        elif right_pinch and not self.right_pinched and not left_pinch:

            if current_time - self.last_click_time > self.click_cooldown:
                pyautogui.click(button="right")
                self.last_click_time = current_time
                action = "RIGHT CLICK"
            else:
                action = "WAIT"

        # Scroll with index and middle fingers raised
        elif index_up and middle_up:

            current_y = (index[1] + middle[1]) / 2

            if self.last_scroll_y is not None:
                difference = self.last_scroll_y - current_y

                if difference > 15:
                    pyautogui.scroll(2)
                    action = "SCROLL UP"

                elif difference < -15:
                    pyautogui.scroll(-2)
                    action = "SCROLL DOWN"

                else:
                    action = "SCROLL MODE"
            else:
                action = "SCROLL MODE"

            self.last_scroll_y = current_y

            self.left_pinched = left_pinch
            self.right_pinched = right_pinch

            return action

        # Move with index finger raised
        elif index_up:

            self.move_mouse(
                index[0],
                index[1],
                frame_width,
                frame_height
            )

            action = "MOVING"

        else:
            action = "IDLE"

        self.last_scroll_y = None
        self.left_pinched = left_pinch
        self.right_pinched = right_pinch

        return action

    def reset(self):
        self.last_scroll_y = None
        self.left_pinched = False
        self.right_pinched = False