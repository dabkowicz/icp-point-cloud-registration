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


def run_open3d_icp(source_np, target_np, max_distance=0.5, max_iteration=50, tolerance=1e-6):
    source = numpy_to_open3d(source_np)
    target = numpy_to_open3d(target_np)

    init_transformation = np.eye(4)

    criteria = o3d.pipelines.registration.ICPConvergenceCriteria(
        relative_fitness=tolerance,
        relative_rmse=tolerance,
        max_iteration=max_iteration
    )

    estimation_method = o3d.pipelines.registration.TransformationEstimationPointToPoint()

    start = time.perf_counter()

    result = o3d.pipelines.registration.registration_icp(
        source,
        target,
        max_distance,
        init_transformation,
        estimation_method,
        criteria
    )

    end = time.perf_counter()
    elapsed_time = end - start

    source.transform(result.transformation)
    transformed_source_np = np.asarray(source.points)

    return (
        transformed_source_np,
        result.transformation,
        result.fitness,
        result.inlier_rmse,
        elapsed_time
    )
"""
^^^
runs the icp algorithm using the open3d library
it convers numpy point clouds to open3d format, performs point to point icp and
returns the aligned source cloud with quality metrics

parameters:
- source point cloud (transformed cloud to be aligned)
- target point cloud (reference cloud)
- max_distance (maximum correspondence distance)
- max_iteration (maximum number of icp iterations)
- tolerance (convergence tolerance for fitness and rmse)

it returns:
- aligned source cloud (source cloud after icp)
- transformation matrix (estimated 4x4 transform)
- fitness (ratio of inlier correspondences)
- rmse (root mean square error)
- elapsed time (execution time in seconds)
"""