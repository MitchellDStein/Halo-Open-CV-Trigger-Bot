import time

import cv2
import mss
import numpy as np
from pynput.mouse import Button, Controller

mouse = Controller()

timeout = True

blue = cv2.imread("Shotgun.png")
crop_img = blue[470:595, 895:1010]
cv2.imwrite("ShotgunCrop.png", crop_img)
hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

low_blue = np.array([100, 50, 50])
high_blue = np.array([255, 255, 255])

# create mask from reticle color
mask = cv2.inRange(hsv, low_blue, high_blue)
# inverse mask
mask_inv = cv2.bitwise_not(mask)

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 520, "left": 940, "width": 42, "height": 42}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))

        # Apply mask to get only reticle color
        # res = cv2.bitwise_and(img, img, mask=mask)

        # Get average pixel color
        # average = cv2.mean(res, mask=mask)
        # print(average)

        # Display the picture
        # cv2.imshow("cropped", crop_img)
        # cv2.imshow("Mask", mask)
        # cv2.imshow("res", res)
        cv2.imshow("blue", crop_img)


        # print("fps: {}".format(1 / (time.time() - last_time)))

        # if((float(average[0]) > 10 and float(average[0]) < 90) and (float(average[2]) > 130 and float(average[2]) < 180)):
        #     # if (float(average[0]) < 15 ):
        #     timeout = True
        #     if timeout == True:
        #         # mouse.press(Button.left)
        #         timeout = False
        #         time.sleep(0.1)
        #         # mouse.release(Button.left)
        #         print("click")
        #         time.sleep(0.2)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
