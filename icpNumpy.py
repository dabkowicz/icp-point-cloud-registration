import time
import numpy as np
from scipy.spatial import KDTree

def nearest_neighbors(source, target):
    tree  = KDTree(source)
    distances, indices = tree.query(target)

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