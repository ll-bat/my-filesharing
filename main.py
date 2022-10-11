import numpy as np
import pyautogui
import imutils
import cv2

image = pyautogui.screenshot()
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
cv2.imwrite("in_memory_to_disk.png", image)

image = cv2.imread("in_memory_to_disk.png")
cv2.imshow("Screenshot", imutils.resize(image, width=900))
cv2.waitKey(0)