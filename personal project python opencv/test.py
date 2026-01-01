import cv2
import mediapipe as mp
import pygetwindow as gw
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

def is_fist(hand_landmarks):
    """Returns True if hand is in a fist"""
    tips = [8, 12, 16, 20]
    folded = 0
    for tip in tips:
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[tip - 2].y:
            folded += 1
    return folded == 4

# To avoid repeated minimization
fist_detected = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # mirror
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if is_fist(hand_landmarks):
                if not fist_detected:
                    fist_detected = True
                    # Minimize the active window
                    active_win = gw.getActiveWindow()
                    if active_win is not None:
                        active_win.minimize()
                    time.sleep(1)  # small delay to prevent multiple triggers
            else:
                fist_detected = False  # reset when hand opens

    cv2.imshow("Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
