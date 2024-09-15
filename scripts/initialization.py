import open3d as o3d
from pathlib import Path
import numpy as np

scene_folder = Path('../data/south-building')
images_folder = scene_folder / 'images'
database_path = scene_folder / 'database.db'
output_path = scene_folder / 'undistorted_images'

pcd = o3d.io.read_point_cloud(str(scene_folder / 'sparse.ply'))
pcd.estimate_covariances(search_param=o3d.geometry.KDTreeSearchParamKNN(knn=3))
print(np.asarray(pcd.covariances).shape)

points = np.asarray(pcd.points)
colors = np.asarray(pcd.colors)
cov_3d = np.asarray(pcd.covariances)

np.save(output_path / 'points.npy', points)
np.save(output_path / 'colors.npy', colors)
np.save(output_path / 'cov_3d.npy', cov_3d)