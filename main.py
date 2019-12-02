"""
entry point for robotic final project

from experience with OpenCV, our team knew to approach this
project with multithreading in mind, especially if we wanted to
see the image processing as it happened.

so basically 4 different threads were created for each of the tasks:
grabbing the raw image from the camera, processing the image, displaying
the image to watch the processing in action, and controlling the motors
"""

from threading import Thread

from display_image import display_image
from grab_image import grab_image
from motor_control import motor_control
from process_image import process_image


def main():
    """
    allocates shared memory variables, initializes all threads,
    starts all threads, then waits for all threads to end
    """
    memory = {
        "running": True,
        "raw_image": None,
        "red_centroid": None,
        "blue_centroid": None,
        "image": None,
    }
    threads = [
        Thread(name="grab_image", target=grab_image, args=(memory, )),
        Thread(name="process_image", target=process_image, args=(memory, )),
        Thread(name="display_image", target=display_image, args=(memory, )),
        Thread(name="motor_control", target=motor_control, args=(memory, )),
    ]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

if __name__ == "__main__":
    main()
