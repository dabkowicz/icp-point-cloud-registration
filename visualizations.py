import numpy as np
import matplotlib.pyplot as plt


def set_axes_equal(ax):

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    y_range = abs(y_limits[1] - y_limits[0])
    z_range = abs(z_limits[1] - z_limits[0])

    max_range = max(x_range, y_range, z_range)

    x_middle = np.mean(x_limits)
    y_middle = np.mean(y_limits)
    z_middle = np.mean(z_limits)

    ax.set_xlim3d([x_middle - max_range / 2, x_middle + max_range / 2])
    ax.set_ylim3d([y_middle - max_range / 2, y_middle + max_range / 2])
    ax.set_zlim3d([z_middle - max_range / 2, z_middle + max_range / 2])
"""
makes all axes in a 3d plot have the same scale

parameters:
ax: matplotlib 3d axis object

what it returns:
none
"""




def plot_before_after_matplotlib(source_before, target_before, source_after, target_after, visualization_offset=(0.03, 0.03, 0.0)):
    target_color = "#1f3a93"
    source_color = "#8b1e3f"

    source_after_vis = source_after + np.array(visualization_offset)

    fig = plt.figure(figsize=(16, 7))

    fig.suptitle(
        "iterative closest point",
        fontsize=24,
        fontweight="bold"
    )

    fig.text(
        0.5,
        0.91,
        "before and after point cloud alignment",
        ha="center",
        fontsize=12
    )

    ax_before = fig.add_subplot(121, projection="3d")

    ax_before.scatter(
        target_before[:, 0],
        target_before[:, 1],
        target_before[:, 2],
        s=5,
        c=target_color,
        alpha=0.5,
        label="target"
    )

    ax_before.scatter(
        source_before[:, 0],
        source_before[:, 1],
        source_before[:, 2],
        s=5,
        c=source_color,
        alpha=0.5,
        label="source"
    )

    ax_before.set_title("before icp", fontsize=13)
    ax_before.set_xlabel("x")
    ax_before.set_ylabel("y")
    ax_before.set_zlabel("z")
    ax_before.view_init(elev=20, azim=-60)
    ax_before.legend()
    set_axes_equal(ax_before)

    ax_after = fig.add_subplot(122, projection="3d")

    ax_after.scatter(
        target_after[:, 0],
        target_after[:, 1],
        target_after[:, 2],
        s=5,
        c=target_color,
        alpha=0.5,
        label="target"
    )

    ax_after.scatter(
        source_after_vis[:, 0],
        source_after_vis[:, 1],
        source_after_vis[:, 2],
        s=5,
        c=source_color,
        alpha=0.5,
        label="source after icp"
    )

    ax_after.set_title("after icp", fontsize=13)
    ax_after.set_xlabel("x")
    ax_after.set_ylabel("y")
    ax_after.set_zlabel("z")
    ax_after.view_init(elev=20, azim=-60)
    ax_after.legend()
    set_axes_equal(ax_after)

    plt.tight_layout(rect=[0, 0, 1, 0.88])
    plt.show()
"""
shows point clouds before and after icp alignment in one matplotlib window

parameters:
- source_before: source point cloud before icp alignment
- target_before: reference point cloud before icp alignment
- source_after: source point cloud after icp alignment
- target_after: reference point cloud after icp alignment

what it returns:
    none
"""







def plot_icp_errors(errors):

    plt.figure(figsize=(8, 5))
    plt.plot(errors, marker="o", linewidth=2)

    plt.title("icp error in consecutive iterations")
    plt.xlabel("iteration")
    plt.ylabel("mean error")
    plt.grid(True)

    plt.tight_layout()
    plt.show()
"""
plots the mean icp error in consecutive iterations

parameters:
- errors: list of mean errors calculated during icp iterations

what it returns:
- none
"""




def print_result_summary(method_name, transformation, rmse, elapsed_time, fitness=None):

    print("\n" + "=" * 60)
    print(method_name)
    print("=" * 60)

    print("\nestimated transformation")
    print(transformation)

    print("\nrmse", rmse)

    if fitness is not None:
        print("fitness", fitness)

    print("time", elapsed_time, "s")

"""
prints a short summary of icp alignment results

parameters:
- method_name: name of the used icp method
- transformation: final 4x4 transformation matrix estimated by icp
- rmse: root mean square error after alignment
- elapsed_time: execution time in seconds
- fitness: optional open3d fitness value describing the ratio of inlier correspondences

what it returns:
- none
"""