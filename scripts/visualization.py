import numpy as np
import pyvista as pv
from pyntcloud import PyntCloud

# Generate random point cloud data

pt = PyntCloud.from_file('../data/birmingham_block_0/segmented-cloud-subsampled-rgb.ply')

coords = pt.points[['x', 'y', 'z']].values

x = (coords[:, 0] - np.mean(coords[:, 0])) / np.std(coords[:, 0])
y = (coords[:, 1] - np.mean(coords[:, 1])) / np.std(coords[:, 1])
z = (coords[:, 2] - np.mean(coords[:, 2])) / np.std(coords[:, 2])

# Create a PolyData object from the points
point_cloud = pv.PolyData(np.column_stack([x, y, z]))
# point_cloud = pv.PolyData(coords)
point_cloud.cell_data['colors'] = pt.points[['red', 'green', 'blue']].values

print(pt.points.columns)
print(pt.points.iloc[0])
print(pt.points['red'].max(), pt.points['green'].max(), pt.points['blue'].max())
print(pt.points['red'].min(), pt.points['green'].min(), pt.points['blue'].min())

# Plot the point cloud
plotter = pv.Plotter()
plotter.add_mesh(point_cloud, point_size=3, render_points_as_spheres=True,
                 scalars='colors', lighting=False, rgb=True, preference='cell')
plotter.show()