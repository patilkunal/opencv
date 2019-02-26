import cv2
import numpy as np
import matplotlib.pyplot as plt

def toCanny(image):
    "Peforms edge detection on the image"
    #Convert to grayscale 
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # reduce noise using gaussian blur
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    # edge detection using canny alg
    canny = cv2.Canny(blur, 50, 150)
    return canny

def display_lines(image, lines):
    if(lines is not None):
        line_image = np.zeros_like(image)
        for line in lines:
            # print(line)
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1),  (x2, y2), (255, 0, 0), 10)
    return line_image


def region_of_interest(image):
    height = image.shape[0] #returns the height (bottom) of the image 
    # get the array pixels bounded by the triangle
    # the selected area needs to be in array of arrays fashion
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
    ])
    #create a mask of same size as image with all zeros (black color)     
    mask = np.zeros_like(image)
    # just for the region of interest (triangle area) fill with white (255) pattern
    cv2.fillPoly(mask, polygons, 255)
    # apply the mask to the image to just show the area of interest
    masked_image = cv2.bitwise_and(image, mask)
    # return the result image after masking
    return masked_image

image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
canny = toCanny(lane_image)


cropped_image = region_of_interest(canny)
lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
line_image = display_lines(lane_image, lines)
combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
cv2.imshow("result", combo_image)
cv2.waitKey(0)

# plt.imshow(canny)
# plt.show()
