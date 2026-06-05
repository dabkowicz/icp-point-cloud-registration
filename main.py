import tkinter as tk

from shapes import generateRubberDuckPoints
from transformations import transform_points

from icpNumpy import run_numpy_icp
from icpNumpy import calculate_rmse

from icpOpen3d import run_open3d_icp
from icpOpen3d import visualize_before_after_open3d

from visualizations import plot_before_after_matplotlib
from visualizations import plot_icp_errors
from visualizations import print_result_summary



#opens a small styled window where the user chooses visualization mode
def choose_visualization_window():

    selected_mode = {"value": None}

    def choose_matplotlib():
        selected_mode["value"] = "matplotlib"
        window.destroy()

    def choose_open3d():
        selected_mode["value"] = "open3d"
        window.destroy()

    window = tk.Tk()
    window.title("icp visualization mode")
    window.geometry("520x360")
    window.resizable(False, False)
    window.configure(bg="#101827")

    card = tk.Frame(
        window,
        bg="#f5f7fb",
        bd=0,
        relief="flat"
    )

    title = tk.Label(
        card,
        text="ICP point cloud registration",
        font=("segoe ui", 22, "bold"),
        bg="#f5f7fb",
        fg="#101827"
    )

    subtitle = tk.Label(
        card,
        text="choose visualization mode",
        font=("segoe ui", 13),
        bg="#f5f7fb",
        fg="#3b4658"
    )

    description = tk.Label(
        card,
        text="Matplotlib shows two separate plots in one window\nOpen3D shows a cleaner interactive 3D preview",
        font=("segoe ui", 10),
        bg="#f5f7fb",
        fg="#5d6675",
        justify="center"
    )

    matplotlib_button = tk.Button(
        card,
        text="Matplotlib view",
        font=("segoe ui", 12, "bold"),
        width=24,
        height=2,
        bg="#1f3a93",
        fg="white",
        activebackground="#172c70",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=choose_matplotlib
    )

    open3d_button = tk.Button(
        card,
        text="Open3D view",
        font=("segoe ui", 12, "bold"),
        width=24,
        height=2,
        bg="#8b1e3f",
        fg="white",
        activebackground="#6f1832",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=choose_open3d
    )

    footer = tk.Label(
        card,
        text="SOURCE cloud vs TARGET cloud alignment",
        font=("segoe ui", 9),
        bg="#f5f7fb",
        fg="#8a94a6"
    )

    card.place(relx=0.5, rely=0.5, anchor="center", width=430, height=285)

    title.pack(pady=(25, 4))
    subtitle.pack(pady=(0, 10))
    description.pack(pady=(0, 18))

    matplotlib_button.pack(pady=6)
    open3d_button.pack(pady=6)

    footer.pack(pady=(14, 0))

    window.mainloop()

    if selected_mode["value"] is None:
        return "Matplotlib"

    return selected_mode["value"]






def main():
    visualization_mode = choose_visualization_window()

    target = generateRubberDuckPoints(
        n_points=4000,
        noise=0.0
    )

    source, true_transformation = transform_points(
        target,
        angle_x=10,
        angle_y=20,
        angle_z=35,
        translation=(1.0, 0.5, 0.3),
        noise=0.01
    )

    print("\ntrue transformation used to create source cloud")
    print(true_transformation)

    if visualization_mode == "Matplotlib":
        aligned_source, numpy_transformation, errors, numpy_time = run_numpy_icp(
            source,
            target,
            max_iterations=50,
            tolerance=1e-6
        )

        numpy_rmse = calculate_rmse(
            aligned_source,
            target
        )

        print_result_summary(
            method_name="Numpy ICP",
            transformation=numpy_transformation,
            rmse=numpy_rmse,
            elapsed_time=numpy_time
        )

        plot_before_after_matplotlib(
            source_before=source,
            target_before=target,
            source_after=aligned_source,
            target_after=target
        )

        plot_icp_errors(errors)

    if visualization_mode == "Open3D":
        aligned_source, open3d_transformation, fitness, rmse, open3d_time = run_open3d_icp(
            source,
            target,
            max_distance=1.0,
            max_iteration=80,
            tolerance=1e-6
        )

        print_result_summary(
            method_name="Open3D ICP",
            transformation=open3d_transformation,
            rmse=rmse,
            elapsed_time=open3d_time,
            fitness=fitness
        )

        visualize_before_after_open3d(
            source_before=source,
            target_before=target,
            source_after=aligned_source,
            target_after=target
        )


if __name__ == "__main__":
    main()