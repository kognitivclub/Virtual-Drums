import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone

cam = cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)
detector = HandDetector(detectionCon=0.8)

global c_val

def update(cursor, bboxs):
    for x, bbox in enumerate(bboxs):
        x1, y1, x2, y2 = bbox
        if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
            if x == 0:
                c_val = 1
                print("Option a clicked !")



while True:
    success, img = cam.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    img, bbox1 = cvzone.putTextRect(img, "Option A", [100, 300], 1, 1, offset=50)

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]
        length, info, img = detector.findDistance(lmList[4],lmList[8], img)
        lmList, bbox = detector.findPosition(img, draw=True)

        if length < 35:
            update(cursor, [bbox1])

    cv2.imshow("Virtual Drums", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()