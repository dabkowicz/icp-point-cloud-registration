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


