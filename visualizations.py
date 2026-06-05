import matplotlib.pyplot as plt


def plot_3d_clouds(source, target, title ="POINT CLOUDS"):
    fig = plt.figure(figsize=(8,7))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter( target[:, 0], target[:, 1], target[:, 2], s=8, label="target")
    ax.scatter( source[:, 0], source[:, 1], source[:, 2], s=8, label="source")

    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.legend()

    plt.tight_layout()
    plt.show()

"""
^^^
visualisation of two 3d point clouds with matplottlib

source cloud is shown as the transformed cloud
target cloud is shown as the reference cloud
"""


def plot_icp_errors(errors, title ="ICP ERRORS"):
    plt.figure(figsize=(8,7))
    plt.plot(errors, marker = "o")

    plt.title(title)
    plt.xlabel("iteration")
    plt.ylabel("mean error")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

#plots the mean error in consecutive iterations


def print_result_summary(method_name, transformation, rmse, elapsed_time, fitness=None):
    print("\n" + "=" * 60)
    print(method_name)
    print("=" * 60)
    print("\nestimated transformation:")
    print(transformation)

    print("\nRMSE:", rmse)

    if fitness is not None:
        print("fitness:", fitness)

    print("time:", elapsed_time, "s")