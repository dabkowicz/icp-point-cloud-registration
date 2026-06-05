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

"""
^^^
these 3 functions create a 3D rotation matrix around x,y, z the x, y and z axis (input angle is given in degrees)
"""


def create_transformation_matrix(rotation, translation):
    transformation = np.eye(4)
    transformation[:3, :3] = rotation
    transformation[:3, 3] = translation

    return transformation


#use of a ready-made 4x4 matrix
def apply_transformation(points, transformation):
    ones = np.ones((points.shape[0], 1))
    homogeneous_points = np.hstack((points, ones))

    transformed_points = (transformation @ homogeneous_points.T).T

    return transformed_points[:, :3]
"""
this function takes 3D points and temporarily transforms them into a homogeneous form: [x, y, z, 1]

because of this a 4x4 transformation matrix can then simultaneously perform:
                            rotation + translation
"""


def transform_points(points, angle_x=0, angle_y=0, angle_z=0, translation=(0,0,0)):
    rx = rotation_matrix_x(angle_x)
    ry = rotation_matrix_y(angle_y)
    rz = rotation_matrix_z(angle_z)

    rotation = rz @ ry @ rx

    transformation = create_transformation_matrix( rotation=rotation, translation=np.array(translation) )

    transformed_points = apply_transformation(points, transformation)

    return transformed_points, transformation

"""
this function creates rotation matrices around the x, y and z axes, combines them into one rotation matrix, builds a 4x4 transformation
matrix and applies it to the input point cloud

in return we have:
- transformed_points: transformed version of the input point cloud,
- transformation: the exact transformation matrix used to generate it

the returned matrix can later be compared with the transformation estimated by the ICP algorithm

"""