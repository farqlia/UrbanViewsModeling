import pycolmap
from pathlib import Path

scene_folder = Path('../data/matrix_city_aerial/train/sparse')
images_folder = scene_folder / 'images'

database_path = scene_folder / 'database.db'
reconstruction = pycolmap.Reconstruction(scene_folder / '0')

reconstruction.export_PLY(scene_folder / 'sparse.ply')



