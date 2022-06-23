import numpy as np
import cv2
from matplotlib import pyplot as plt

# read images
imgL = cv2.imread('imgs/CameraScreenShot_L.png', 0)
imgR = cv2.imread('imgs/CameraScreenShot_R.png', 0)

# estimate depth
# stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
# stereo = cv2.StereoBM_create(numDisparities=96, blockSize=15)
stereo = cv2.StereoBM_create(numDisparities=64, blockSize=15)
disparity_px_16 = stereo.compute(imgL, imgR)

# # raw output
# plt.figure(figsize=(13,3))
# plt.imshow(disparity_px_16)
# plt.colorbar()
# plt.show()

# # output value in pixel
# plt.figure(figsize=(13,3))
# plt.imshow(disparity_px_16/16)
# plt.colorbar()
# plt.show()

# camera parameters
fov = 90  # [deg]
B = 20  # [cm]
width = disparity_px_16.shape[1]  # [px]
# f = 1.0 # [cm]

# ratio: px per cm
fov_ = fov * np.pi / 180  # [rad]
ratio = (width/2) / np.tan(fov_/2)

# convert disparity to depth
depth = B * ratio * 16.0 / disparity_px_16
# this line above is equivalent to the line below
# depth = B * f / (disparity_px_16 / 16.0 / ratio)

# set unexpected values to zero 
depth[np.where(depth < 0)] = 0
depth[np.where(depth > 500)] = 0

# show result
plt.imshow(depth)
plt.colorbar()
plt.show()