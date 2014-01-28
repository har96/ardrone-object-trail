#!/usr/bin/env python
'''
=======================
=======================
'''

# Import/use system module
import sys

# Import/use OpenCV module
import cv2
import numpy as np
import cone_track
#from drone_control import Drone

SAFE_OFFSET = 50

# Print OpenCV version
print "OpenCV version:", cv2.__version__

# Capture numbers for video camera
#  0 = /dev/video0
#  1 = /dev/video1
#  etc...

#
#  Parse the input command line
#
video_path = None
if len(sys.argv) == 2:
    vidnum = sys.argv[1]
    if not vidnum.isdigit():
        video_path = vidnum
else:
    vidnum = 0

if not video_path:
	print "Using /dev/video%d" % int(vidnum)
	print " press 'q' to quit"

#
#  Setup video capture
#
#	cap = cv2.VideoCapture(int(vidnum))
else:
    print "Using %s" % video_path
   # cap = cv2.VideoCapture(video_path)

def draw_crosshairs(frame, rect):
    x,y,w,h = rect
    cv2.line(frame, (x-5, y+(h/2)), (x+w+5, y+(h/2)), cv2.cv.RGB(255,0,0))
    cv2.line(frame, (x+(w/2), y-5), (x+(w/2), y+h+5), cv2.cv.RGB(255,0,0))
    return frame

#drone = Drone(safe_offset=25)
#drone.launch()
#
#  Loop until 'q' is pressed
#
def main_loop():
    while(True):

        # capture frame from camera
        frame = cv2.imread("out.jpeg", cv2.CV_LOAD_IMAGE_COLOR)

        if frame is None:
    		continue
    	# Scale down frame
        #frame = cv2.resize(frame, (0,0), frame, 0.25, 0.25, cv2.INTER_AREA)

        rects = []
        for x,y,w,h in cone_track.get_obs(frame):
            rects.append( (x,y,w,h) )
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        if rects:
            rects.sort(key=lambda x: x[2]*x[3], reverse=True)
            max_rect = rects[0]
            frame = draw_crosshairs(frame, max_rect)
    		#drone.track_target(max_rect)
        else:
			#drone.stop()
            pass

        # display on screen camera frame
        cv2.line(frame, (320-SAFE_OFFSET, 0), (320-SAFE_OFFSET, 360), cv2.cv.RGB(0,0,0), 4)
        cv2.line(frame, (320+SAFE_OFFSET, 0), (320+SAFE_OFFSET, 360), cv2.cv.RGB(0,0,0), 4)
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xff == ord('p'):
            cv2.imshow('pic', frame)
            cv2.imwrite('pic.jpg', frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break


#  
#  Release video capture object
#
#cap.release()

#
#  Close and destroy display window
#
try:
    main_loop()
except:
	#drone.done()
    pass

cv2.destroyAllWindows()
