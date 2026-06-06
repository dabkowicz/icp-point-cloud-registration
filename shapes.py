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
    generates a simplified 3d point cloud resembling classic paper 3d glasses

    parameters:
    n_points: number of generated points
    noise: gaussian noise level

    returns:
    points: generated point cloud
    """

    def generateRoundedLensPoints(n_points, center, width, height, thickness=0.025, noise=0.0):
        """
        generates a rounded rectangular lens
        """

        points = []

        while len(points) < n_points:
            x = np.random.uniform(-width / 2, width / 2)
            z = np.random.uniform(-height / 2, height / 2)

            test_value = (abs(x) / (width / 2)) ** 4 + (abs(z) / (height / 2)) ** 4

            if test_value <= 1:
                y = np.random.uniform(-thickness / 2, thickness / 2)
                points.append([x, y, z])

        points = np.array(points)
        points += np.array(center)

        if noise > 0:
            points += np.random.normal(0, noise, points.shape)

        return points

    def rotate_y(points, angle_deg):
        """
        rotates points around y axis
        """

        angle = np.radians(angle_deg)

        rotation = np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ])

        return points @ rotation.T

    frame_n = int(n_points * 0.44)
    lens_n = int(n_points * 0.24)
    temple_n = int(n_points * 0.22)
    bridge_n = int(n_points * 0.10)

    # lenses
    left_lens = generateRoundedLensPoints(
        n_points=lens_n // 2,
        center=(-0.58, 0.0, 0.02),
        width=0.58,
        height=0.42,
        thickness=0.02,
        noise=noise
    )

    right_lens = generateRoundedLensPoints(
        n_points=lens_n // 2,
        center=(0.58, 0.0, 0.02),
        width=0.58,
        height=0.42,
        thickness=0.02,
        noise=noise
    )

    # front frame
    top_bar = generateBoxSurfacePoints(
        n_points=frame_n // 5,
        center=(0.0, 0.0, 0.29),
        size=(1.65, 0.04, 0.08),
        noise=noise
    )

    left_bottom_bar = generateBoxSurfacePoints(
        n_points=frame_n // 7,
        center=(-0.58, 0.0, -0.28),
        size=(0.62, 0.04, 0.08),
        noise=noise
    )

    right_bottom_bar = generateBoxSurfacePoints(
        n_points=frame_n // 7,
        center=(0.58, 0.0, -0.28),
        size=(0.62, 0.04, 0.08),
        noise=noise
    )

    left_outer_bar = generateBoxSurfacePoints(
        n_points=frame_n // 8,
        center=(-0.92, 0.0, 0.00),
        size=(0.08, 0.04, 0.55),
        noise=noise
    )

    right_outer_bar = generateBoxSurfacePoints(
        n_points=frame_n // 8,
        center=(0.92, 0.0, 0.00),
        size=(0.08, 0.04, 0.55),
        noise=noise
    )

    left_inner_bar = generateBoxSurfacePoints(
        n_points=frame_n // 8,
        center=(-0.23, 0.0, 0.03),
        size=(0.07, 0.04, 0.47),
        noise=noise
    )

    right_inner_bar = generateBoxSurfacePoints(
        n_points=frame_n // 8,
        center=(0.23, 0.0, 0.03),
        size=(0.07, 0.04, 0.47),
        noise=noise
    )

    bridge_top = generateBoxSurfacePoints(
        n_points=bridge_n // 2,
        center=(0.0, 0.0, 0.10),
        size=(0.24, 0.04, 0.07),
        noise=noise
    )

    bridge_bottom_left = generateBoxSurfacePoints(
        n_points=bridge_n // 4,
        center=(-0.08, 0.0, -0.12),
        size=(0.10, 0.04, 0.20),
        noise=noise
    )

    bridge_bottom_right = generateBoxSurfacePoints(
        n_points=bridge_n // 4,
        center=(0.08, 0.0, -0.12),
        size=(0.10, 0.04, 0.20),
        noise=noise
    )

    # temples
    left_temple_main = generateBoxSurfacePoints(
        n_points=temple_n // 3,
        center=(-1.12, -0.45, 0.18),
        size=(0.10, 0.90, 0.08),
        noise=noise
    )

    right_temple_main = generateBoxSurfacePoints(
        n_points=temple_n // 3,
        center=(1.12, -0.45, 0.18),
        size=(0.10, 0.90, 0.08),
        noise=noise
    )

    left_temple_hook = generateBoxSurfacePoints(
        n_points=temple_n // 6,
        center=(-1.20, -0.85, 0.35),
        size=(0.10, 0.20, 0.35),
        noise=noise
    )

    right_temple_hook = generateBoxSurfacePoints(
        n_points=temple_n // 6,
        center=(1.20, -0.85, 0.35),
        size=(0.10, 0.20, 0.35),
        noise=noise
    )

    # slight perspective rotation so it looks more natural
    all_parts = [
        left_lens,
        right_lens,
        top_bar,
        left_bottom_bar,
        right_bottom_bar,
        left_outer_bar,
        right_outer_bar,
        left_inner_bar,
        right_inner_bar,
        bridge_top,
        bridge_bottom_left,
        bridge_bottom_right,
        left_temple_main,
        right_temple_main,
        left_temple_hook,
        right_temple_hook
    ]

    points = np.vstack(all_parts)
    points = rotate_y(points, -12)

    if noise > 0:
        points += np.random.normal(0, noise, points.shape)

    return points


def generateBoxSurfacePoints(n_points, center, size, noise=0.0):
    """
    generates points on the surface of a rectangular box

    parameters:
    n_points: number of generated points
    center: box center as x y z
    size: box dimensions as sx sy sz
    noise: gaussian noise level

    returns:
    points: generated point cloud
    """

    cx, cy, cz = center
    sx, sy, sz = size

    points = []

    for _ in range(n_points):
        face = np.random.randint(6)

        x = np.random.uniform(-sx / 2, sx / 2)
        y = np.random.uniform(-sy / 2, sy / 2)
        z = np.random.uniform(-sz / 2, sz / 2)

        if face == 0:
            x = -sx / 2
        elif face == 1:
            x = sx / 2
        elif face == 2:
            y = -sy / 2
        elif face == 3:
            y = sy / 2
        elif face == 4:
            z = -sz / 2
        else:
            z = sz / 2

        points.append([x + cx, y + cy, z + cz])

    points = np.array(points)

    if noise > 0:
        points += np.random.normal(0, noise, points.shape)

    return points