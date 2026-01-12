import cv2 as cv

# Load Haarcascade for smile detection
SMILE_CASCADE = cv.CascadeClassifier(r'D:\Open-Cv\AI_MODELS_FILES\haarcascade_smile.xml')
if SMILE_CASCADE.empty():
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

    # Detect smiles
    smiles = SMILE_CASCADE.detectMultiScale(
        gray_image,
        scaleFactor=1.7,   # Higher scaleFactor works better for smiles
        minNeighbors=60    # Increase to reduce false positives
    )

    for (x, y, w, h) in smiles:
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.putText(image, "Smile", (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)

    cv.imshow("Smile Detection", image)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv.destroyAllWindows()
