from collections import deque
from imutils.video import WebcamVideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

class Video(object):
 def _init_(self):
        self.vs= WebcamVideoStream(src=0).start()

 def _del_(self):
        self.vs.stop()

 def detector(self):
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
    args = vars(ap.parse_args())

    greenLower = (29, 86, 40)
    greenUpper = (64, 255, 255)



    time.sleep(2.0)

    while True:
        Response, frame =self.vs.read()

        frame = frame[1] if args.get("video", False) else frame

        if frame is None:
            break

        frame = imutils.resize(frame, width=300)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        #cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
                     break
        ret, jpeg = cv2.imencode('.jpg',frame)
        data =[]
        data.append(jpeg.tobytes())
        return data

cv2.destroyAllWindows()