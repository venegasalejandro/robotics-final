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
    # board1, motors1 = init("COM11")

    [actuate_motor(motor, 0) for motor in motors0]
    # [actuate_motor(motor, 0) for motor in motors1]
    sleep(1)

    # namaste
    actuate_motor(motors0[2], -0.8)
    # actuate_motor(motors1[2], -0.8)
    sleep(0.500)
    actuate_motor(motors0[2], 0.8)
    # actuate_motor(motors1[2], 0.8)
    sleep(0.500)
    actuate_motor(motors0[2], 0)
    # actuate_motor(motors1[2], 0)

    actuate_motor(motors0[4], 0.8)
    actuate_motor(motors0[4], 0)

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
                dy = red_centroid_y - blue_centroid_y
                if abs(dy) > 20:
                    actuate_motor(motors0[1], 0.8 if dy > 0 else -0.8)
        else:
            # random_motor = random.randint(0, 4)
            # actuate_motor(motors0[random_motor], 0.8)
            # actuate_motor(motors1[random_motor], -0.8)
            # sleep(0.800)
            # actuate_motor(motors0[random_motor], 0)
            # actuate_motor(motors1[random_motor], 0)
            retreating -= 1
        sleep(0.100)

    [actuate_motor(motor, 0) for motor in motors0]
    # [actuate_motor(motor, 0) for motor in motors1]
    board0.exit()
    board0.exit()
