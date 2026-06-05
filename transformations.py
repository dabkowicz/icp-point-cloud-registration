import numpy as np

def rotation_matrix_x(angle_deg):
    angle = np.radians(angle_deg)

    return np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle),  np.cos(angle)]
    ])


def rotation_matrix_y(angle_deg):
    angle = np.radians(angle_deg)

    return np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])


def rotation_matrix_z(angle_deg):
    angle = np.radians(angle_deg)

    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle),  np.cos(angle), 0],
        [0, 0, 1]
    ])


def create_transformation_matrix(rotation, translation):
    transformation = np.eye(4)
    transformation[:3, :3] = rotation
    transformation[:3, 3] = translation

    return transformation



def apply_transformation(points, transformation):
    ones = np.ones((points.shape[0], 1))
    homogeneous_points = np.hstack((points, ones))

    transformed_points = (transformation @ homogeneous_points.T).T

    return transformed_points[:, :3]



def transform_points(points, angle_x=0, angle_y=0, angle_z=0, translation=(0,0,0)):
    rx = rotation_matrix_x(angle_x)
    ry = rotation_matrix_y(angle_y)
    rz = rotation_matrix_z(angle_z)

    rotation = rz @ ry @ rx

    transformation = create_transformation_matrix( rotation=rotation, translation=np.array(translation) )

    transformed_points = apply_transformation(points, transformation)

    return transformed_points, transformation