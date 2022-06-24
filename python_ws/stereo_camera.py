import numpy as np
import cv2
from matplotlib import pyplot as plt
import open3d as o3d

# read images
# imgL = cv2.imread('imgs/CameraScreenShot_L.png', 0)
# imgR = cv2.imread('imgs/CameraScreenShot_R.png', 0)
imgL = cv2.imread('imgs/testL.png', 0)
imgR = cv2.imread('imgs/testR.png', 0)

# estimate depth
# stereo = cv2.StereoBM_create(numDisparities=64, blockSize=15) # 高速
stereo = cv2.StereoSGBM_create(numDisparities=64, blockSize=15) # 信頼性が高い．
disparity_px_16 = stereo.compute(imgL, imgR)

disparity = disparity_px_16/16.0

# # output value in pixel
# plt.figure(figsize=(13,3))
# plt.imshow(disparity)
# plt.colorbar()
# plt.show()

# camera parameters
B = 200 # [mm]
# B = 0.2 # [m]

_f = 18 # [mm]
mmToPx = 640.0 / 36.0 # センサーサイズ 640px / 36mm.
f = mmToPx * _f

# convert disparity to depth
depth = ( B * f ) / (disparity)

# this line above is equivalent to the line below
# depth = B * f / (disparity_px_16 / 16.0 / ratio)

# set unexpected values to zero 
depth[np.where(depth < 0)] = 0
depth[np.where(depth > 5000)] = 0
# depth[np.where(depth > 5)] = 0

# show result
plt.imshow(depth)
plt.colorbar()
# plt.show()

print(depth)

# depth image to pointcloud
image_height, image_width  = depth.shape
fx = _f * (image_width  / 36.0) # [pixel]
fy = _f * (image_height / 27.0) # [pixel]
cx = image_width  / 2.0 # [pixel]
cy = image_height / 2.0 # [pixel]
camera_intrinsics = o3d.camera.PinholeCameraIntrinsic(image_width, image_height, fx, fy, cx, cy)

# o3d_depth = o3d.Image(depth)
# pcd = o3d.geometry.PointCloud.create_from_depth_image(o3d_depth, camera_intrinsics)
#         # np.identity(4))
#         # depth_scale=1)
#         # depth_trunc=10000.0)
# print('asdfasdfa')

# pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
# print(np.asarray(pcd.points)[1,:])
# o3d.visualization.draw_geometries([pcd])

# 点群型データ作成
pcd = o3d.geometry.PointCloud()

color_img = cv2.imread('imgs/testL.png')
for h in range(image_height):
        for w in range(image_width):
                d = depth[h, w]
                # sub_x = d * np.sin( np.arctan2((w - cx) , fx) ) # [mm]
                # sub_y = d * np.cos( np.arctan2((w - cx) , fx) ) # [mm]
                # sub_z = d * np.cos( np.arctan2((h - cy) , fy) ) # [mm]

                # sub_x = w
                # sub_y = h
                # sub_z = d

                # 座標設定
                sub_x = (d * (w - cx)) / fx
                sub_y = (d * (h - cy)) / fy
                sub_z = d

                pcd.points.append([sub_x, sub_y, sub_z])

                B, G, R = color_img[h, w]
                # pcd.colors.append([int(R), int(G), int(B)])
                pcd.colors.append([R/255.0, G/255.0, B/255.0])
                # pcd.colors.append([255, 255, 1])
                # print(int(R), int(G), int(B))

pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
o3d.visualization.draw_geometries([pcd])

plt.show()
