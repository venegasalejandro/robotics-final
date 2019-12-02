from threading import Thread

from display_image import display_image
from grab_image import grab_image
from motor_control import motor_control
from process_image import process_image


def main():
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
