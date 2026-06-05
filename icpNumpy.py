import time
import numpy as np
from scipy.spatial import KDTree

def nearest_neighbors(source, target):
    tree  = KDTree(target)
    distances, indices = tree.query(source)

    return distances, indices

"""
^^^
finds the nearest target point for every source point

parametrs:
- source (point cloud that should be aligned to the target)
- target (reference point cloud)

it returns:
- distances (from source points to their nearest target points)
- indices (of the nearest target points)
"""


def best_fit_transform(source, target):

    centroid_source = np.mean(source, axis=0)
    centroid_target = np.mean(target, axis=0)

    source_centered = source - centroid_source
    target_centered = target - centroid_target

    covariance_matrix = source_centered.T @ target_centered

    U, _, Vt = np.linalg.svd(covariance_matrix)

    rotation_matrix = Vt.T @ U.T

    #it prevents reflection (ICP should use rotation not mirror reflection)
    if np.linalg.det(rotation_matrix) < 0:
        Vt[-1, :] *= -1
        rotation_matrix = Vt.T @ U.T

    translation_vector = centroid_target - rotation_matrix @ centroid_source

    return rotation_matrix, translation_vector

"""
^^^
computes the best rigid transformation between two corresponding point clouds
the function estimates a rotation matrix and a translation vector  
it uses an svd based method to find the rotation that minimizes the mean squared
distance between matching points
"""


def transform_point_cloud(points, rotation_matrix, translation_vector):
    return points @ rotation_matrix.T + translation_vector

#^ applies rotation and translation to a  point cloud



def run_numpy_icp(source, target, max_iterations=50, tolerance=1e-6):

    transformed_source = source.copy()
    errors = []

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

    return transformed_source, total_transformation, errors, elapsed_time



"""
^^^
this function runs the iterative closest point algorithm using numpy and scipy
aligns the source point cloud to the target by repeatedly finding nearest neighbors and estimating the best rigid transform

parameters
-source transformed point cloud that should be aligned
-target reference point cloud
-max iterations maximum number of icp iterations
-tolerance stopping criterion based on change in error

returns
-transformed source source cloud after alignment
-transformation matrix final 4x4 rigid transform
-errors list of mean errors from each iteration
-elapsed time total execution time

"""


def calculate_rmse(source, target):

    distances, _ = nearest_neighbors(source, target)
    rmse = np.sqrt(np.mean(distances ** 2))

    return rmse

#^^^ calculates RMSE between source points and their nearest target points