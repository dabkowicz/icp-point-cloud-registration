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

from visualizations import plot_before_after_matplotlib
from visualizations import plot_icp_errors
from visualizations import print_result_summary


blue_depths = "#2c356a"
dark_ruby = "#720013"
meteorite = "#2c2929"
cultured_pearl = "#f5f4f2"
catacomb_walls = "#dcd7d4"
creme_white = "#c3b79d"


title_font = ("Georgia", 24, "bold")
subtitle_font = ("Segoe UI", 12)
label_font = ("Segoe UI", 11, "bold")
button_font = ("Segoe UI", 12, "bold")
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
        "visualization": "matplotlib",
        "shape": "rubber duck"
    }

    def start_project():
        selected_options["visualization"] = visualization_var.get()
        selected_options["shape"] = shape_var.get()
        window.destroy()

    window = tk.Tk()
    window.title("icp point cloud registration")

    window_width = 600
    window_height = 430

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
        545,
        385,
        radius=32,
        fill=cultured_pearl,
        outline=catacomb_walls,
        width=2
    )

    content = tk.Frame(
        window,
        bg=cultured_pearl
    )

    canvas.create_window(
        300,
        215,
        window=content,
        width=455,
        height=300
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

    title.pack(pady=(18, 3))
    subtitle.pack(pady=(0, 24))

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Custom.TCombobox",
        fieldbackground="#ebe7e2",
        background="#ebe7e2",
        foreground=meteorite,
        arrowcolor=dark_ruby,
        bordercolor=catacomb_walls,
        lightcolor=catacomb_walls,
        darkcolor=catacomb_walls,
        padding=8
    )

    style.map(
        "Custom.TCombobox",
        fieldbackground=[("readonly", "#ebe7e2")],
        selectbackground=[("readonly", "#ebe7e2")],
        selectforeground=[("readonly", meteorite)]
    )

    form = tk.Frame(
        content,
        bg=cultured_pearl
    )

    form.pack()

    visualization_var = tk.StringVar(value="matplotlib")
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
        padx=18
    )

    shape_block.grid(
        row=0,
        column=1,
        padx=18
    )

    visualization_label = tk.Label(
        visualization_block,
        text="visualization mode",
        font=label_font,
        bg=cultured_pearl,
        fg=blue_depths,
        anchor="center",
        justify="center"
    )

    visualization_label.pack(pady=(0, 7))

    visualization_box = ttk.Combobox(
        visualization_block,
        textvariable=visualization_var,
        values=["matplotlib", "open3d"],
        state="readonly",
        font=("Segoe UI", 10),
        width=21,
        justify="center",
        style="Custom.TCombobox"
    )

    visualization_box.pack()

    shape_label = tk.Label(
        shape_block,
        text="shape",
        font=label_font,
        bg=cultured_pearl,
        fg=dark_ruby,
        anchor="center",
        justify="center"
    )

    shape_label.pack(pady=(0, 7))

    shape_box = ttk.Combobox(
        shape_block,
        textvariable=shape_var,
        values=["cube", "sphere", "rubber duck"],
        state="readonly",
        font=("Segoe UI", 10),
        width=21,
        justify="center",
        style="Custom.TCombobox"
    )

    shape_box.pack()

    description = tk.Label(
        content,
        text="the program creates a transformed source cloud\nand aligns it with the target cloud using icp",
        font=small_font,
        bg=cultured_pearl,
        fg=meteorite,
        justify="center"
    )

    description.pack(pady=(24, 18))

    start_button = tk.Button(
        content,
        text="start visualization",
        font=button_font,
        width=26,
        height=2,
        bg=dark_ruby,
        fg=cultured_pearl,
        activebackground=meteorite,
        activeforeground=cultured_pearl,
        bd=0,
        cursor="hand2",
        command=start_project
    )

    start_button.pack()

    footer = tk.Label(
        content,
        text="source cloud vs target cloud alignment",
        font=small_font,
        bg=cultured_pearl,
        fg="#77706b"
    )

    footer.pack(pady=(15, 0))

    window.mainloop()

    return selected_options["visualization"], selected_options["shape"]

    def start_project():
        selected_options["visualization"] = visualization_var.get()
        selected_options["shape"] = shape_var.get()
        window.destroy()

    window = tk.Tk()
    window.title("icp point cloud registration")
    window_width = 560
    window_height = 420

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    window.resizable(False, False)
    window.configure(bg=blue_depths)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "TCombobox",
        fieldbackground=cultured_pearl,
        background=cultured_pearl,
        foreground=meteorite,
        arrowcolor=meteorite,
        padding=6
    )

    card = tk.Frame(
        window,
        bg=cultured_pearl,
        bd=0,
        relief="flat",
        highlightbackground=catacomb_walls,
        highlightthickness=2
    )

    card.place(
        relx=0.5,
        rely=0.5,
        anchor="center",
        width=455,
        height=335
    )

    title = tk.Label(
        card,
        text="icp point cloud registration",
        font=title_font,
        bg=cultured_pearl,
        fg=dark_ruby
    )

    subtitle = tk.Label(
        card,
        text="choose visualization mode and shape",
        font=subtitle_font,
        bg=cultured_pearl,
        fg=meteorite
    )

    title.pack(pady=(25, 4))
    subtitle.pack(pady=(0, 22))

    form = tk.Frame(
        card,
        bg=cultured_pearl
    )

    form.pack()

    visualization_var = tk.StringVar(value="matplotlib")
    shape_var = tk.StringVar(value="rubber duck")

    visualization_label = tk.Label(
        form,
        text="visualization mode",
        font=label_font,
        bg=cultured_pearl,
        fg=blue_depths
    )

    visualization_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=12,
        pady=(0, 5)
    )

    visualization_box = ttk.Combobox(
        form,
        textvariable=visualization_var,
        values=["matplotlib", "open3d"],
        state="readonly",
        font=("Segoe UI", 10),
        width=22
    )

    visualization_box.grid(
        row=1,
        column=0,
        sticky="w",
        padx=12,
        pady=(0, 15)
    )

    shape_label = tk.Label(
        form,
        text="shape",
        font=label_font,
        bg=cultured_pearl,
        fg=dark_ruby
    )

    shape_label.grid(
        row=0,
        column=1,
        sticky="w",
        padx=12,
        pady=(0, 5)
    )

    shape_box = ttk.Combobox(
        form,
        textvariable=shape_var,
        values=["cube", "sphere", "rubber duck"],
        state="readonly",
        font=("Segoe UI", 10),
        width=22
    )

    shape_box.grid(
        row=1,
        column=1,
        sticky="w",
        padx=12,
        pady=(0, 15)
    )

    description = tk.Label(
        card,
        text="the program creates a transformed source cloud\nand aligns it with the target cloud using icp",
        font=small_font,
        bg=cultured_pearl,
        fg=meteorite,
        justify="center"
    )

    description.pack(pady=(2, 16))

    start_button = tk.Button(
        card,
        text="start visualization",
        font=button_font,
        width=26,
        height=2,
        bg=dark_ruby,
        fg=cultured_pearl,
        activebackground=meteorite,
        activeforeground=cultured_pearl,
        bd=0,
        cursor="hand2",
        command=start_project
    )

    start_button.pack(pady=(0, 12))

    footer = tk.Label(
        card,
        text="source cloud vs target cloud alignment",
        font=small_font,
        bg=cultured_pearl,
        fg="#77706b"
    )

    footer.pack()

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

    if visualization_mode == "matplotlib":
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
            method_name="numpy icp",
            transformation=numpy_transformation,
            rmse=numpy_rmse,
            elapsed_time=numpy_time
        )

        plot_before_after_matplotlib(
            source_before=source,
            target_before=target,
            source_after=aligned_source,
            target_after=target,
            info_text=f"shape: {shape_name}     rmse: {numpy_rmse:.6f}     time: {numpy_time:.4f} s     iterations: {len(errors)}"
        )

        plot_icp_errors(errors)

    if visualization_mode == "open3d":
        aligned_source, open3d_transformation, fitness, rmse, open3d_time = run_open3d_icp(
            source,
            target,
            max_distance=1.0,
            max_iteration=80,
            tolerance=1e-6
        )

        print_result_summary(
            method_name="open3d icp",
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