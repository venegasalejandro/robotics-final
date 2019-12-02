"""
this module is pretty simple and straight forward
only in charge of display the process imaged that
has been placed in shared memory.

OpenCVs GUI is a light wonky. OpenCV only draws when
cv2.waitKey is called, so to keep the image realtime
it is better to have an image grabbing and processing
be done on a separate thread and allow image displaying
to run independently and as fast as it can.

there was the classic multithreading concern here and
in motor_control about multiple threads reading and writing
to the shared memory. but after some research we found that
Python's list and dict structures were actually created with
this in mind and are safe to be accessed/modified across
multiple threads.
"""

import cv2


def display_image(memory={}):
    while memory.get("running"):
        image = memory.get("image")
        if image is not None:
            cv2.imshow("Demo 4", image)
        if cv2.waitKey(25) == ord("q"):
            memory["running"] = False
    cv2.destroyAllWindows()
