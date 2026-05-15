import numpy as np
import matplotlib.pyplot as plt
import cv2
import mss
import time
import pyautogui
from skimage.measure import label, regionprops
from skimage.morphology import opening, closing

game_borders = {"left": 660, "top": 310, "width": 700, "height": 170}

def screen_capture(region):
    with mss.mss() as sct:
        image = sct.grab(region)
        return np.array(image)[:, :, :-1]
    
def classificate_region(region):
    region_box = region.bbox
    if region_box[2] < 115:
        if region_box[2] < 90:
            return 'bird3'
        #print(region_box)
        return 'bird2'
    else:
        if region_box[3] - region_box[1] > 50:
            return 'wide'
        return 'narrow'

start_time = time.monotonic()
speed_mult = 1
pyautogui.press('space')
while True:
    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.destroyAllWindows()
        break
    screenshot = screen_capture(game_borders)
    grayscale = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(grayscale, 150, 1, cv2.THRESH_BINARY_INV)
    binary = opening(binary, np.ones((3, 3)))
    binary = closing(binary, np.ones((5, 5)))
    labeled = label(binary)
    rprops = regionprops(labeled)

    leftmost = None
    leftmost_coord = 10**10
    for region in rprops:
        if region.bbox[1] < leftmost_coord and region.bbox[1] > 20:
            leftmost_coord = region.bbox[1]
            leftmost = region
    
    obj_type = None
    if leftmost is not None:
        obj_type = classificate_region(leftmost)
        if obj_type == 'narrow':
            jump_range = leftmost_coord - 170 * speed_mult
        elif obj_type == 'wide':
            jump_range = leftmost_coord - 140 * speed_mult
        elif obj_type == 'bird2':
            jump_range = leftmost_coord - 50 * speed_mult**0.5
        else:
            jump_range = 1
    else:
        jump_range = 1

    if obj_type != 'bird2':
        if jump_range <= 0:
            pyautogui.press('space')
    else:
        if jump_range <= 0:
            pyautogui.keyDown('down')
            time.sleep(0.1)
            pyautogui.keyUp('down')


    end_time = time.monotonic()
    curr_time = end_time - start_time
    speed_mult = min(max((curr_time / 25)**0.5, 1), 2.35)

    cv2.imshow("Press q to stop", screenshot)

print(curr_time, speed_mult)
#plt.imshow(binary)
#plt.show()