import time
import numpy as np
import open3d as o3d


def numpy_to_open3d(points_np, color=None):
    """
    converts a numpy array of 3d points into an open3d point cloud

    parameters:
    points_np: numpy array with shape n x 3 containing point coordinates
    color: optional rgb color written as values from 0 to 1

    returns:
    point_cloud: open3d point cloud object
    """

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points_np)

    if color is not None:
        point_cloud.paint_uniform_color(color)

    return point_cloud


def run_open3d_icp(source_np, target_np, max_distance=1.0, max_iteration=80, tolerance=1e-6):
    """
    runs point to point icp using the open3d library

    parameters:
    source_np: transformed point cloud that should be aligned to target
    target_np: reference point cloud
    max_distance: maximum allowed distance between corresponding points
    max_iteration: maximum number of icp iterations
    tolerance: stopping criterion based on relative fitness and rmse change

    returns:
    transformed_source_np: source point cloud after icp alignment
    transformation: final 4x4 transformation matrix estimated by open3d icp
    fitness: ratio of inlier correspondences found by open3d
    rmse: root mean square error of inlier correspondences
    elapsed_time: icp execution time in seconds
    """

    source = numpy_to_open3d(source_np)
    target = numpy_to_open3d(target_np)

    initial_transformation = np.eye(4)

    criteria = o3d.pipelines.registration.ICPConvergenceCriteria(
        relative_fitness=tolerance,
        relative_rmse=tolerance,
        max_iteration=max_iteration
    )

    start_time = time.perf_counter()

    result = o3d.pipelines.registration.registration_icp(
        source,
        target,
        max_distance,
        initial_transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        criteria
    )

    end_time = time.perf_counter()

    source.transform(result.transformation)
    transformed_source_np = np.asarray(source.points)

    return (
        transformed_source_np,
        result.transformation,
        result.fitness,
        result.inlier_rmse,
        end_time - start_time
    )


def visualize_before_after_open3d(source_before, target_before, source_after, target_after):
    """
    shows before and after icp alignment in one open3d window

    parameters:
    source_before: source point cloud before icp alignment
    target_before: reference point cloud before icp alignment
    source_after: source point cloud after icp alignment
    target_after: reference point cloud after icp alignment

    returns:
    none
    """

    all_points = np.vstack((
        source_before,
        target_before,
        source_after,
        target_after
    ))

    x_span = np.max(all_points[:, 0]) - np.min(all_points[:, 0])
    offset = np.array([x_span + 2.5, 0.0, 0.0])

    source_before_left = source_before.copy()
    target_before_left = target_before.copy()

    source_after_right = source_after.copy() + offset
    target_after_right = target_after.copy() + offset

    before_source_cloud = numpy_to_open3d(
        source_before_left,
        color=[0.45, 0.00, 0.07]
    )

    before_target_cloud = numpy_to_open3d(
        target_before_left,
        color=[0.17, 0.21, 0.42]
    )

    after_source_cloud = numpy_to_open3d(
        source_after_right,
        color=[0.45, 0.00, 0.07]
    )

    after_target_cloud = numpy_to_open3d(
        target_after_right,
        color=[0.17, 0.21, 0.42]
    )

    o3d.visualization.draw_geometries(
        [
            before_source_cloud,
            before_target_cloud,
            after_source_cloud,
            after_target_cloud
        ],
        window_name="before icp on the left and after icp on the right",
        width=1600,
        height=900,
        left=50,
        top=50
    )

def animate_icp_open3d(target, history, interval=0.08):
        """
        animates icp alignment process using open3d

        parameters:
        target: reference point cloud
        history: list of source point clouds saved after consecutive icp iterations
        interval: delay between animation frames in seconds

        returns:
        none
        """

        import time

        target_cloud = numpy_to_open3d(
            target,
            color=[0.17, 0.21, 0.42]
        )

        source_cloud = numpy_to_open3d(
            history[0],
            color=[0.45, 0.00, 0.07]
        )

        visualizer = o3d.visualization.Visualizer()
        visualizer.create_window(
            window_name="open3d icp animation",
            width=1600,
            height=900,
            left=50,
            top=50
        )

        visualizer.add_geometry(target_cloud)
        visualizer.add_geometry(source_cloud)

        render_option = visualizer.get_render_option()
        render_option.point_size = 3.0
        render_option.background_color = np.array([0.96, 0.95, 0.93])

        view_control = visualizer.get_view_control()
        view_control.set_zoom(0.75)

        frame_index = 0
        last_update_time = time.time()

        def animation_callback(vis):
            nonlocal frame_index
            nonlocal last_update_time

            current_time = time.time()

            if current_time - last_update_time >= interval:
                current_source = history[frame_index]

                source_cloud.points = o3d.utility.Vector3dVector(current_source)
                vis.update_geometry(source_cloud)

                frame_index += 1

                if frame_index >= len(history):
                    frame_index = 0

                last_update_time = current_time

            return False

        visualizer.register_animation_callback(animation_callback)
        visualizer.run()
        visualizer.destroy_window()