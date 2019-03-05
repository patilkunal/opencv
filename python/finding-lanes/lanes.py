import cv2
import numpy as np
import matplotlib.pyplot as plt

def make_coordinates(image, line_parameters):
    "Returns line co-ord from the slope and intercept params"
    slope, intercept = line_parameters
    # try to validate the shape of image by printing shape of it
    # print(image.shape) # (704, 1279, 3) (height, width, color_depth)
    # y1 will be the bottom of and hence first value 
    y1 = image.shape[0]
    # y2 we are positioning at the 3/5th of the image 
    y2 = int(y1*(3/5))
    # now calculate corresponding x co-ord 
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    # print x1, y1, x2, y2
    # return co-ord as array (better way to return multiple values)
    return np.array([x1, y1, x2, y2])



def average_slope_intercept(image, lines):
    "put each line in right and left bucket"
    # init the buckets
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        # calculates the slope and y intercept for given line defined by the co-ord
        # +ve slope = as x incr +v, y also incr +ve
        # polyfit function fits first degree polynomial function (y=mx+b) for given two points of degree 1
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        # returns a vector coefficient with slope and y intercept
        # print(parameters) - will print the 
        slope = parameters[0]
        intercept = parameters[1]
        # right side lines have +ve slope and left have -ve slopes
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
            
    # print(left_fit)
    # print(right_fit)
    # average out values vertically (hence axis=0)
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    # print(left_fit_average, 'left')
    # print(right_fit_average, 'right')
    # make the average values map to a single straight left and right line
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])


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
    line_image = np.zeros_like(image)
    if(lines is not None):
        for line in lines:
            # print(line)
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1),  (x2, y2), (255, 0, 0), 10)
    return line_image


def region_of_interest(image):
    #returns the height (bottom) of the image 
    height = image.shape[0] 
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

origimage = cv2.imread('test_image.jpg')
lane_image = np.copy(origimage)
canny_image = toCanny(lane_image)


cropped_image = region_of_interest(canny_image)
# calculate the hough lines from the cropped image
lines_hough = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
# calculate the averaged lines based off the hough lines
avg_lines = average_slope_intercept(lane_image, lines_hough)
# avg lines are straight than hough lines, hence use them to show
# as overlay on the original image
line_image = display_lines(lane_image, avg_lines) # try showing hough lines if you want to see them
combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
cv2.imshow("result", combo_image)
cv2.waitKey(0)

# plt.imshow(canny)
# plt.show()

# uncomment following to see line detection on video feed
'''
cap = cv2.VideoCapture("test2.mp4")
while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = toCanny(frame)
    cropped_image = region_of_interest(canny_image)
    lines_hough = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    avg_lines = average_slope_intercept(frame, lines_hough)
    line_image = display_lines(frame, avg_lines) # try showing hough lines if you want to see them
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow("result", combo_image)    
    if cv2.waitKey(1) == ord('q'):
        break;

cap.release()
cv2.destroyAllWindows()
'''
