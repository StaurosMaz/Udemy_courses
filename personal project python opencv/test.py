import cv2
import mediapipe as mp
import pygetwindow as gw
import pyautogui
import time
import math

# ---------------- INITIALIZATION ----------------

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# ---------------- CONFIG ----------------

MOVE_SCALE = 3
PINCH_FRAMES_REQUIRED = 2
FIST_FRAMES_REQUIRED = 3
SMOOTHING_ALPHA = 0.25  # lower = smoother, higher = faster

# ---------------- HELPER FUNCTIONS ----------------

def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def finger_folded(hand_landmarks, tip, pip):
    return hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y

def thumb_folded(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    index_mcp = hand_landmarks.landmark[5]
    return abs(thumb_tip.x - index_mcp.x) < 0.04

def is_fist(hand_landmarks):
    fingers = [
        finger_folded(hand_landmarks, 8, 6),
        finger_folded(hand_landmarks, 12, 10),
        finger_folded(hand_landmarks, 16, 14),
        finger_folded(hand_landmarks, 20, 18)
    ]
    return all(fingers) and thumb_folded(hand_landmarks)

def fingers_extended(hand_landmarks):
    return (
        hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y and
        hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    )

def is_pinch(hand_landmarks):
    thumb = hand_landmarks.landmark[4]
    index = hand_landmarks.landmark[8]
    middle = hand_landmarks.landmark[12]

    wrist = hand_landmarks.landmark[0]
    mcp = hand_landmarks.landmark[9]

    hand_size = distance(wrist, mcp)
    pinch_threshold = hand_size * 0.4

    return (
        distance(thumb, index) < pinch_threshold and
        distance(thumb, middle) < pinch_threshold
    )

# ---------------- STATE ----------------

dragging = False
pinch_counter = 0
fist_counter = 0
fist_detected = False

start_hand_x = start_hand_y = 0
start_win_x = start_win_y = 0

smooth_x = smooth_y = 0

# ---------------- MAIN LOOP ----------------

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # -------- FIST --------
            if is_fist(hand_landmarks):
                fist_counter += 1
            else:
                fist_counter = 0

            if fist_counter >= FIST_FRAMES_REQUIRED and not fist_detected:
                fist_detected = True
                win = gw.getActiveWindow()
                if win:
                    win.minimize()
                time.sleep(1)

            if fist_counter == 0:
                fist_detected = False

            # -------- PINCH STABILITY --------
            if is_pinch(hand_landmarks) and fingers_extended(hand_landmarks):
                pinch_counter += 1
            else:
                pinch_counter = 0

            pinch = pinch_counter >= PINCH_FRAMES_REQUIRED

            # -------- PINCH → MOVE WINDOW (SMOOTH) --------
            palm = hand_landmarks.landmark[0]
            screen_w, screen_h = pyautogui.size()
            hand_x = int(palm.x * screen_w)
            hand_y = int(palm.y * screen_h)

            win = gw.getActiveWindow()

            if pinch and win:
                if not dragging:
                    dragging = True
                    start_hand_x, start_hand_y = hand_x, hand_y
                    start_win_x, start_win_y = win.left, win.top
                    smooth_x, smooth_y = start_win_x, start_win_y
                else:
                    target_x = start_win_x + (hand_x - start_hand_x) * MOVE_SCALE
                    target_y = start_win_y + (hand_y - start_hand_y) * MOVE_SCALE

                    smooth_x += SMOOTHING_ALPHA * (target_x - smooth_x)
                    smooth_y += SMOOTHING_ALPHA * (target_y - smooth_y)

                    win.moveTo(int(smooth_x), int(smooth_y))
            else:
                dragging = False

    cv2.imshow("Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------- CLEANUP ----------------

cap.release()
cv2.destroyAllWindows()
