import cv2 as cv
import mediapipe as mp
import winsound
import time

smile_detected = False
frame_count = 0
SMILE_FRAMES = 4       # smile must persist for 3 consecutive frames
THRESHOLD = 80         # balanced threshold for small and medium smiles

face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
camera = cv.VideoCapture(0)

if not camera.isOpened():
    exit()

while True:
    ret, frame = camera.read()
    if not ret or frame is None:
        continue

    frame = cv.flip(frame, 1)
    fh, fw, _ = frame.shape
    RGB_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    output = face_mesh.process(RGB_frame)
    all_faces = output.multi_face_landmarks

    if all_faces:
        landmarks = all_faces[0].landmark
        x1 = int(landmarks[61].x * fw)
        y1 = int(landmarks[61].y * fh)
        x2 = int(landmarks[291].x * fw)
        y2 = int(landmarks[291].y * fh)

        dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5

        if dist > THRESHOLD:
            frame_count += 1
        else:
            frame_count = 0

        if frame_count >= SMILE_FRAMES and not smile_detected:
            filename = f"smile_{int(time.time()*1000)}.png"
            cv.imwrite(filename, frame)
            winsound.PlaySound(r"D:\Open-Cv\SOUND\sounnd.wav", winsound.SND_FILENAME)
            print(f"Smile captured! Saved as {filename}")
            smile_detected = True

        elif dist <= THRESHOLD:
            smile_detected = False

    cv.imshow("Smile Detector", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv.destroyAllWindows()
