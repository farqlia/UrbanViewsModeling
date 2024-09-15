import pycolmap
from pathlib import Path
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from src.geometry.point_transformation import *

scene_folder = Path('../data/south-building')
images_folder = scene_folder / 'images'
database_path = scene_folder / 'database.db'
output_path = scene_folder / 'undistorted_images'

reconstruction = pycolmap.Reconstruction(output_path / 'sparse')

img_id = 1
img = reconstruction.images[img_id]
cam_id = 1

extrinsic_matrix = get_extrinsic_params(img.cam_from_world)
f, cx, cy = reconstruction.cameras[cam_id].params
width, height = reconstruction.cameras[cam_id].width, reconstruction.cameras[cam_id].height
znear, zfar = 1, 5
intrinsic_matrix = get_intrinsic_opengl_params(f, f, height, width, zfar=zfar, znear=znear)

colors = np.array([p.color for p in reconstruction.points3D.values()]) / 255.0
homogeneous_points = convert_to_homogenous(get_points_xyz(reconstruction))
camera_coordinates = homogeneous_points @ extrinsic_matrix.T
clip_coordinates = camera_coordinates @ intrinsic_matrix.T
point_ids = cull_coordinates_ids(clip_coordinates, camera_coordinates, zfar=zfar, znear=znear)

ndc_coordinates = to_ndc_coordinates(clip_coordinates[point_ids])
c = colors[point_ids]

screen_coordinates = to_screen_coordinates(ndc_coordinates, width, height, zfar, znear)
image = mpimg.imread(images_folder / f'{img.name}')
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.scatter(screen_coordinates[:, 0], -screen_coordinates[:, 1], s=2, c=c)
plt.subplot(1, 2, 2)
plt.imshow(image)
plt.show()

