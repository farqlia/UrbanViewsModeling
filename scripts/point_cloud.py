import pycolmap
from pathlib import Path

scene_folder = Path('../data/south-building')
images_folder = scene_folder / 'images'

database_path = scene_folder / 'database.db'
reconstruction = pycolmap.Reconstruction(scene_folder)

print(reconstruction.summary())

camera = reconstruction.cameras[1]
img = reconstruction.images[1]
point = reconstruction.points3D[1].xyz

print(camera.img_from_cam())

print(pycolmap.has_cuda)



