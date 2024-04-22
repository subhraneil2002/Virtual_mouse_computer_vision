import cv2
import mediapipe as mp
import pyautogui
import time

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0
double_click_time = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if cv2.waitKey(1) & 0xFF == 27:  # Checking for the escape key (ASCII value 27)
        break
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 9:
                    cv2.circle(img = frame, center = (x,y), radius = 10, color = (0, 255, 255))
                    middle_cursor_x = screen_width / frame_width * x
                    middle_cursor_y = screen_height / frame_height * y
                    pyautogui.moveTo(middle_cursor_x, middle_cursor_y)

                if id == 8:
                    cv2.circle(img = frame, center = (x,y), radius = 10, color = (0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                if id == 4:
                    cv2.circle(img = frame, center=(x, y), radius = 10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    print('outside left click distance', abs(index_y - thumb_y),'\n')

                    if abs(index_y - thumb_y) < 35:
                        current_time = time.time()
                        pyautogui.click()
                        pyautogui.sleep(1)
                        print('left click')

                        if current_time - double_click_time > 0.5:
                            pyautogui.dragTo(middle_cursor_x, middle_cursor_y)

                if id == 12:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    middle_x = screen_width / frame_width * x
                    middle_y = screen_height / frame_height * y

                    if abs(middle_y - thumb_y) < 35:
                        pyautogui.doubleClick()
                        pyautogui.sleep(1)
                        print('double click')

                if id == 16:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    ring_x = screen_width / frame_width * x
                    ring_y = screen_height / frame_height * y
                    print('outside right click distance', abs(ring_y - thumb_y))

                    if abs(ring_y - thumb_y) < 35:
                        pyautogui.rightClick()
                        pyautogui.sleep(1)
                        print('right click')

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
