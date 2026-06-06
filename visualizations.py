import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


blue_depths = "#2c356a"
dark_ruby = "#720013"
meteorite = "#2c2929"
cultured_pearl = "#f5f4f2"
catacomb_walls = "#dcd7d4"

def animate_icp_alignment(target, history, errors=None, interval=450):
    """
    animates icp alignment process step by step using matplotlib

    parameters:
    target: reference point cloud
    history: list of source point clouds saved after consecutive icp iterations
    errors: optional list of mean errors from consecutive iterations
    interval: delay between animation frames in milliseconds

    returns:
    none
    """

    fig = plt.figure(
        figsize=(16, 9),
        facecolor=cultured_pearl
    )

    maximize_matplotlib_window()

    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#fbfaf8")

    fig.suptitle(
        "iterative closest point animation",
        fontsize=28,
        fontweight="bold",
        color=dark_ruby
    )

    fig.text(
        0.5,
        0.925,
        "source cloud is gradually aligned with the target cloud",
        ha="center",
        fontsize=13,
        color=meteorite
    )

    ax.scatter(
        target[:, 0],
        target[:, 1],
        target[:, 2],
        s=4,
        c=blue_depths,
        alpha=0.45,
        label="target"
    )

    source_plot = ax.scatter(
        history[0][:, 0],
        history[0][:, 1],
        history[0][:, 2],
        s=4,
        c=dark_ruby,
        alpha=0.55,
        label="source"
    )

    ax.set_title(
        "iteration 0",
        fontsize=15,
        color=meteorite
    )

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.view_init(elev=20, azim=-60)
    ax.legend()

    all_points = np.vstack([target] + history)

    ax.set_xlim(np.min(all_points[:, 0]), np.max(all_points[:, 0]))
    ax.set_ylim(np.min(all_points[:, 1]), np.max(all_points[:, 1]))
    ax.set_zlim(np.min(all_points[:, 2]), np.max(all_points[:, 2]))
    set_axes_equal(ax)

    info_box = fig.text(
        0.5,
        0.045,
        "",
        ha="center",
        fontsize=12,
        color=meteorite,
        bbox=dict(
            facecolor=cultured_pearl,
            edgecolor=catacomb_walls,
            boxstyle="round,pad=0.6"
        )
    )

    def update(frame):
        current_source = history[frame]

        source_plot._offsets3d = (
            current_source[:, 0],
            current_source[:, 1],
            current_source[:, 2]
        )

        ax.set_title(
            f"iteration {frame}",
            fontsize=15,
            color=meteorite
        )

        if errors is not None and frame > 0 and frame - 1 < len(errors):
            info_box.set_text(
                f"iteration: {frame}     mean error: {errors[frame - 1]:.6f}"
            )
        else:
            info_box.set_text(
                f"iteration: {frame}"
            )

        return source_plot,

    animation = FuncAnimation(
        fig,
        update,
        frames=len(history),
        interval=interval,
        blit=False,
        repeat=True
    )

    plt.tight_layout(rect=[0, 0.07, 1, 0.89])
    plt.show()




def set_axes_equal(ax):
    """
    makes all axes in a 3d plot have the same scale

    parameters:
    ax: matplotlib 3d axis object

    returns:
    none
    """

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


def maximize_matplotlib_window():
    """
    tries to maximize matplotlib window

    parameters:
    none

    returns:
    none
    """

    manager = plt.get_current_fig_manager()

    try:
        manager.window.state("zoomed")
    except Exception:
        try:
            manager.full_screen_toggle()
        except Exception:
            pass


def prepare_axis(ax, title):
    """
    prepares one 3d axis for point cloud visualization

    parameters:
    ax: matplotlib 3d axis object
    title: plot title

    returns:
    none
    """

    ax.set_title(
        title,
        fontsize=14,
        color=meteorite
    )

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    ax.set_facecolor("#fbfaf8")
    ax.view_init(elev=20, azim=-60)


def plot_before_after_matplotlib(
        source_before,
        target_before,
        source_after,
        target_after,
        visualization_offset=(0.03, 0.03, 0.0),
        info_text=None
):
    """
    shows before and after icp alignment as two separate 3d plots in one window

    parameters:
    source_before: source point cloud before icp alignment
    target_before: reference point cloud before icp alignment
    source_after: source point cloud after icp alignment
    target_after: reference point cloud after icp alignment
    visualization_offset: small shift used only for better visibility after alignment
    info_text: optional text displayed at the bottom of the figure

    returns:
    none
    """

    source_after_vis = source_after + np.array(visualization_offset)

    fig = plt.figure(
        figsize=(16, 8),
        facecolor=cultured_pearl
    )

    maximize_matplotlib_window()

    fig.suptitle(
        "iterative closest point algorithm",
        fontsize=26,
        fontweight="bold",
        color=dark_ruby
    )

    fig.text(
        0.5,
        0.93,
        "comparison of source and target point clouds before and after alignment",
        ha="center",
        fontsize=13,
        color=meteorite
    )

    ax_before = fig.add_subplot(121, projection="3d")

    ax_before.scatter(
        target_before[:, 0],
        target_before[:, 1],
        target_before[:, 2],
        s=4,
        c=blue_depths,
        alpha=0.52,
        label="target"
    )

    ax_before.scatter(
        source_before[:, 0],
        source_before[:, 1],
        source_before[:, 2],
        s=4,
        c=dark_ruby,
        alpha=0.52,
        label="source"
    )

    prepare_axis(ax_before, "before icp")
    ax_before.legend()
    set_axes_equal(ax_before)

    ax_after = fig.add_subplot(122, projection="3d")

    ax_after.scatter(
        target_after[:, 0],
        target_after[:, 1],
        target_after[:, 2],
        s=4,
        c=blue_depths,
        alpha=0.52,
        label="target"
    )

    ax_after.scatter(
        source_after_vis[:, 0],
        source_after_vis[:, 1],
        source_after_vis[:, 2],
        s=4,
        c=dark_ruby,
        alpha=0.52,
        label="source after icp"
    )

    prepare_axis(ax_after, "after icp")
    ax_after.legend()
    set_axes_equal(ax_after)

    if info_text is not None:
        fig.text(
            0.5,
            0.045,
            info_text,
            ha="center",
            fontsize=11,
            color=meteorite,
            bbox=dict(
                facecolor=cultured_pearl,
                edgecolor=catacomb_walls,
                boxstyle="round,pad=0.6"
            )
        )

    plt.tight_layout(rect=[0, 0.07, 1, 0.89])
    plt.show()


def plot_icp_errors(errors):
    """
    plots the mean icp error in consecutive iterations

    parameters:
    errors: list of mean errors calculated during icp iterations

    returns:
    none
    """

    plt.figure(
        figsize=(10, 6),
        facecolor=cultured_pearl
    )

    maximize_matplotlib_window()

    plt.plot(
        errors,
        marker="o",
        linewidth=2,
        color=dark_ruby
    )

    plt.title(
        "icp error in consecutive iterations",
        color=dark_ruby,
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel("iteration")
    plt.ylabel("mean error")
    plt.grid(True, alpha=0.35)

    plt.tight_layout()
    plt.show()


def animate_icp_alignment(target, history, errors=None, interval=450):
    """
    animates icp alignment process step by step

    parameters:
    target: reference point cloud
    history: list of source point clouds saved after consecutive icp iterations
    errors: optional list of mean errors from consecutive iterations
    interval: delay between animation frames in milliseconds

    returns:
    none
    """

    fig = plt.figure(
        figsize=(16, 9),
        facecolor=cultured_pearl
    )

    maximize_matplotlib_window()

    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#fbfaf8")

    fig.suptitle(
        "iterative closest point animation",
        fontsize=28,
        fontweight="bold",
        color=dark_ruby
    )

    subtitle = fig.text(
        0.5,
        0.925,
        "source cloud is gradually aligned with the target cloud",
        ha="center",
        fontsize=13,
        color=meteorite
    )

    target_plot = ax.scatter(
        target[:, 0],
        target[:, 1],
        target[:, 2],
        s=4,
        c=blue_depths,
        alpha=0.45,
        label="target"
    )

    source_plot = ax.scatter(
        history[0][:, 0],
        history[0][:, 1],
        history[0][:, 2],
        s=4,
        c=dark_ruby,
        alpha=0.55,
        label="source"
    )

    ax.set_title(
        "iteration 0",
        fontsize=15,
        color=meteorite
    )

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.view_init(elev=20, azim=-60)
    ax.legend()

    all_points = np.vstack([target] + history)

    ax.set_xlim(np.min(all_points[:, 0]), np.max(all_points[:, 0]))
    ax.set_ylim(np.min(all_points[:, 1]), np.max(all_points[:, 1]))
    ax.set_zlim(np.min(all_points[:, 2]), np.max(all_points[:, 2]))
    set_axes_equal(ax)

    info_box = fig.text(
        0.5,
        0.045,
        "",
        ha="center",
        fontsize=12,
        color=meteorite,
        bbox=dict(
            facecolor=cultured_pearl,
            edgecolor=catacomb_walls,
            boxstyle="round,pad=0.6"
        )
    )

    def update(frame):
        current_source = history[frame]

        source_plot._offsets3d = (
            current_source[:, 0],
            current_source[:, 1],
            current_source[:, 2]
        )

        ax.set_title(
            f"iteration {frame}",
            fontsize=15,
            color=meteorite
        )

        if errors is not None and frame > 0 and frame - 1 < len(errors):
            info_box.set_text(
                f"iteration: {frame}     mean error: {errors[frame - 1]:.6f}"
            )
        else:
            info_box.set_text(
                f"iteration: {frame}"
            )

        return source_plot,

    animation = FuncAnimation(
        fig,
        update,
        frames=len(history),
        interval=interval,
        blit=False,
        repeat=True
    )

    plt.tight_layout(rect=[0, 0.07, 1, 0.89])
    plt.show()


def print_result_summary(method_name, transformation, rmse, elapsed_time, fitness=None):
    """
    prints a short summary of icp alignment results

    parameters:
    method_name: name of the used icp method
    transformation: final 4x4 transformation matrix estimated by icp
    rmse: root mean square error after alignment
    elapsed_time: execution time in seconds
    fitness: optional open3d fitness value describing the ratio of inlier correspondences

    returns:
    none
    """

    print("\n" + "=" * 60)
    print(method_name)
    print("=" * 60)

    print("\nestimated transformation")
    print(transformation)

    print("\nrmse", rmse)

    if fitness is not None:
        print("fitness", fitness)

    print("time", elapsed_time, "s")