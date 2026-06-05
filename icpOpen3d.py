import time
import numpy as np
import open3d as o3d


def numpy_to_open3d(points_np, color=None):
    """
    converts a numpy array of 3D points into an open3D point cloud

    parameters:
    points_np: NumPy array with shape (n_points, 3)
    color: optional RGB color, for example [1, 0, 0]

    it returns:
    Open3D PointCloud object
    """

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points_np)

    if color is not None:
        point_cloud.paint_uniform_color(color)

    return point_cloud

