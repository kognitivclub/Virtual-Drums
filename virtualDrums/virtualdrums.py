import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
from playsound import playsound

cam = cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)
detector = HandDetector(detectionCon=0.8)


def update(cursor, bboxs):
    for x, bbox in enumerate(bboxs):
        x1, y1, x2, y2 = bbox
        if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
            if x == 0:
                playsound('sounds/sounds_high_hat_1.mp3')
            elif x == 1:
                playsound('sounds/sounds_high_hat_2.wav')
            elif x == 2:
                playsound('sounds/sounds_high_hat_3.wav')
            elif x == 3:
                playsound('sounds/sounds_snare_1.wav')
            elif x == 4:
                playsound('sounds/sounds_snare_2.wav')
            elif x == 5:
                import ctypes
                ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None) 
 
while True:
    success, img = cam.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    img, bbox1 = cvzone.putTextRect(img, "High Hat", [10, 100], 1, 1, offset=50, colorT=(255, 255, 255),colorR=(0, 0, 0))
    img, bbox2 = cvzone.putTextRect(img, "High Hat 2", [400, 300], 1, 1, offset=50)
    img, bbox3 = cvzone.putTextRect(img, "High Hat 3", [700, 300], 1, 1, offset=50)
    img, bbox4 = cvzone.putTextRect(img, "Snare 1", [200, 500], 1, 1, offset=50)
    img, bbox5 = cvzone.putTextRect(img, "Snare 2", [500, 500], 1, 1, offset=50)
    img, bbox6 = cvzone.putTextRect(img, "Open CD", [900, 500], 2, 2, offset=50)

    bl = [bbox1, bbox2, bbox3, bbox4, bbox5, bbox6]
    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]
        length, info, img = detector.findDistance(lmList[4],lmList[8], img)
        lmList, bbox = detector.findPosition(img, draw=True)

        if length < 35:
            update(cursor,bl )
    cv2.imshow("Virtual Drums", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()