import time, sys, cv2, mss, numpy as np
from pynput.mouse import Button, Controller

# control mouse input
mouse = Controller()

# timeout for timing clicks
timeout = True

# Determine if you want sniper or DMR
picture = ""
extraReloadTime = 0
if len(sys.argv) == 2:
    print(sys.argv)
    if(sys.argv[1] == "1"):
        picture = "SniperReticle.png"
        print("Sniper")
        extraReloadTime = 0.3
    if(sys.argv[1] == "2"):
        picture = "ShotgunCrop.png"
        print("shotgun")
else:
    picture = "DMRreticle.png"
    print("DMR")

# read image and convert to HSV
blue = cv2.imread(picture)
hsv = cv2.cvtColor(blue, cv2.COLOR_BGR2HSV)

# create blue color spaces
low_blue = np.array([100, 50, 70])
high_blue = np.array([255, 255, 255])

# create mask from reticle color
mask = cv2.inRange(hsv, low_blue, high_blue)

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 520, "left": 940, "width": 42, "height": 42}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))

        # Apply mask to get only reticle color
        res = cv2.bitwise_and(img, img, mask=mask)

        # Get average pixel color
        average = cv2.mean(res, mask=mask)
        # print(average)

        # Display the picture
        cv2.imshow("Mask", mask)
        cv2.imshow("res", res)

        # print("fps: {}".format(1 / (time.time() - last_time)))

        if((float(average[0]) > 10 and float(average[0]) < 90) and (float(average[2]) > 130 and float(average[2]) < 180)):
            # if (float(average[0]) < 15 ):
            timeout = True
            if timeout == True:
                mouse.press(Button.left)
                timeout = False
                time.sleep(0.1)
                mouse.release(Button.left)
                # print("click")
                time.sleep(0.2 + extraReloadTime)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
