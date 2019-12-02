import numpy as np

import cv2

RED_ROD_LOWER_BOUNDARY_HSV_COLOR = np.array([0,100,100])
RED_ROD_UPPER_BOUNDARY_HSV_COLOR = np.array([15,255,255])
BLUE_ROD_LOWER_BOUNDARY_HSV_COLOR = np.array([90,100,100])
BLUE_ROD_UPPER_BOUNDARY_HSV_COLOR = np.array([150,255,255])

def process_image(memory={}):
    while memory.get("running"):
        image = memory.get("raw_image")
        if image is not None:
            image = image.copy()
            image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            red_mask = cv2.inRange(image_hsv, RED_ROD_LOWER_BOUNDARY_HSV_COLOR, RED_ROD_UPPER_BOUNDARY_HSV_COLOR)
            red_masked_image = cv2.bitwise_and(image, image, mask=red_mask)
            red_median_blur = cv2.medianBlur(red_masked_image, 15)
            red_hsv = cv2.cvtColor(red_median_blur, cv2.COLOR_BGR2HSV)
            red_h, red_s, red_v = cv2.split(red_hsv)
            red_success, red_threshold = cv2.threshold(red_s, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            red_contours, red_hierarchy = cv2.findContours(red_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for (index, contour) in enumerate(red_contours):
                moments = cv2.moments(contour)
                if moments["m00"]:
                    red_centroid_x = int(moments["m10"] / moments["m00"])
                    red_centroid_y = int(moments["m01"] / moments["m00"])
                    memory["red_centroid"] = {
                        "x": red_centroid_x,
                        "y": red_centroid_y,
                        "area": moments["m00"],
                    }
                    cv2.drawContours(image, red_contours, index, (255,255,255), 3)
                    cv2.circle(image, (red_centroid_x, red_centroid_y), 5, (255, 255, 255), -1)
                    break

            blue_mask = cv2.inRange(image_hsv, BLUE_ROD_LOWER_BOUNDARY_HSV_COLOR, BLUE_ROD_UPPER_BOUNDARY_HSV_COLOR)
            blue_masked_image = cv2.bitwise_and(image, image, mask=blue_mask)
            blue_median_blur = cv2.medianBlur(blue_masked_image, 15)
            blue_hsv = cv2.cvtColor(blue_median_blur, cv2.COLOR_BGR2HSV)
            blue_h, blue_s, blue_v = cv2.split(blue_hsv)
            blue_success, blue_threshold = cv2.threshold(blue_s, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            blue_contours, blue_hierarchy = cv2.findContours(blue_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for (index, contour) in enumerate(blue_contours):
                moments = cv2.moments(contour)
                if moments["m00"]:
                    blue_centroid_x = int(moments["m10"] / moments["m00"])
                    blue_centroid_y = int(moments["m01"] / moments["m00"])
                    memory["blue_centroid"] = {
                        "x": blue_centroid_x,
                        "y": blue_centroid_y,
                        "area": moments["m00"],
                    }
                    cv2.drawContours(image, blue_contours, index, (255,255,255), 3)
                    cv2.circle(image, (blue_centroid_x, blue_centroid_y), 5, (255, 255, 255), -1)
                    break

            memory["image"] = image
