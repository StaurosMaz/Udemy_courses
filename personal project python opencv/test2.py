import cv2
import mediapipe as mp
import pygetwindow as gw
import pyautogui
import time
import math

# ================== INIT ==================

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.80,
)

mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# ================== CONFIG ==================

MOVE_SCALE = 2.5
SMOOTHING = 0.40

PINCH_THRESHOLD_RATIO = 0.60
OPEN_PALM_HOLD_TIME = 1
V_SIGN_HOLD_TIME = 0.4

# ================== STATE ==================

state = "IDLE"

open_palm_start = None
v_sign_start = None

start_hand_x = start_hand_y = 0
start_win_x = start_win_y = 0
smooth_x = smooth_y = 0

windows = []
selected_index = 0
last_hand_x = None

# ================== HELPERS ==================

def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

def is_pinch(lm):
    thumb = lm.landmark[4]
    index = lm.landmark[8]
    wrist = lm.landmark[0]
    mcp = lm.landmark[9]
    hand_size = dist(wrist, mcp)
    return dist(thumb, index) < hand_size * PINCH_THRESHOLD_RATIO

def is_thumb_middle_pinch(lm):
    thumb = lm.landmark[4]
    middle = lm.landmark[12]
    wrist = lm.landmark[0]
    mcp = lm.landmark[9]
    hand_size = dist(wrist, mcp)
    return dist(thumb, middle) < hand_size * PINCH_THRESHOLD_RATIO

def is_fist(lm):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    return all(lm.landmark[t].y > lm.landmark[p].y for t, p in zip(tips, pips))

def is_open_palm(lm):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    return all(lm.landmark[t].y < lm.landmark[p].y for t, p in zip(tips, pips))

def is_v_sign(lm):
    index_up = lm.landmark[8].y < lm.landmark[6].y
    middle_up = lm.landmark[12].y < lm.landmark[10].y
    ring_down = lm.landmark[16].y > lm.landmark[14].y
    pinky_down = lm.landmark[20].y > lm.landmark[18].y
    return index_up and middle_up and ring_down and pinky_down

# ================== MAIN LOOP ==================

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    screen_w, screen_h = pyautogui.size()

    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)

        palm = lm.landmark[0]
        hand_x = int(palm.x * screen_w)
        hand_y = int(palm.y * screen_h)

        win = gw.getActiveWindow()

        # ================== IDLE ==================
        if state == "IDLE":

            if is_v_sign(lm):
                if v_sign_start is None:
                    v_sign_start = time.time()
                elif time.time() - v_sign_start > V_SIGN_HOLD_TIME:
                    windows = [w for w in gw.getAllWindows() if w.isMinimized]
                    if windows:
                        selected_index = 0
                        last_hand_x = hand_x
                        state = "WINDOW_SELECT"
                    v_sign_start = None
            else:
                v_sign_start = None

            if is_pinch(lm) and win:
                state = "DRAGGING"
                start_hand_x, start_hand_y = hand_x, hand_y
                start_win_x, start_win_y = win.left, win.top
                smooth_x, smooth_y = start_win_x, start_win_y

            if is_open_palm(lm):
                if open_palm_start is None:
                    open_palm_start = time.time()
                elif time.time() - open_palm_start > OPEN_PALM_HOLD_TIME:
                    if win:
                        win.restore() if win.isMaximized else win.maximize()
                    open_palm_start = None
            else:
                open_palm_start = None

        # ================== DRAGGING ==================
        elif state == "DRAGGING":
            if not is_pinch(lm) or is_fist(lm):
                state = "IDLE"
            else:
                target_x = start_win_x + (hand_x - start_hand_x) * MOVE_SCALE
                target_y = start_win_y + (hand_y - start_hand_y) * MOVE_SCALE
                smooth_x += SMOOTHING * (target_x - smooth_x)
                smooth_y += SMOOTHING * (target_y - smooth_y)
                if win:
                    win.moveTo(int(smooth_x), int(smooth_y))

        # ================== WINDOW SELECT ==================
        elif state == "WINDOW_SELECT":

            if is_fist(lm):
                state = "IDLE"

            if last_hand_x is not None:
                dx = hand_x - last_hand_x
                if abs(dx) > 40:
                    selected_index = (selected_index + (1 if dx > 0 else -1)) % len(windows)
                    last_hand_x = hand_x

            if is_thumb_middle_pinch(lm):
                windows[selected_index].restore()
                state = "IDLE"

            cv2.putText(
                frame,
                f"SELECT: {windows[selected_index].title}",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

        # ================== UI ==================
        cv2.putText(
            frame,
            f"STATE: {state}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("Gesture Window Control V3", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
