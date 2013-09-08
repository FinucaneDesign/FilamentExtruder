# By Patrick Finucane (9-7-2013)
#
# Except where otherwise noted, this work is licensed under
# http://creativecommons.org/licenses/by-sa/3.0/
#
#
#
# NO WARRANTY

import numpy as np          # note that numby is required
import cv2                  # note this mostly uses cv2
import cv2.cv as cv         # just in case you need cv vs cv2
import time                 #


# name some windows...
cv2.namedWindow ('contour')
cv2.namedWindow ('thresh')

# Test image not used...
im = cv2.imread('test.jpg')

# set up the capature object
cap = cv2.VideoCapture(1)

# Set up the recording code
###############################################################################
flag, frame = cap.read() # **EDIT:** to get frame size
width = np.size(frame, 1) #here is why you need numpy!  (remember to "import numpy as np")
height = np.size(frame, 0)

# Uncomment the following line to enable recording
#writer = cv2.VideoWriter(filename="your_writing_file.avi", 
fourcc=cv.CV_FOURCC('i','Y', 'U', 'V'), #this is the codec that works for me
fps=15, #frames per second, I suggest 315 as a rough initial estimate
frameSize=(width, height)
###############################################################################

while True:

     ret,img = cap.read()
     
     # print type(im)
     # print type(img)

     #gray = cv2.CreateImage(cv2.GetSize(img), 8, 1)
     #cv2.CvtColor(img, gray, cv2.CV_RGB2GRAY)

     # turn the image gray
     imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
     
     # Only look at the middle of the image 
     crop_img = imgray[0:680, 300:320]
     
     #
     # A simple threshold function to find the edges
     ret,thresh = cv2.threshold(crop_img,80,255,0)
     
     # Pull out the contours from 
     contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
     
     cnt = contours[0]
     
     # print cnt
     # time.sleep(5.5)  
     
     # Find min's and max's but these are not used
     min_val, max_val, min_loc,max_loc = cv2.minMaxLoc(imgray)
     
     # print ("min: " + str(min_val) + ", max_val: " + str(max_val) + ", min_loc: " + str(min_loc) + ", max_loc: " + str(max_loc))
     
     # Find the top and bottom contours
     topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
     bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
     
     # Calculate the heigh in px
     height = bottommost[1] - topmost[1]
     
     # print height

     # add contours to img
     cv2.drawContours(img,contours,-1,(0,255,0),offset=(300,0))
     
     # set the locations
     x1 = (250,topmost[1])
     x2 = (290,topmost[1])
     x3 = (250,bottommost[1])
     x4 = (290,bottommost[1])
     x5 = (290,topmost[1]-15)
     
     # set the color
     color = (0, 0, 255)
     thickness = 2
     
     # add the lines
     cv2.line(img, x1, x2, (0, 0, 255), 3)
     cv2.line(img, x3,x4,color, thickness)
     
     # add the text
     textString = "Height: " + str(height) + " px"
     cv2.putText(img,textString, x5, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color)
     
     # Create a couple of windows
     cv2.imshow ('contour', img)
     cv2.imshow ('thresh', thresh)
     
     # this writes the edited image to the file (Uncomment to use)
     #writer.write(img) #write to the video file
     
     # allow a break
     k = cv2.waitKey(10)     
     
     #print k
     if k == 27:                # press ETC to break... if that doesn't work
          break                 # press crtl+C a bunch of times
     
