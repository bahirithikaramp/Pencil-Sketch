import cv2

#reading the image
img = cv2.imread("golden_trio.jpg")
cv2.imshow("Actual Image",img)

#convering the image to grayscale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayscale Image",img_gray)

#inverting the grayscale image
img_invert = cv2.bitwise_not(img_gray)
cv2.imshow("Inverted Grayscale Image",img_invert)

#Smoothing the Image
img_smoothing = cv2.GaussianBlur(img_invert,(21,21),sigmaX=0,sigmaY=0)
cv2.imshow("Smoothned Image",img_smoothing)

#function to get the final pencil sketch using a blend function dodgeV2(x,y)
def dodgeV2(x,y):
    return cv2.divide(x, 255-y, scale=256)

#final output
final_img = dodgeV2(img_gray, img_smoothing)
cv2.imshow("Final Pencil Sketch",final_img)


cv2.waitKey(50000)
