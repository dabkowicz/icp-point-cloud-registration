import tkinter as tk
from tkinter import ttk

from shapes import generateCubePoints
from shapes import generateSpherePoints
from shapes import generateRubberDuckPoints

from transformations import transform_points

from icpNumpy import run_numpy_icp
from icpNumpy import calculate_rmse

from icpOpen3d import run_open3d_icp
from icpOpen3d import visualize_before_after_open3d
from icpOpen3d import animate_icp_open3d

from visualizations import plot_before_after_matplotlib
from visualizations import plot_icp_errors
from visualizations import animate_icp_alignment
from visualizations import print_result_summary


blue_depths = "#2c356a"
dark_ruby = "#720013"
meteorite = "#2c2929"
cultured_pearl = "#f5f4f2"
catacomb_walls = "#dcd7d4"
input_background = "#e7e1dc"
soft_text = "#8f8882"


title_font = ("Georgia", 24, "bold")
subtitle_font = ("Segoe UI", 12)
label_font = ("Segoe UI", 11, "bold")
button_font = ("Segoe UI", 13, "bold")
small_font = ("Segoe UI", 9)


def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """
    creates a rounded rectangle on tkinter canvas

    parameters:
    canvas: tkinter canvas object
    x1: left coordinate
    y1: top coordinate
    x2: right coordinate
    y2: bottom coordinate
    radius: corner radius

    returns:
    rounded rectangle object id
    """

    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]

    return canvas.create_polygon(
        points,
        smooth=True,
        **kwargs
    )


def choose_project_options():
    """
    opens a styled window where the user chooses visualization mode and shape

    parameters:
    none

    returns:
    visualization_mode: selected visualization mode
    shape_name: selected shape name
    """

    selected_options = {
        "visualization": "Animation for Matplotlib",
        "shape": "rubber duck"
    }

    def start_project():
        selected_options["visualization"] = visualization_var.get()
        selected_options["shape"] = shape_var.get()
        window.destroy()

    window = tk.Tk()
    window.title("ICP point cloud registration")

    window_width = 660
    window_height = 500

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    window.resizable(False, False)
    window.configure(bg=blue_depths)

    canvas = tk.Canvas(
        window,
        width=window_width,
        height=window_height,
        bg=blue_depths,
        highlightthickness=0
    )

    canvas.pack(fill="both", expand=True)

    create_rounded_rectangle(
        canvas,
        55,
        45,
        605,
        455,
        radius=34,
        fill=cultured_pearl,
        outline=catacomb_walls,
        width=2
    )

    content = tk.Frame(
        window,
        bg=cultured_pearl
    )

    canvas.create_window(
        330,
        250,
        window=content,
        width=500,
        height=360
    )

    title = tk.Label(
        content,
        text="icp point cloud registration",
        font=title_font,
        bg=cultured_pearl,
        fg=dark_ruby
    )

    subtitle = tk.Label(
        content,
        text="choose visualization mode and shape",
        font=subtitle_font,
        bg=cultured_pearl,
        fg=meteorite
    )

    title.pack(pady=(18, 4))
    subtitle.pack(pady=(0, 26))

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Custom.TCombobox",
        fieldbackground=input_background,
        background=input_background,
        foreground=meteorite,
        arrowcolor=dark_ruby,
        bordercolor=catacomb_walls,
        lightcolor=catacomb_walls,
        darkcolor=catacomb_walls,
        padding=8
    )

    style.map(
        "Custom.TCombobox",
        fieldbackground=[("readonly", input_background)],
        selectbackground=[("readonly", input_background)],
        selectforeground=[("readonly", meteorite)]
    )

    form = tk.Frame(
        content,
        bg=cultured_pearl
    )

    form.pack()

    visualization_var = tk.StringVar(value="Animation for Matplotlib")
    shape_var = tk.StringVar(value="rubber duck")

    visualization_block = tk.Frame(
        form,
        bg=cultured_pearl
    )

    shape_block = tk.Frame(
        form,
        bg=cultured_pearl
    )

    visualization_block.grid(
        row=0,
        column=0,
        padx=22
    )

    shape_block.grid(
        row=0,
        column=1,
        padx=22
    )

    label_color = blue_depths

    visualization_label = tk.Label(
        visualization_block,
        text="visualization mode",
        font=label_font,
        bg=cultured_pearl,
        fg=label_color,
        anchor="center",
        justify="center"
    )

    visualization_label.pack(pady=(0, 8))

    visualization_box = ttk.Combobox(
        visualization_block,
        textvariable=visualization_var,
        values=[
            "Matplotlib before after",
            "Open3D before after",
            "Animation for Matplotlib",
            "Animation for Open3D"
        ],
        state="readonly",
        font=("Segoe UI", 10),
        width=26,
        justify="center",
        style="Custom.TCombobox"
    )

    visualization_box.pack(ipady=6)

    shape_label = tk.Label(
        shape_block,
        text="shape",
        font=label_font,
        bg=cultured_pearl,
        fg=label_color,
        anchor="center",
        justify="center"
    )

    shape_label.pack(pady=(0, 8))

    shape_box = ttk.Combobox(
        shape_block,
        textvariable=shape_var,
        values=["cube", "sphere", "rubber duck"],
        state="readonly",
        font=("Segoe UI", 10),
        width=26,
        justify="center",
        style="Custom.TCombobox"
    )

    shape_box.pack(ipady=6)

    button_canvas = tk.Canvas(
        content,
        width=295,
        height=64,
        bg=cultured_pearl,
        highlightthickness=0
    )

    button_canvas.pack(pady=(32, 0))

    create_rounded_rectangle(
        button_canvas,
        5,
        5,
        290,
        59,
        radius=22,
        fill=dark_ruby,
        outline=dark_ruby
    )

    button_canvas.create_text(
        147,
        32,
        text="start visualization",
        font=button_font,
        fill=cultured_pearl
    )

    button_canvas.bind("<Button-1>", lambda event: start_project())
    button_canvas.bind("<Enter>", lambda event: button_canvas.config(cursor="hand2"))

    description = tk.Label(
        content,
        text="the program creates a transformed source cloud\nand aligns it with the target cloud using icp",
        font=small_font,
        bg=cultured_pearl,
        fg=soft_text,
        justify="center"
    )

    description.pack(pady=(16, 0))

    footer = tk.Label(
        content,
        text="source cloud vs target cloud alignment",
        font=small_font,
        bg=cultured_pearl,
        fg="#aaa39d"
    )

    footer.pack(pady=(10, 0))

    window.mainloop()

    return selected_options["visualization"], selected_options["shape"]


def generate_selected_shape(shape_name):
    """
    generates selected point cloud shape

    parameters:
    shape_name: selected shape name

    returns:
    target: generated target point cloud
    """

    if shape_name == "cube":
        return generateCubePoints(
            n_points=1800,
            size=1.0,
            noise=0.0
        )

    if shape_name == "sphere":
        return generateSpherePoints(
            n_points=1800,
            radius=1.0,
            noise=0.0
        )

    if shape_name == "rubber duck":
        return generateRubberDuckPoints(
            n_points=3500,
            noise=0.0
        )

    raise ValueError("unknown shape selected")


def main():
    visualization_mode, shape_name = choose_project_options()

    target = generate_selected_shape(shape_name)

    source, true_transformation = transform_points(
        target,
        angle_x=10,
        angle_y=20,
        angle_z=35,
        translation=(1.0, 0.5, 0.3),
        noise=0.01
    )

    print("\nselected shape")
    print(shape_name)

    print("\nvisualization mode")
    print(visualization_mode)

    print("\ntrue transformation used to create source cloud")
    print(true_transformation)

    if visualization_mode == "Open3D before after":
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

    if visualization_mode in [
        "Matplotlib before after",
        "Animation for Matplotlib",
        "Animation for Open3D"
    ]:
        aligned_source, numpy_transformation, errors, numpy_time, history = run_numpy_icp(
            source,
            target,
            max_iterations=50,
            tolerance=1e-6,
            save_history=True
        )

        numpy_rmse = calculate_rmse(
            aligned_source,
            target
        )

        print_result_summary(
            method_name="NumPy ICP",
            transformation=numpy_transformation,
            rmse=numpy_rmse,
            elapsed_time=numpy_time
        )

        if visualization_mode == "Matplotlib before after":
            plot_before_after_matplotlib(
                source_before=source,
                target_before=target,
                source_after=aligned_source,
                target_after=target,
                info_text=f"shape: {shape_name}     rmse: {numpy_rmse:.6f}     time: {numpy_time:.4f} s     iterations: {len(errors)}"
            )

            plot_icp_errors(errors)

        if visualization_mode == "Animation for Matplotlib":
            animate_icp_alignment(
                target=target,
                history=history,
                errors=errors,
                interval=450
            )

        if visualization_mode == "Animation for Open3D":
            animate_icp_open3d(
                target=target,
                history=history,
                interval=0.08
            )


if __name__ == "__main__":
    main()