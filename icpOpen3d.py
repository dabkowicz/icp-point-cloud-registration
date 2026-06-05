import numpy as np
import open3d as o3d

def run_open3d_icp(source_np, target_np, max_distance=0.5, max_iteration=50, tolerance =1e-6):

    #numpy data do open3d
    source = o3d.geometry.PointCloud()
    source.points = o3d.utility.Vector3dVector(source_np)

    target = o3d.geometry.PointCloud()
    target.points = o3d.utility.Vector3dVector(target_np)

    #trsnsformation matrix
    init_transformation = np.eye(4)
    criteria = o3d.pipelines.registration.ICPConvergenceCriteria(
        relative_fitness=tolerance,
        relative_rmse = tolerance,
        max_iteration=max_iteration,
    )

    estimation_method = o3d.pipelines.registration.TransformationEstimationPointToPoint()
    #algorithm
    result = o3d.pipelines.registration.registration_icp(
        source,
        target,
        max_distance,
        init_transformation,
        estimation_method,
        criteria
    )

    source.transform(result.transformation)
    transformed_source_np = np.asarray(source.points)

    return transformed_source_np, result.fitness, result.inlier_rmse

