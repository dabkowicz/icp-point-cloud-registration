import numpy as np


def generateCubePoints(n_points=1000, size=1.0, noise=0.0):

    points = np.random.uniform(-size, size, (n_points, 3))

    if noise > 0:
        points += np.random.normal(0, noise, points.shape)

    return points


def generateSpherePoints(n_points=1000, radius=1.0, noise=0.0):
    phi = np.random.uniform(0, 2 * np.pi, size=n_points)
    costheta = np.random.uniform(-1, 1, size=n_points)
    theta = np.arccos(costheta)

    x = radius * np.sin(theta) * np.cos(phi)
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * np.cos(theta)

    points = np.column_stack((x, y, z))

    if noise > 0:
        points += np.random.normal(0, noise, points.shape)

    return points



def generateEllipsoidPoints(n_points, center, radii, noise=0.0):
    """
    generates points on the surface of an ellipsoid
    center: center [x, y, z]
    radii: radii [rx, ry, rz]
    """

    phi = np.random.uniform(0, 2 * np.pi, size=n_points)
    costheta = np.random.uniform(-1, 1, size=n_points)
    theta = np.arccos(costheta)

    x = radii[0] * np.sin(theta) * np.cos(phi)
    y = radii[1] * np.sin(theta) * np.sin(phi)
    z = radii[2] * np.cos(theta)

    points = np.column_stack((x, y, z))
    points += np.array(center)

    if noise > 0:
        points += np.random.normal(0, noise, points.shape)

    return points


def generateBeakPoints(n_points, start=(1.25, 0, 0.95), length=0.9, base_y=0.32, base_z=0.18, noise=0.0):
    """
    generates points that form a duckbill
    the beak is simplified as a flattened cone directed in the X axis
    """

    t = np.random.uniform(0, 1, size=n_points)
    angle = np.random.uniform(0, 2 * np.pi, size=n_points)

    x = start[0] + length * t

    radius_y = base_y * (1 - t)
    radius_z = base_z * (1 - t)

    y = start[1] + radius_y * np.cos(angle)
    z = start[2] + radius_z * np.sin(angle)

    points = np.column_stack((x, y, z))

    if noise > 0:
        points += np.random.normal(0, noise, points.shape)

    return points


def generateRubberDuckPoints(n_points=4000, noise=0.0):
    """
    generates a simplified 3D point cloud resembling a bathing duck
    the shape consists of a body, head, beak, eyes, and wings
    """

    body_n = int(n_points * 0.38)
    head_n = int(n_points * 0.22)
    beak_n = int(n_points * 0.12)
    wing_n = int(n_points * 0.16)
    eye_n = int(n_points * 0.06)

    body = generateEllipsoidPoints(
        n_points=body_n,
        center=(0, 0, 0),
        radii=(1.6, 0.85, 0.75),
        noise=noise
    )

    head = generateEllipsoidPoints(
        n_points=head_n,
        center=(0.85, 0, 0.95),
        radii=(0.65, 0.55, 0.60),
        noise=noise
    )

    beak = generateBeakPoints(
        n_points=beak_n,
        start=(1.35, 0, 0.95),
        length=0.75,
        base_y=0.28,
        base_z=0.16,
        noise=noise
    )

    left_wing = generateEllipsoidPoints(
        n_points=wing_n // 2,
        center=(-0.25, 0.78, 0.1),
        radii=(0.75, 0.12, 0.42),
        noise=noise
    )

    right_wing = generateEllipsoidPoints(
        n_points=wing_n // 2,
        center=(-0.25, -0.78, 0.1),
        radii=(0.75, 0.12, 0.42),
        noise=noise
    )

    left_eye = generateEllipsoidPoints(
        n_points=eye_n // 2,
        center=(1.22, 0.33, 1.15),
        radii=(0.08, 0.08, 0.08),
        noise=noise
    )

    right_eye = generateEllipsoidPoints(
        n_points=eye_n // 2,
        center=(1.22, -0.33, 1.15),
        radii=(0.08, 0.08, 0.08),
        noise=noise
    )

    points = np.vstack((
        body,
        head,
        beak,
        left_wing,
        right_wing,
        left_eye,
        right_eye
    ))

    return points