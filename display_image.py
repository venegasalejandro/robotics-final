import cv2


def display_image(memory={}):
    while memory.get("running"):
        image = memory.get("image")
        if image is not None:
            cv2.imshow("Demo 4", image)
        if cv2.waitKey(25) == ord("q"):
            memory["running"] = False
    cv2.destroyAllWindows()
