import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5
)

TIP_IDS = [4, 8, 12, 16, 20]

def detect_hand(image):

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if not results.multi_hand_landmarks:
        return "No Hand"

    hand = results.multi_hand_landmarks[0]

    landmarks = hand.landmark

    fingers = []

    # Thumb
    if landmarks[TIP_IDS[0]].x < landmarks[TIP_IDS[0]-1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for tip in TIP_IDS[1:]:

        if landmarks[tip].y < landmarks[tip-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    total = sum(fingers)

    if total == 0:
        return "Rock"

    elif total == 2:
        return "Scissors"

    elif total >= 4:
        return "Paper"

    return f"Fingers: {total}"