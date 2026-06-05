import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
import time

"""
how this algorithm works:
1. take the source cloud
2. find the closest target point for each source point
3. calculate the best rotation and translation
4. move the source cloud
5. record the error
6. repeat until the error stops decreasing
"""


def createBoxPoints():

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
 #^^^generates points on the surface of a three-dimensional box




def transformPointCloud(points, rotation_matrix, translation_vector):

    return np.dot(points, rotation_matrix.T) + translation_vector
#^^^applies rotation and translation to a point cloud




def addNoise(points, noise_level=0.02):

    noise = np.random.normal(0, noise_level, points.shape)
    return points + noise
#^^^adds Gaussian noise to simulate measurement errors




def nearestNeighbors(source, target):

    tree = KDTree(target)
    distances, indices = tree.query(source)

    return distances, indices
#^^^finds the nearest target point for every source point





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
#^^^computes the best rotation and translation that aligns source to target uses SVD




def runICP(source, target, max_iterations=50, tolerance=1e-6):

    transformed_source = source.copy()
    errors = []

    for iteration in range(max_iterations):
        distances, indices = nearestNeighbors(transformed_source, target)

        matched_target = target[indices]

        rotation_matrix, translation_vector = bestFitTransform(
            transformed_source,
            matched_target
        )

        transformed_source = transformPointCloud(
            transformed_source,
            rotation_matrix,
            translation_vector
        )

        mean_error = np.mean(distances)
        errors.append(mean_error)

        if iteration > 0 and abs(errors[-2] - errors[-1]) < tolerance:
            break

    return transformed_source, errors
#^^^ runs the Iterative Closest Point algorithm



def paintClouds(source, target, title="Point cloud visualization"):


    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(target[:, 0], target[:, 1], target[:, 2], s=10, label="target")
    ax.scatter(source[:, 0], source[:, 1], source[:, 2], s=10, label="source")

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()

    plt.show()
#it visualise two point clouds

def plotErrors(errors):

    plt.figure(figsize=(7, 5))
    plt.plot(errors, marker="o")
    plt.title("ICP error in consecutive iterations")
    plt.xlabel("iteration")
    plt.ylabel("mean error")
    plt.grid(True)
    plt.show()

#^^^plots ICP error in consecutive iterations

def main():
    target = createBoxPoints()

    angle = np.radians(35)

    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle),  np.cos(angle), 0],
        [0,              0,             1]
    ])

    translation_vector = np.array([0.7, 0.4, 0.3])

    source = transformPointCloud(target, rotation_matrix, translation_vector)
    source = addNoise(source, noise_level=0.01)

    paintClouds(source, target, "before ICP")

    start = time.perf_counter()
    aligned_source, errors = runICP(source, target)
    end = time.perf_counter()

    paintClouds(aligned_source, target, "after ICP")
    plotErrors(errors)

    print("number of iterations:", len(errors))
    print("final error:", errors[-1])
    print("ICP time:", end - start, "s")


if __name__ == "__main__":
    main()