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


def generateBoxSurfacePoints(n_points, center, size, noise=0.0):
    """
    generates points on the surface of a rectangular box

    parameters:
    n_points: number of generated points
    center: center of the box
    size: box size in x y z directions
    noise: gaussian noise level

    returns:
    points: generated box surface point cloud
    """

    center = np.array(center)
    size = np.array(size)

    points = []

    for _ in range(n_points):
        face = np.random.randint(0, 6)

        x = np.random.uniform(-size[0] / 2, size[0] / 2)
        y = np.random.uniform(-size[1] / 2, size[1] / 2)
        z = np.random.uniform(-size[2] / 2, size[2] / 2)

        if face == 0:
            x = -size[0] / 2
        elif face == 1:
            x = size[0] / 2
        elif face == 2:
            y = -size[1] / 2
        elif face == 3:
            y = size[1] / 2
        elif face == 4:
            z = -size[2] / 2
        else:
            z = size[2] / 2

        points.append([x, y, z])

    points = np.array(points)
    points += center

    if noise > 0:
        points += np.random.normal(0, noise, points.shape)

    return points


def generateRoundedLensPoints(n_points, center, width, height, thickness=0.03, noise=0.0):
    """
    generates points inside a rounded rectangular lens

    parameters:
    n_points: number of generated points
    center: center of the lens
    width: lens width
    height: lens height
    thickness: lens thickness
    noise: gaussian noise level

    returns:
    points: generated lens point cloud
    """

    points = []

    while len(points) < n_points:
        x = np.random.uniform(-width / 2, width / 2)
        z = np.random.uniform(-height / 2, height / 2)

        rounded_limit = (abs(x) / (width / 2)) ** 4 + (abs(z) / (height / 2)) ** 4

        if rounded_limit <= 1:
            y = np.random.uniform(-thickness / 2, thickness / 2)
            points.append([x, y, z])

    points = np.array(points)
    points += np.array(center)

    if noise > 0:
        points += np.random.normal(0, noise, points.shape)

    return points


def generate3DGlassesPoints(n_points=4000, noise=0.0):
    """
    generates a simplified 3d point cloud resembling anaglyph 3d glasses

    parameters:
    n_points: number of generated points
    noise: gaussian noise level

    returns:
    points: generated 3d glasses point cloud
    """

    frame_n = int(n_points * 0.38)
    lens_n = int(n_points * 0.36)
    bridge_n = int(n_points * 0.08)
    temple_n = int(n_points * 0.18)

    left_lens = generateRoundedLensPoints(
        n_points=lens_n // 2,
        center=(-0.65, 0, 0),
        width=0.75,
        height=0.42,
        thickness=0.025,
        noise=noise
    )

    right_lens = generateRoundedLensPoints(
        n_points=lens_n // 2,
        center=(0.65, 0, 0),
        width=0.75,
        height=0.42,
        thickness=0.025,
        noise=noise
    )

    top_frame = generateBoxSurfacePoints(
        n_points=frame_n // 4,
        center=(0, 0, 0.32),
        size=(1.85, 0.08, 0.10),
        noise=noise
    )

    bottom_frame = generateBoxSurfacePoints(
        n_points=frame_n // 4,
        center=(0, 0, -0.32),
        size=(1.85, 0.08, 0.10),
        noise=noise
    )

    left_outer_frame = generateBoxSurfacePoints(
        n_points=frame_n // 8,
        center=(-1.08, 0, 0),
        size=(0.10, 0.08, 0.65),
        noise=noise
    )

    right_outer_frame = generateBoxSurfacePoints(
        n_points=frame_n // 8,
        center=(1.08, 0, 0),
        size=(0.10, 0.08, 0.65),
        noise=noise
    )

    left_inner_frame = generateBoxSurfacePoints(
        n_points=frame_n // 8,
        center=(-0.18, 0, 0),
        size=(0.08, 0.08, 0.55),
        noise=noise
    )

    right_inner_frame = generateBoxSurfacePoints(
        n_points=frame_n // 8,
        center=(0.18, 0, 0),
        size=(0.08, 0.08, 0.55),
        noise=noise
    )

    bridge = generateBoxSurfacePoints(
        n_points=bridge_n,
        center=(0, 0, 0.08),
        size=(0.38, 0.08, 0.10),
        noise=noise
    )

    left_temple = generateBoxSurfacePoints(
        n_points=temple_n // 2,
        center=(-1.35, -0.55, 0.05),
        size=(0.10, 1.10, 0.08),
        noise=noise
    )

    right_temple = generateBoxSurfacePoints(
        n_points=temple_n // 2,
        center=(1.35, -0.55, 0.05),
        size=(0.10, 1.10, 0.08),
        noise=noise
    )

    points = np.vstack((
        left_lens,
        right_lens,
        top_frame,
        bottom_frame,
        left_outer_frame,
        right_outer_frame,
        left_inner_frame,
        right_inner_frame,
        bridge,
        left_temple,
        right_temple
    ))

    return points