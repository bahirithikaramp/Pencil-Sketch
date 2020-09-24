import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

vid = cv2.VideoCapture(0)

vid.set(3, frameWidth)
vid.set(4, frameHeight)
vid.set(10, 150)

# myColors is a list of colors that we want to detect.
myColors = [
			[55,60,50,69,190,180],
			[35,140,100,179,255,165],
			[125,120,35,154,200,255],

            ]

# myColorValues is a list of colors that we want to show
myColorValues = [
				 [0,204,0],            # This should be written in BGR format
				 [255,0,255],
				 [128,0,128],
				    
                 ]

myPoints = []     # [x, y, ColorId]

def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)  # This will give us the filtered out image of that color.
        x,y = getContours(mask)
        cv2.circle(imgResult, (x,y), 10, myColorValues[count], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x, y, count])
        count += 1
        #cv2.imshow(str(color), mask)

    return newPoints


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0

    for cnt in contours:
        area = cv2.contourArea(cnt) # This is used to find the area of the contour.
        if area>500: # The areas below 500 pixels will not be considered
            #cv2.drawContours(imgResult, cnt, -1, (255,0,0), 3) # -1 denotes that we need to draw all the contours
            perimeter = cv2.arcLength(cnt, True) # The true indicates that the contour is closed
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True) # This method is used to find the approximate number of contours
            x,y,w,h = cv2.boundingRect(approx) # In this we get the values of our bounding box that we will draw around the object

    return x+w//2,y


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)



while True:
    success, img = vid.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Output", imgResult)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
