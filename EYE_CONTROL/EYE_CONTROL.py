import cv2 as cv
import mediapipe as mp
import pyautogui

screen_w, screen_h = pyautogui.size()
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cap = cv.VideoCapture(0)

prev_x, prev_y = 0, 0
smooth = 5
blink_thresh = 0.025  # adjust for your webcam
blink_frames = 2       # blink must persist for N frames
blink_counter = 0
eye_closed = False

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    output = face_mesh.process(rgb)

    if output.multi_face_landmarks:
        lm = output.multi_face_landmarks[0].landmark

        iris = lm[474:478]
        x = sum([p.x for p in iris]) / 4
        y = sum([p.y for p in iris]) / 4

        mouse_x = int(screen_w * x)
        mouse_y = int(screen_h * y)

        smooth_x = prev_x + (mouse_x - prev_x) / smooth
        smooth_y = prev_y + (mouse_y - prev_y) / smooth
        pyautogui.moveTo(smooth_x, smooth_y)
        prev_x, prev_y = smooth_x, smooth_y

        # Draw iris
        for p in iris:
            cv.circle(frame, (int(p.x*w), int(p.y*h)), 5, (0,255,0), -1)

        left_eye = [lm[145], lm[159]]
        eye_dist = left_eye[1].y - left_eye[0].y

        # Draw eye landmarks
        for p in left_eye:
            cv.circle(frame, (int(p.x*w), int(p.y*h)), 5, (0,255,255), -1)

        if eye_dist < blink_thresh:
            blink_counter += 1
        else:
            blink_counter = 0

        if blink_counter >= blink_frames and not eye_closed:
            pyautogui.click()
            eye_closed = True
        elif blink_counter == 0:
            eye_closed = False

    cv.imshow("Eye Mouse", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
