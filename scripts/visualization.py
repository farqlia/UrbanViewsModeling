import numpy as np
import pandas as pd
import pyvista as pv
from pyntcloud import PyntCloud

# Generate random point cloud data

pt = PyntCloud.from_file('../data/cambridge_blocks/cambridge_block_4_subsampled.ply')

# pt.points['class'] = pt.points['scalar_class'].astype(int)

coords = pt.points[['x', 'y', 'z']].values

"""x = (coords[:, 0] - np.mean(coords[:, 0])) / np.std(coords[:, 0])
y = (coords[:, 1] - np.mean(coords[:, 1])) / np.std(coords[:, 1])
z = (coords[:, 2] - np.mean(coords[:, 2])) / np.std(coords[:, 2])"""

x = (coords[:, 0] - np.min(coords[:, 0])) / (np.max(coords[:, 0]) - np.min(coords[:, 0]))
y = (coords[:, 1] - np.min(coords[:, 1])) / (np.max(coords[:, 1]) - np.min(coords[:, 1]))
z = (coords[:, 2] - np.min(coords[:, 2])) / (np.max(coords[:, 2]) - np.min(coords[:, 2]))

# Create a PolyData object from the points
point_cloud = pv.PolyData(np.column_stack([x, y, z]))
# point_cloud = pv.PolyData(coords)


print(pt.points.iloc[0])
# point_cloud.save('../data/birmingham_blocks/birmingham_block_6_normalized.ply')

def color_with_labels(points):
    classes = points['class'].unique().astype(int)
    colors = np.random.uniform(size=(len(classes), 3))
    colored_classes = pd.DataFrame(colors, index=classes, columns=['r', 'g', 'b'])
    red = colored_classes.loc[points['class'], 'r']
    green = colored_classes.loc[points['class'], 'g']
    blue = colored_classes.loc[points['class'], 'b']

    return np.column_stack((red, green, blue)), colored_classes

# point_cloud = pv.PolyData(coords)
colors, colored_classes = color_with_labels(pt.points)
point_cloud.cell_data['colors'] = colors


# Plot the point cloud
plotter = pv.Plotter()
plotter.add_mesh(point_cloud, point_size=3, render_points_as_spheres=True,
                 scalars='colors', lighting=False, rgb=True, preference='cell')

legend = [
    [str(label), [float(row['r']), float(row['g']), float(row['b'])], "circle"] for label, row in colored_classes.iterrows()
]

print(legend)

plotter.add_legend(legend)

plotter.show()