import numpy as np
import pyvista as pv
from pyntcloud import PyntCloud

# Generate random point cloud data
points = np.random.rand(100, 3)

pt = PyntCloud.from_file('../data/birmingham_block_0/segmented-cloud-subsampled.ply')


# Create a PolyData object from the points
point_cloud = pv.PolyData(pt.points.loc[:20000, ['x', 'y', 'z']].values)

# Plot the point cloud
plotter = pv.Plotter()
plotter.add_mesh(point_cloud, color="green", point_size=5, render_points_as_spheres=True)
plotter.show()