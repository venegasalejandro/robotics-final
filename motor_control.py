"""
this is probably the most complicated module in the project.
we talk to our Arduino through this nifty little package called
Firmata, it is flashed onto the Arduinos which allows
for the Arduinos to be controlled through serial communication.
Moving on from that, this module checks for the red and blue
centroids in the shared memory space, when it finds them then
it controls the motors to try to push the centroids to each other.
upon seemingly colliding, the two robots randomly 'retreat' from
each other. the retreat is made up of both robots choosing 3
random directions and moving in those directions. after 'retreating',
the robots return to the image processing algorithm, and repeat
again, and so on.
additionally for some flair, on every iteration of the control
there is a random chance for either of the robots to twirl their
rods :)

there was the classic multithreading concern here and
in display_image about multiple threads reading and writing
to the shared memory. but after some research we found that
Python's list and dict structures were actually created with
this in mind and are safe to be accessed/modified across
multiple threads.
"""

import random
from time import sleep

from pyfirmata import ArduinoMega

EN_IDS = ["d:{}:p".format(x) for x in range(2, 7)]
IN_IDS = ["d:{}:o".format(x) for x in range(22, 42, 2)]
THESHOLD = 75

def init(com):
    board = ArduinoMega(com)
    ens = [board.get_pin(en_id) for en_id in EN_IDS]
    ins = [board.get_pin(in_id) for in_id in IN_IDS]

    for (index, in_pin) in enumerate(ins):
        in_pin.write(index % 2)

    def pack_motor_config(x):
        return {
            "en": ens[x],
            "in1": ins[x * 2],
            "in2": ins[x * 2 + 1],
        }

    motors = [pack_motor_config(x) for x in range(0, 5)]
    return (board, motors)

def actuate_motor(motor, value):
    motor.get("in1").write(0 if value > 0 else 1)
    motor.get("in2").write(1 if value > 0 else 0)
    motor.get("en").write(abs(value))

def motor_control(memory={}):
    board0, motors0 = init("COM10")
    board1, motors1 = init("COM11")

    [actuate_motor(motor, 0) for motor in motors0]
    [actuate_motor(motor, 0) for motor in motors1]
    sleep(1)

    retreating = 0
    while memory.get("running"):
        if retreating == 0:
            red_centroid = memory.get("red_centroid")
            blue_centroid = memory.get("blue_centroid")
            if (red_centroid is not None) and (blue_centroid is not None):
                red_centroid_x = red_centroid.get("x")
                red_centroid_y = red_centroid.get("y")
                red_contour_area = red_centroid.get("area")
                blue_centroid_x = blue_centroid.get("x")
                blue_centroid_y = blue_centroid.get("y")
                blue_contour_area = blue_centroid.get("area")

                error = (red_contour_area - blue_contour_area)
                if abs(error) > 300:
                    actuate_motor(motors0[4], 0.8 if error > 0 else -0.8)
                    actuate_motor(motors1[4], -0.8 if error > 0 else 0.8)
                dy = red_centroid_y - blue_centroid_y
                if abs(dy) > 20:
                    actuate_motor(motors0[1], 0.8 if dy > 0 else -0.8)
                    actuate_motor(motors1[1], -0.8 if dy > 0 else 0.8)
        else:
            random_motor = random.randint(0, 4)
            actuate_motor(motors0[random_motor], 0.8)
            actuate_motor(motors1[random_motor], -0.8)
            sleep(0.800)
            actuate_motor(motors0[random_motor], 0)
            actuate_motor(motors1[random_motor], 0)
            retreating -= 1

        roll = random.randint(0, 100)
        if roll <= 25 or (50 <= roll and roll <= 75):
            actuate_motor(motors0[0], 0.8)
            sleep(0.200)
            actuate_motor(motors0[0], 0)
        roll = random.randint(0, 100)
        if roll <= 25 or (50 <= roll and roll <= 75):
            actuate_motor(motors1[0], 0.8)
            sleep(0.200)
            actuate_motor(motors1[0], 0)
        sleep(0.100)

    [actuate_motor(motor, 0) for motor in motors0]
    [actuate_motor(motor, 0) for motor in motors1]
    board0.exit()
    board0.exit()
