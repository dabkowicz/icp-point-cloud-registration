import time
import numpy as np
from scipy.spatial import KDTree


def nearest_neighbors(source, target):
    """
    finds the nearest target point for every source point

    parameters:
    source: point cloud that should be aligned to the target
    target: reference point cloud

    returns:
    distances: distances from source points to their nearest target points
    indices: indices of the nearest target points
    """

    tree = KDTree(target)
    distances, indices = tree.query(source)

    return distances, indices


def best_fit_transform(source, target):
    """
    computes the best rigid transformation between two corresponding point clouds

    parameters:
    source: source point cloud with already matched correspondences
    target: target point cloud with already matched correspondences

    returns:
    rotation_matrix: estimated 3x3 rotation matrix
    translation_vector: estimated 3d translation vector
    """

    centroid_source = np.mean(source, axis=0)
    centroid_target = np.mean(target, axis=0)

    source_centered = source - centroid_source
    target_centered = target - centroid_target

    covariance_matrix = source_centered.T @ target_centered

    u, _, vt = np.linalg.svd(covariance_matrix)

    rotation_matrix = vt.T @ u.T

    if np.linalg.det(rotation_matrix) < 0:
        vt[-1, :] *= -1
        rotation_matrix = vt.T @ u.T

    translation_vector = centroid_target - rotation_matrix @ centroid_source

    return rotation_matrix, translation_vector


def transform_point_cloud(points, rotation_matrix, translation_vector):
    """
    applies rotation and translation to a point cloud

    parameters:
    points: input point cloud
    rotation_matrix: 3x3 rotation matrix
    translation_vector: 3d translation vector

    returns:
    transformed_points: point cloud after rotation and translation
    """

    transformed_points = points @ rotation_matrix.T + translation_vector

    return transformed_points


def run_numpy_icp(source, target, max_iterations=50, tolerance=1e-6, save_history=False):
    """
    runs the iterative closest point algorithm using numpy and scipy

    parameters:
    source: transformed point cloud that should be aligned to target
    target: reference point cloud
    max_iterations: maximum number of icp iterations
    tolerance: stopping criterion based on the error change
    save_history: if true saves source cloud after every iteration

    returns:
    transformed_source: source point cloud after icp alignment
    total_transformation: final 4x4 transformation matrix estimated by icp
    errors: list of mean errors from consecutive iterations
    elapsed_time: icp execution time in seconds
    history: optional list of source clouds from consecutive iterations
    """

    transformed_source = source.copy()
    errors = []
    history = []

    if save_history:
        history.append(transformed_source.copy())

    total_transformation = np.eye(4)

    start_time = time.perf_counter()

    for iteration in range(max_iterations):
        distances, indices = nearest_neighbors(transformed_source, target)

        matched_target = target[indices]

        rotation_matrix, translation_vector = best_fit_transform(
            transformed_source,
            matched_target
        )

        transformed_source = transform_point_cloud(
            transformed_source,
            rotation_matrix,
            translation_vector
        )

        if save_history:
            history.append(transformed_source.copy())

        step_transformation = np.eye(4)
        step_transformation[:3, :3] = rotation_matrix
        step_transformation[:3, 3] = translation_vector

        total_transformation = step_transformation @ total_transformation

        mean_error = np.mean(distances)
        errors.append(mean_error)

        if iteration > 0 and abs(errors[-2] - errors[-1]) < tolerance:
            break

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    if save_history:
        return transformed_source, total_transformation, errors, elapsed_time, history

    return transformed_source, total_transformation, errors, elapsed_time


def calculate_rmse(source, target):
    """
    calculates rmse between source points and their nearest target points

    parameters:
    source: source point cloud after alignment
    target: reference point cloud

    returns:
    rmse: root mean square error between source and nearest target points
    """

    distances, _ = nearest_neighbors(source, target)
    rmse = np.sqrt(np.mean(distances ** 2))

    return rmse