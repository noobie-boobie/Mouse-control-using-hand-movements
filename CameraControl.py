import cv2 as cv
import time
import mediapipe as mp
import base64

ScreenX, ScreenY = 70,120
ScreenW, ScreenH = 480, 360

cap = None
mp_hands = None
mp_draw = None
running = None

indexTip, indexDip = (0, 0), (0, 0)
middleTip, middleDip = (0, 0), (0, 0)
ringTip, ringDip = (0, 0), (0, 0)
pinkyTip, pinkyDip = (0, 0), (0, 0)
thumpTip = (0, 0)
wrist = (0,0)
Finger = None
hands = None
prev = None

def getScreen():
    global ScreenX, ScreenY, ScreenW, ScreenH
    return ScreenX, ScreenY, ScreenW, ScreenH

def initSetup():
    global cap, mp_hands, mp_draw, running, indexDip, indexTip, middleDip, middleTip,ringTip, ringDip, wrist
    global pinkyTip, pinkyDip, thumpTip, Finger, hands, prev
    cap = cv.VideoCapture(1)
    running = True

    print('Starting Camera...')
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    fingerpoint = mp_hands.HandLandmark
    prev = 0
    hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
    Finger = {
        1: '',
        2: '',
        3: '',
        4: ''
    }

    indexTip, indexDip = (0, 0), (0, 0)
    middleTip, middleDip = (0, 0), (0, 0)
    ringTip, ringDip = (0, 0), (0, 0)
    pinkyTip, pinkyDip = (0, 0), (0, 0)
    wrist = (0,0)
    thumpTip = (0, 0)

def getFrame():
    global cap, mp_hands, mp_draw, running, indexDip, indexTip, middleDip, middleTip, ringTip, ringDip, wrist
    global pinkyTip, pinkyDip, thumpTip, Finger, hands, prev
    ret, frame = cap.read()
    imgStr = ''

    image = cv.flip(frame, 1)
    image = cv.resize(image, (640, 480))
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image.flags.writeable = False
    POINTS = hands.process(image)
    image.flags.writeable = True
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    imageHeight, imageWidth, _ = image.shape


    ctime = time.time()
    fps = 1 / (ctime - prev)
    fps = str(int(fps))
    prev = ctime

    #
    cv.putText(image, 'FPS: ' + fps, (20, imageHeight - 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
    if POINTS.multi_hand_landmarks:
        for hand in POINTS.multi_hand_landmarks:
            for point in mp_hands.HandLandmark:
                normalizedLandmark = hand.landmark[point]
                pixelCoordinatesLandmark =mp_draw._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                         normalizedLandmark.y,
                                                                                         imageWidth,
                                                                                         imageHeight)
                if pixelCoordinatesLandmark == None:
                    continue
                if point == mp_hands.HandLandmark.INDEX_FINGER_TIP:
                    indexTip = pixelCoordinatesLandmark

                elif point == mp_hands.HandLandmark.INDEX_FINGER_DIP:
                    indexDip = pixelCoordinatesLandmark
                elif point == mp_hands.HandLandmark.MIDDLE_FINGER_TIP:
                    middleTip = pixelCoordinatesLandmark
                elif point == mp_hands.HandLandmark.MIDDLE_FINGER_DIP:
                    middleDip = pixelCoordinatesLandmark
                elif point == mp_hands.HandLandmark.RING_FINGER_DIP:
                    ringDip = pixelCoordinatesLandmark
                elif point == mp_hands.HandLandmark.RING_FINGER_TIP:
                    ringTip = pixelCoordinatesLandmark
                elif point == mp_hands.HandLandmark.PINKY_DIP:
                    pinkyDip = pixelCoordinatesLandmark
                elif point == mp_hands.HandLandmark.PINKY_TIP:
                    pinkyTip = pixelCoordinatesLandmark
                elif point == mp_hands.HandLandmark.THUMB_TIP:
                    thumpTip = pixelCoordinatesLandmark
                elif point == mp_hands.HandLandmark.WRIST:
                    wrist = pixelCoordinatesLandmark
                    #rint('Wrist')



                # if point == fingerpoint.MIDDLE_FINGER_DIP or point == fingerpoint.INDEX_FINGER_TIP:

                if indexTip[1] < indexDip[1]:
                    Finger[1] = '1'
                elif indexDip[1] < indexTip[1]:
                    Finger[1] = '0'

                if middleTip[1] < middleDip[1]:
                    Finger[2] = '1'
                elif middleDip[1] < middleTip[1]:
                    Finger[2] = '0'

                if ringTip[1] < ringDip[1]:
                    Finger[3] = '1'
                elif ringDip[1] < ringTip[1]:
                    Finger[3] = '0'

                if pinkyTip[1] < pinkyDip[1]:
                    Finger[4] = '1'
                elif pinkyDip[1] < pinkyTip[1]:
                    Finger[4] = '0'

                cv.putText(image, Finger[1], (20, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                cv.putText(image, Finger[2], (50, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                cv.putText(image, Finger[3], (80, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                cv.putText(image, Finger[4], (110, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                cv.putText(image, 'X: '+ str(wrist[0]), (20, 100), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
                cv.putText(image, 'Y: '+ str(wrist[1]), (20, 140), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))

                # print(pixelCoordinatesLandmark)
                # print(normalizedLandmark)

            mp_draw.draw_landmarks(image, hand,mp_hands.HAND_CONNECTIONS)
    sx,sy,sw,sh = getScreen()
    cv.rectangle(image, (sx,sy), (sx +sw, sy + sh), (255, 0, 0), 2)
    cv.imshow('Hand', image)
    if cv.waitKey(1) == 27:
        running = False
        stop()
    smallImg = cv.resize(image, (200,150))
    ret, imgenc = cv.imencode('.jpg', smallImg)
    imgStr = base64.b64encode(imgenc)
    height, width = image.shape[:2]

    return  (Finger, wrist, height, width)

def toStr(A):
    try:
        f = A[0]
        x,y = A[1]
        h, w = A[2], A[3]
    except:
        return {}

    global cap, mp_hands, mp_draw, running, indexDip, indexTip, middleDip, middleTip, ringTip, ringDip
    global pinkyTip, pinkyDip, thumpTip, Finger, hands, prev
    s = ''
    for i in f:
        s += f[i]

    d = {
        'Finger': s,
        'X': x,
        'Y': y,
        'Height': h,
        'Width': w
    }
    return d


def stop():
    global  cap, running
    cap.release()
    cv.destroyAllWindows()
    running = False



def getFingersValue():
    if running:
        return toStr(getFrame())
    else:
        return False

# if __name__ == '__main__':
#     initSetup()
#     while True:
#         print(getFingersValue())