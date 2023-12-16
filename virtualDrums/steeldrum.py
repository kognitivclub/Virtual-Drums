import cv2
from cvzone.HandTrackingModule import HandDetector
import playsound
import os
import cvzone

def putTextRect(
    img,
    text,
    pos,
    pos2,
    scale=3,
    thickness=3,
    colorT=(255, 255, 255),
    colorR=(255, 0, 255),
    font=cv2.FONT_HERSHEY_PLAIN,
    offset=10,
    border=None,
    colorB=(0, 255, 0),
):

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

dir_path = r"Steel_Drum/"
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

    stpt = 70
    edpt = stpt + 150
    blist = []
    top_line = 180
    bot_line = 380
    for r in range(len(res)):
        if edpt > 1040:
            top_line = 400
            bot_line = 600
            stpt = 70
            edpt = stpt + 150
        img, bbox = putTextRect(img,res[r],[stpt, top_line],[edpt, bot_line],1,1,colorR=(0, 0, 0),colorT=(68, 70, 71))
        # img, bbox = cvzone.putTextRect(img,res[r],(100,100),0.8,1,colorR=(255,67,45))
        blist.append(bbox)
        stpt += 170
        edpt += 170

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
