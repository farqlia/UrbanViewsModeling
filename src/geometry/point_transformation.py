import numpy as np
import pycolmap

def get_camera_from_image(image: pycolmap.Image):
    return image.cam_from_world


def get_extrinsic_params(camera: pycolmap.Rigid3d):
    return np.concatenate((camera.matrix(), np.array([[0, 0, 0, 1]])))


def get_intrinsic_params(reconstruction: pycolmap.Reconstruction):
    '''
    Assumes that there is only one camera, and it is a PINHOLE camera
    :param reconstruction: reconstruction object
    :return: 3x4 intrinsic matrix
    '''
    f, cx, cy = reconstruction.cameras[1].params
    intrinsic_matrix = np.array([[f, 0, cx, 0], [0, f, cy, 0], [0, 0, 1, 0]])
    return intrinsic_matrix


def get_points_xyz(reconstruction: pycolmap.Reconstruction):
    return np.array([point.xyz for point in reconstruction.points3D.values()])


def points3D_to_np(points) -> np.array:
    return np.array([point.xyz for point in points])


def convert_to_homogenous(points: np.array) -> np.array:
    return np.concatenate((points, np.ones((len(points), 1), np.float32)), axis=1)


def convert_from_homogenous(points):
    x = points[:, 0] / points[:, 2]
    y = points[:, 1] / points[:, 2]
    return x, y


def filter_view_points(img_points: np.array, colors: np.array, width: int, height: int):
    points_ids = np.where((img_points[:, 0] > 0) & (img_points[:, 0] < width) & (img_points[:, 1] > 0) & (img_points[:, 1] < height))[0]
    selected_points = img_points[points_ids]
    selected_colors = colors[points_ids]
    return selected_points, selected_colors


def to_camera_viewpoint(reconstruction: pycolmap.Reconstruction, img_id: int):
    extrinsic_matrix = get_extrinsic_params(get_camera_from_image(reconstruction.images[img_id]))
    homogenous_points = convert_to_homogenous(get_points_xyz(reconstruction)).T

    projected_to_camera_viewpoint = (extrinsic_matrix @ homogenous_points)



def projection_from_reconstruction(reconstruction: pycolmap.Reconstruction, img_id: int):
    extrinsic_matrix = get_extrinsic_params(get_camera_from_image(reconstruction.images[img_id]))
    intrinsic_matrix = get_intrinsic_params(reconstruction)
    homogenous_points = convert_to_homogenous(get_points_xyz(reconstruction)).T

    projected_to_camera_viewpoint = (extrinsic_matrix @ homogenous_points)
    projected_to_image_plane = (intrinsic_matrix @ projected_to_camera_viewpoint).T

    x, y = convert_from_homogenous(projected_to_image_plane)
    img_points = np.stack((x, y)).T
    c = np.array([p.color for p in reconstruction.points3D.values()]) / 255.0

    return img_points, c


def projection_from_points(reconstruction: pycolmap.Reconstruction, points3D, img_id: int):
    extrinsic_matrix = get_extrinsic_params(get_camera_from_image(reconstruction.images[img_id]))
    intrinsic_matrix = get_intrinsic_params(reconstruction)
    homogenous_points = convert_to_homogenous(points3D_to_np(points3D)).T

    projected_to_camera_viewpoint = (extrinsic_matrix @ homogenous_points)
    projected_to_image_plane = (intrinsic_matrix @ projected_to_camera_viewpoint).T

    x, y = convert_from_homogenous(projected_to_image_plane)
    img_points = np.stack((x, y)).T
    c = np.array([p.color for p in points3D]) / 255.0

    return img_points, c