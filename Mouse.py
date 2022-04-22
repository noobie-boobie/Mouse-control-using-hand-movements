import mouse
from  CameraControl import getFrame, getFingersValue, initSetup, stop, getScreen
from win32api import GetSystemMetrics
# mouse.move(100, 100, absolute=False, duration=0.2)

finger = ''
mouseX = -1
mouseY = -1
ScreenWidth = GetSystemMetrics(0)
ScreenHeight = GetSystemMetrics(1)

vsX, vsY, vsW, vsH = getScreen()
heightFactor, widthFactor = ScreenHeight//vsH, ScreenWidth//vsW
print(ScreenWidth, ScreenHeight)
print(heightFactor, widthFactor)
running = True

def inScreen(x, y):
    global vsX, vsY, vsW, vsH

    if x >= vsX and x <= (vsX + vsW) and y >= vsY and y <= (vsH + vsY):
        return True
    return False

def getXYPOS(fx, fy):
    if not inScreen(fx, fy):
        return -1, -1
    tempX, tempY = fx - vsX, fy - vsY
    mfx = 1.75
    mfy = 1.2
    mX, mY = tempX*widthFactor*mfx - 100, mfy*tempY*heightFactor - 50
    #print(mX, mY, fx, fy)

    return mX, mY

initSetup()
while running:
    data = getFingersValue()

    finger = data['Finger']
    #print(finger)

    fX, fY = data['X'], data['Y']
    # if finger == '0111':
    #     mouse.click('left')
    # elif finger == '1000':
    #     mouse.click('right')

    mouseX, mouseY = getXYPOS(fX, fY)

    if finger == '1100' and mouseX != -1:
        mouse.move(mouseX, mouseY)

    if finger == '1001':
        stop()
        running = False    