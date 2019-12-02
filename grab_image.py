"""
this module is pretty simple and straight forward
only in charge of grabbing the raw image and placing
it into shared memory.
"""

import cv2


def grab_image(memory={}):
    video_capture = cv2.VideoCapture(1)
    while memory.get("running"):
        success, image = video_capture.read()
        if success:
            memory["raw_image"] = image
    video_capture.release()
