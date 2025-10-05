import cv2
import mediapipe as mp
import time

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
cv2.namedWindow("Virtual Keyboard", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Virtual Keyboard", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,  # Only track 1 hand
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
mp_draw = mp.solutions.drawing_utils

# Keyboard layout (English only)
keys = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Caps", "Z", "X", "C", "V", "B", "N", "M", "Delete"],
    ["Shift", "Space", "Enter", "Close"]
]

final_text = ""
shift_active = False
caps_lock = False
clicked = False
last_click_time = 0

# Button class
class Button:
    def __init__(self, pos, text, size=(85, 85)):
        self.pos = pos
        self.size = size
        self.text = text

# Draw transparent buttons
def draw_buttons(img, buttons, hover_idx=None):
    overlay = img.copy()
    alpha = 0.4  # درجة الشفافية (0 شفاف تمامًا - 1 بدون شفافية)

    for idx, btn in enumerate(buttons):
        x, y = btn.pos
        w, h = btn.size
        color = (0, 255, 0) if idx == hover_idx else (50, 50, 50)

        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, cv2.FILLED)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 255, 255), 2)

        text_size = cv2.getTextSize(btn.text, cv2.FONT_HERSHEY_PLAIN, 2, 2)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(overlay, btn.text, (text_x, text_y),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
    return img

# Create buttons and center layout
def create_buttons():
    buttons = []
    y_offset = 100
    for row in keys:
        widths = []
        for key in row:
            if key == "Space":
                widths.append(685)
            elif key == "Enter":
                widths.append(150)
            elif key == "Delete":
                widths.append(180)
            else:
                widths.append(85)
        total_width = sum(widths) + (len(row) - 1) * 10
        x_offset = (1280 - total_width) // 2

        for i, key in enumerate(row):
            w = widths[i]
            buttons.append(Button((x_offset, y_offset), key, (w, 85)))
            x_offset += w + 10
        y_offset += 100
    return buttons

# Get hand landmarks
def get_landmarks(img):
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    lm = []
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
            for id, pt in enumerate(hand.landmark):
                h, w, _ = img.shape
                lm.append((id, int(pt.x * w), int(pt.y * h)))
    return lm

# Main loop
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    lm_list = get_landmarks(img)
    button_list = create_buttons()
    hover_idx = None

    if lm_list:
        ix, iy = lm_list[8][1], lm_list[8][2]
        for idx, btn in enumerate(button_list):
            x, y = btn.pos
            w, h = btn.size
            if x < ix < x + w and y < iy < y + h:
                hover_idx = idx
                break

    img = draw_buttons(img, button_list, hover_idx)

    if lm_list:
        ix, iy = lm_list[8][1], lm_list[8][2]
        base_y = lm_list[7][2]
        mid_tip_y = lm_list[12][2]
        mid_base_y = lm_list[11][2]

        for btn in button_list:
            x, y = btn.pos
            w, h = btn.size
            if x < ix < x + w and y < iy < y + h:
                current_time = time.time()
                if iy < base_y and mid_tip_y < mid_base_y and not clicked and (current_time - last_click_time > 0.5):
                    key = btn.text
                    if key == "Space":
                        final_text += " "
                    elif key == "Delete":
                        final_text = final_text[:-1]
                    elif key == "Shift":
                        shift_active = not shift_active
                    elif key == "Caps":
                        caps_lock = not caps_lock
                    elif key == "Enter":
                        with open("typed_output.txt", "a", encoding="utf-8") as f:
                            f.write(final_text + "\n")
                        final_text = ""
                    elif key == "Close":
                        cap.release()
                        cv2.destroyAllWindows()
                        exit(0)
                    else:
                        if caps_lock or shift_active:
                            final_text += key.upper()
                        else:
                            final_text += key.lower()
                    clicked = True
                    last_click_time = current_time

        if iy < base_y and mid_tip_y > mid_base_y:
            clicked = False

    # Transparent text bar
    overlay = img.copy()
    cv2.rectangle(overlay, (50, 20), (1230, 90), (0, 128, 255), -1)
    img = cv2.addWeighted(overlay, 0.5, img, 0.5, 0)
    cv2.putText(img, final_text, (60, 80), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
