import cv2 as cv

FACE_CASCADE = cv.CascadeClassifier(r'D:\Open-Cv\AI_MODELS_FILES\haarcascade_frontalface_default.xml')
if FACE_CASCADE.empty():
    print("Failed to load cascade file")
    exit()

webcam = cv.VideoCapture(0, cv.CAP_DSHOW)
if not webcam.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, image = webcam.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv.imshow("Face Detection", image)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv.destroyAllWindows()
