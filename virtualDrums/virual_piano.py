import cv2
from cvzone.HandTrackingModule import HandDetector
import playsound
import os


# Constants
FONT = cv2.FONT_HERSHEY_PLAIN
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 0, 255)
GRAY = (68, 70, 71)
GREEN = (0, 255, 0)

# Functions
def putTextRect(img, text, pos, pos2, scale=3, thickness=3, colorT=WHITE, colorR=PINK,
                 font=FONT, offset=10, border=None, colorB=GREEN):
    x1, y1 = pos
    x2, y2 = pos2

    cv2.rectangle(img, (x1, y1), (x2, y2), colorR, cv2.FILLED)
    if border is not None:
        cv2.rectangle(img, (x1, y1), (x2, y2), colorB, border)
    cv2.putText(img, text, (x1 + 20, y2), font, scale, colorT, thickness)
    return img, [x1, y2, x2, y1]

cam = cv2.VideoCapture(0)
cam.set(3, 1280)
cam.set(4, 720)
detector = HandDetector(detectionCon=0.8)

dir_path = r"Music_Notes/"
res = []
music_file = []
for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        music_file.append(path)
        res.append(os.path.splitext(path)[0])


def update(cursor, bboxs):
    for x, bbox in enumerate(bboxs):
        x1, y2, x2, y1 = bbox
        if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
            cv2.rectangle(img, (x1, y1), (x2, y2), (68, 70, 71), cv2.FILLED)
            for a, file in enumerate(music_file):
                if x == a:
                    path = str(dir_path + file)
                    playsound.playsound(path)


while True:
    success, img = cam.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    start_pt = 100
    end_pt = start_pt + 50
    blist = []
    top_line = 400
    bot_line = 600

    for i in range(len(res)):
        if i % 2 == 0:
            colorR=(0, 0, 0)
            colorT=(255, 255, 255)
        elif i % 2 != 0:
            colorR=(255, 255, 255)
            colorT=(0, 0, 0)
        img, bbox = putTextRect(img,res[i],[start_pt, top_line],[end_pt, bot_line],1,1,colorR=colorR,colorT=colorT)
        blist.append(bbox)
        start_pt += 55
        end_pt += 55
    if hands:
        lmList = hands[0]["lmList"]
        cursor = lmList[8]
        length, info, img = detector.findDistance(lmList[4], lmList[8], img)
        lmList, bbox = detector.findPosition(img, draw=True)

        if length < 35:
            update(cursor, blist)

    cv2.imshow("Virtual Drums", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()
