import time
import cv2
import numpy as np


def nothing(x):
    pass


# Starting Webcam to capture video
cap = cv2.VideoCapture(0)

# Wait for 2 seconds and capture background image
time.sleep(2)

print('Background capture')

for i in range(10):
    _, bg = cap.read()

# Flip image horizontally
bg = np.flip(bg, axis=1)

# Enable Trackbar below to decide the HSV values for your invisibility cloak

# cv2.namedWindow('Trackbars')
# cv2.createTrackbar('LH', 'Trackbars', 0, 179, nothing)
# cv2.createTrackbar('LS', 'Trackbars', 0, 255, nothing)
# cv2.createTrackbar('LV', 'Trackbars', 0, 255, nothing)
# cv2.createTrackbar('UH', 'Trackbars', 179, 179, nothing)
# cv2.createTrackbar('US', 'Trackbars', 255, 255, nothing)
# cv2.createTrackbar('UV', 'Trackbars', 255, 255, nothing)

# start loop for capturing the video and performing masking operations on each frame
while True:

    # Cap Frame and convert it from RGB to HSV

    _, frame = cap.read()
    frame = np.flip(frame, axis=1)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Enable trackbar variables when you want to change HSV values live for your cloak

    # lh = cv2.getTrackbarPos('LH', 'Trackbars')
    # ls = cv2.getTrackbarPos('LS', 'Trackbars')
    # lv = cv2.getTrackbarPos('LV', 'Trackbars')
    # uh = cv2.getTrackbarPos('UH', 'Trackbars')
    # us = cv2.getTrackbarPos('US', 'Trackbars')
    # uv = cv2.getTrackbarPos('UV', 'Trackbars')
    # low_m = np.array([lh, ls, lv])
    # high_m = np.array([uh, us, uv])

    # Here, I have used the HSV range from low_m, high_m for blue cloak
    low_m = np.array([0, 0, 98])
    high_m = np.array([179, 37, 202])

    # Create a mask with the HSV values as range
    m1 = cv2.inRange(hsv_frame, low_m, high_m)

    # Apply Morphology techniques to get rid of noise from the mask
    m1 = cv2.morphologyEx(m1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    m1 = cv2.morphologyEx(m1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)

    # Create the mask for background by excluding everything from first mask i.e. cloak
    m2 = cv2.bitwise_not(m1)

    # Overlap respective masks m1 with background to depict invisibility and m2 with our frame to get everything
    # except cloak with bitwise and operation
    res1 = cv2.bitwise_and(bg, bg, mask=m1)
    res2 = cv2.bitwise_and(frame, frame, mask=m2)

    # Merge these 2 masks to create our final frame by weighted addition
    finalframe = cv2.addWeighted(res1, 1, res2, 1, 0)

    # Now show the final frame
    cv2.imshow('Invisible', finalframe)

    # Terminate everything and close windows when ESC key is encountered
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
