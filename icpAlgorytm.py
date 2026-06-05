import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
#import open3d as o3d
import time

""" 
how this algorithm works? 
1. take the source
2. find the closest target point for each source
3. calculate the best rotation and translation
4. move the source
5. record the error
6. repeat until the error stops decreasing
"""

def createBoxPoints():

    """
    generates points on the surface of a three-dimensional box
    """

    points = []
    for x in np.linspace(0, 1, 10):
        for y in np.linspace(0, 1, 10):
            points.append([x, y, 0])
            points.append([x, y, 1])
            points.append([0, x, y])
            points.append([1, x, y])
            points.append([x, 0, y])
            points.append([x, 1, y])

    return np.unique(points, axis=0)

#def createShape():



def transformPointCloud(points, R, t):
    return np.dot(points, R.T) + t


def addNoise(points, noise_level=0.02):
    """gaussian noise as a simulation"""
    noise = np.random.normal(0, noise_level, points.shape)
    return points + noise



def nearestNeighbors(source, target):
    """
    finds the nearest target point for every source point
    """

    tree = KDTree(target)
    dist, ind = tree.query(source)

    return dist, ind


def bestFitTransform(source, target):
    centroid_source = np.mean(source, axis=0)
    centroid_target = np.mean(target, axis=0)

    source_centered = source - centroid_source
    target_centered = target - centroid_target

    covariance_matrix = source_centered.T @ target_centered

    U, _, Vt = np.linalg.svd(covariance_matrix)

    rotation_matrix = Vt.T @ U.T

    if np.linalg.det(rotation_matrix) < 0:
        Vt[-1, :] *= -1
        rotation_matrix = Vt.T @ U.T

    translation_vector = centroid_target - rotation_matrix @ centroid_source

    return rotation_matrix, translation_vector



def runICP(source, target, max_iterations=50, tolerance=1e-6):


    transformed_source = source.copy()
    errors = []   #creation of error list

    for iteration in range(max_iterations):   #iterative loop(default maximum 50 iterations)
        distances, indices = nearestNeighbors(transformed_source, target)

        matched_target = target[indices]   #target cloud


        #calculation of the best rotation and shift
        rotation_matrix, translation_vector = bestFitTransform(
            transformed_source,
            matched_target
        )


        #cloud location update
        transformed_source = transformPointCloud(
            transformed_source,
            rotation_matrix,
            translation_vector
        )


#mean error as the average distance between each source point and its closest target point
        mean_error = np.mean(distances)
        errors.append(mean_error)

        if iteration > 0 and abs(errors[-2] - errors[-1]) < tolerance:
            break

    return transformed_source, errors