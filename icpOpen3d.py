import time
import numpy as np
import open3d as o3d
from open3d.visualization import gui, rendering


def numpy_to_open3d(points_np, color=None):

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points_np)

    if color is not None:
        point_cloud.paint_uniform_color(color)

    return point_cloud
"""
converts a numpy array of 3d points into an open3d point cloud

parameters:
- points_np: numpy array with shape n x 3 containing point coordinates
- color: optional rgb color written as values from 0 to 1

what it returns:
- point_cloud: open3d point cloud object
"""




def run_open3d_icp(source_np, target_np, max_distance=1.0, max_iteration=80, tolerance=1e-6):


    source = numpy_to_open3d(source_np)
    target = numpy_to_open3d(target_np)

    initial_transformation = np.eye(4)

    criteria = o3d.pipelines.registration.ICPConvergenceCriteria(
        relative_fitness=tolerance,
        relative_rmse=tolerance,
        max_iteration=max_iteration
    )

    start_time = time.perf_counter()

    result = o3d.pipelines.registration.registration_icp(
        source,
        target,
        max_distance,
        initial_transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        criteria
    )

    end_time = time.perf_counter()

    source.transform(result.transformation)
    transformed_source_np = np.asarray(source.points)

    return (
        transformed_source_np,
        result.transformation,
        result.fitness,
        result.inlier_rmse,
        end_time - start_time
    )
"""
runs point to point icp using the open3d library

parameters:
- source_np: transformed point cloud that should be aligned to target
- target_np: reference point cloud
- max_distance: maximum allowed distance between corresponding points
- max_iteration: maximum number of icp iterations
- tolerance: stopping criterion based on relative fitness and rmse change

what it returns:
- transformed_source_np: source point cloud after icp alignment
- transformation: final 4x4 transformation matrix estimated by open3d icp
- fitness: ratio of inlier correspondences found by open3d
- rmse: root mean square error of inlier correspondences
- elapsed_time: icp execution time in seconds
"""





def visualize_before_after_open3d(source_before, target_before, source_after, target_after):


    before_source_cloud = numpy_to_open3d(
        source_before,
        color=[0.55, 0.12, 0.25]
    )

    before_target_cloud = numpy_to_open3d(
        target_before,
        color=[0.12, 0.23, 0.58]
    )

    after_source_cloud = numpy_to_open3d(
        source_after,
        color=[0.55, 0.12, 0.25]
    )

    after_target_cloud = numpy_to_open3d(
        target_after,
        color=[0.12, 0.23, 0.58]
    )

    o3d.visualization.draw_geometries(
        [
            before_source_cloud,
            before_target_cloud
        ],
        window_name="before icp"
    )

    o3d.visualization.draw_geometries(
        [
            after_source_cloud,
            after_target_cloud
        ],
        window_name="after icp"
    )


"""
^^^
shows before and after icp alignment in two separate open3d windows

parameters:
- source_before: source point cloud before icp alignment
- target_before: reference point cloud before icp alignment
- source_after: source point cloud after icp alignment
- target_after: reference point cloud after icp alignment

what it returns:
-none
"""