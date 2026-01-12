import cv2 as cv
import mediapipe as mp
import pyautogui
import time

x1 = y1 = x2 = y2 = 0
last_action_time = 0  
cooldown = 0.3  

webcam = cv.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils 

while True:
    ret, frame = webcam.read()
    if not ret:
        break
    
    image = cv.flip(frame, 1)
    frame_height, frame_width, _ = image.shape
    rgb_frame = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    output = my_hands.process(rgb_frame)
    hands = output.multi_hand_landmarks
    
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            for id, landmark in enumerate(hand.landmark):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                
                if id == 8:  # Index finger
                    cv.circle(image, (x, y), 10, (0,255,255), 6)
                    x1, y1 = x, y
                if id == 4:  # Thumb
                    cv.circle(image, (x, y), 10, (0,0,255), 6)
                    x2, y2 = x, y
        
        dist = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
        cv.line(image, (x1, y1), (x2, y2), (255,0,0), 3)
        
        current_time = time.time()
        if current_time - last_action_time > cooldown:
            if dist > 100:
                pyautogui.press("volumeup")
                last_action_time = current_time
            elif dist < 50:
                pyautogui.press("volumedown")
                last_action_time = current_time
    
    cv.imshow("Webcam", image)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv.destroyAllWindows()
