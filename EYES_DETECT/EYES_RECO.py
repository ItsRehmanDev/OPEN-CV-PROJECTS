import cv2 as cv

# Load Haarcascade for eyes detection
EYE_CASCADE = cv.CascadeClassifier(r'D:\Open-Cv\AI_MODELS_FILES\haarcascade_eye.xml')
if EYE_CASCADE.empty():
    print("Failed to load cascade file")
    exit()

# Open webcam
webcam = cv.VideoCapture(0, cv.CAP_DSHOW)
if not webcam.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = webcam.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Detect eyes
    eyes = EYE_CASCADE.detectMultiScale(
        gray_frame,
        scaleFactor=1.1,   # adjust for detection sensitivity
        minNeighbors=10     # adjust to reduce false positives
    )

    # Draw rectangles around detected eyes
    for (x, y, w, h) in eyes:
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv.putText(frame, "Eye", (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

    cv.imshow("Eye Detection", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv.destroyAllWindows()
