import cv2 as cv
import mediapipe as mp
import pyautogui

# Hand tracking
Capture_Hand_Gesture = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
Drawing_Utils = mp.solutions.drawing_utils
camera = cv.VideoCapture(0)
Screen_Width, Screen_Height = pyautogui.size()

x1 = y1 = x2 = y2 = 0
Smoothening = 5

while True:
    _, frame = camera.read()
    frame = cv.flip(frame, 1)
    image_height, image_width, _ = frame.shape
    RGB_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    output = Capture_Hand_Gesture.process(RGB_image)
    all_hands = output.multi_hand_landmarks

    if all_hands:
        for hand in all_hands:
            Drawing_Utils.draw_landmarks(frame, hand)
            one_hand = hand.landmark
            for id, lm in enumerate(one_hand):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)

                if id == 8:  # Index finger tip
                    Mouse_X = int(Screen_Width / image_width * x)
                    Mouse_Y = int(Screen_Height / image_height * y)
                    Current_X = x1 + (Mouse_X - x1) // Smoothening
                    Current_Y = y1 + (Mouse_Y - y1) // Smoothening
                    pyautogui.moveTo(Current_X, Current_Y)
                    cv.circle(frame, (x, y), 10, (0, 255, 255), cv.FILLED)
                    x1, y1 = Current_X, Current_Y

                if id == 4:  # Thumb tip
                    x2, y2 = x, y
                    cv.circle(frame, (x, y), 10, (255, 0, 255), cv.FILLED)

        # Click gesture
        dist = abs(y2 - y1)
        if dist < 20:
            pyautogui.click()
            cv.waitKey(200)  # small delay to avoid multiple clicks

    cv.imshow("Hand Gesture Mouse", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv.destroyAllWindows()
