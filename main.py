import tkinter as tk
from tkinter import ttk

from shapes import generateCubePoints
from shapes import generateSpherePoints
from shapes import generateRubberDuckPoints
from shapes import generate3DGlassesPoints

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

#all of the colors that are used
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

    canvas.create_rectangle(
        465,
        76,
        500,
        94,
        outline=blue_depths,
        width=3
    )

    canvas.create_rectangle(
        512,
        76,
        547,
        94,
        outline=dark_ruby,
        width=3
    )

    canvas.create_line(
        500,
        85,
        512,
        85,
        fill=meteorite,
        width=3
    )

    canvas.create_line(
        465,
        85,
        442,
        76,
        fill=meteorite,
        width=3
    )

    canvas.create_line(
        547,
        85,
        570,
        76,
        fill=meteorite,
        width=3
    )


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




def draw_glasses_panel(canvas, x, y):
    """
    draws a cleaner front part of paper 3d glasses

    parameters:
    canvas: tkinter canvas
    x: left position
    y: top position

    returns:
    none
    """

    frame_fill = "#f7f6f4"
    frame_shadow = "#d6d0ca"
    frame_outline = "#c8c1ba"

    left_lens_fill = "#d8edf4"
    right_lens_fill = "#efd9dd"

    left_lens_outline = blue_depths
    right_lens_outline = dark_ruby

    # shadow behind glasses
    create_rounded_rectangle(
        canvas,
        x + 14,
        y + 18,
        x + 626,
        y + 150,
        radius=6,
        fill=frame_shadow,
        outline=frame_shadow
    )

    # main white front
    create_rounded_rectangle(
        canvas,
        x + 8,
        y + 12,
        x + 620,
        y + 144,
        radius=6,
        fill=frame_fill,
        outline=frame_outline,
        width=2
    )

    # nose cutout
    canvas.create_oval(
        x + 282,
        y + 96,
        x + 346,
        y + 162,
        fill=cultured_pearl,
        outline=cultured_pearl
    )

    # hide upper part of oval so only the bottom cut stays visible
    canvas.create_rectangle(
        x + 278,
        y + 12,
        x + 350,
        y + 114,
        fill=frame_fill,
        outline=frame_fill
    )

    # redraw top border after covering oval
    canvas.create_line(
        x + 8,
        y + 12,
        x + 278,
        y + 12,
        fill=frame_outline,
        width=2
    )

    canvas.create_line(
        x + 350,
        y + 12,
        x + 620,
        y + 12,
        fill=frame_outline,
        width=2
    )

    # redraw bottom border left and right of the nose cut
    canvas.create_line(
        x + 8,
        y + 144,
        x + 282,
        y + 144,
        fill=frame_outline,
        width=2
    )

    canvas.create_line(
        x + 346,
        y + 144,
        x + 620,
        y + 144,
        fill=frame_outline,
        width=2
    )

    # nose arc outline
    canvas.create_arc(
        x + 282,
        y + 96,
        x + 346,
        y + 160,
        start=0,
        extent=180,
        style="arc",
        outline=frame_outline,
        width=2
    )

    # left lens
    create_rounded_rectangle(
        canvas,
        x + 72,
        y + 38,
        x + 286,
        y + 116,
        radius=10,
        fill=left_lens_fill,
        outline=left_lens_outline,
        width=2
    )

    # right lens
    create_rounded_rectangle(
        canvas,
        x + 344,
        y + 38,
        x + 558,
        y + 116,
        radius=10,
        fill=right_lens_fill,
        outline=right_lens_outline,
        width=2
    )

    # subtle shine on left lens
    canvas.create_polygon(
        x + 208, y + 40,
        x + 286, y + 40,
        x + 286, y + 68,
        x + 246, y + 116,
        x + 208, y + 116,
        fill="#e8f4f8",
        outline="#e8f4f8"
    )

    # subtle shine on right lens
    canvas.create_polygon(
        x + 480, y + 40,
        x + 558, y + 40,
        x + 558, y + 68,
        x + 518, y + 116,
        x + 480, y + 116,
        fill="#f3e6e9",
        outline="#f3e6e9"
    )

    # labels
    canvas.create_text(
        x + 179,
        y + 54,
        text="visualization mode",
        font=("Segoe UI", 12, "bold"),
        fill=blue_depths
    )

    canvas.create_text(
        x + 451,
        y + 54,
        text="shape",
        font=("Segoe UI", 12, "bold"),
        fill=blue_depths
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

    window_width = 920
    window_height = 660

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    window.resizable(False, False)
    window.configure(bg=blue_depths)

    root_canvas = tk.Canvas(
        window,
        width=window_width,
        height=window_height,
        bg=blue_depths,
        highlightthickness=0
    )

    root_canvas.pack(fill="both", expand=True)

    create_rounded_rectangle(
        root_canvas,
        50,
        40,
        870,
        605,
        radius=34,
        fill=cultured_pearl,
        outline=catacomb_walls,
        width=2
    )

    content = tk.Frame(
        window,
        bg=cultured_pearl
    )

    root_canvas.create_window(
        460,
        323,
        window=content,
        width=760,
        height=520
    )

    title = tk.Label(
        content,
        text="ICP point cloud registration",
        font=("Georgia", 30, "bold"),
        bg=cultured_pearl,
        fg=dark_ruby
    )

    title.pack(pady=(18, 5))

    subtitle = tk.Label(
        content,
        text="choose visualization mode and shape",
        font=("Segoe UI", 13),
        bg=cultured_pearl,
        fg=meteorite
    )

    subtitle.pack(pady=(0, 18))

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Custom.TCombobox",
        fieldbackground="#f3efeb",
        background="#f3efeb",
        foreground=meteorite,
        arrowcolor=dark_ruby,
        bordercolor="#d8d1cb",
        lightcolor="#d8d1cb",
        darkcolor="#d8d1cb",
        padding=6
    )

    style.map(
        "Custom.TCombobox",
        fieldbackground=[("readonly", "#f3efeb")],
        selectbackground=[("readonly", "#f3efeb")],
        selectforeground=[("readonly", meteorite)]
    )

    glasses_canvas = tk.Canvas(
        content,
        width=660,
        height=190,
        bg=cultured_pearl,
        highlightthickness=0
    )

    glasses_canvas.pack(pady=(8, 8))

    draw_glasses_panel(glasses_canvas, 14, 18)

    visualization_var = tk.StringVar(value="Animation for Matplotlib")
    shape_var = tk.StringVar(value="rubber duck")

    visualization_box = ttk.Combobox(
        glasses_canvas,
        textvariable=visualization_var,
        values=[
            "Matplotlib before after",
            "Open3D before after",
            "Animation for Matplotlib",
            "Animation for Open3D"
        ],
        state="readonly",
        font=("Segoe UI", 11),
        width=22,
        justify="center",
        style="Custom.TCombobox"
    )

    shape_box = ttk.Combobox(
        glasses_canvas,
        textvariable=shape_var,
        values=["cube", "sphere", "rubber duck", "3d glasses"],
        state="readonly",
        font=("Segoe UI", 11),
        width=22,
        justify="center",
        style="Custom.TCombobox"
    )

    glasses_canvas.create_window(
        197,
        95,
        window=visualization_box,
        width=185,
        height=32
    )

    glasses_canvas.create_window(
        471,
        95,
        window=shape_box,
        width=185,
        height=32
    )

    button_canvas = tk.Canvas(
        content,
        width=310,
        height=70,
        bg=cultured_pearl,
        highlightthickness=0
    )

    button_canvas.pack(pady=(12, 10))

    create_rounded_rectangle(
        button_canvas,
        6,
        7,
        304,
        63,
        radius=22,
        fill=dark_ruby,
        outline=dark_ruby
    )

    button_canvas.create_text(
        155,
        35,
        text="start visualization",
        font=("Segoe UI", 15, "bold"),
        fill=cultured_pearl
    )

    button_canvas.bind("<Button-1>", lambda event: start_project())
    button_canvas.bind("<Enter>", lambda event: button_canvas.config(cursor="hand2"))

    description = tk.Label(
        content,
        text="the program creates a transformed source cloud\nand aligns it with the target cloud using icp",
        font=("Segoe UI", 10),
        bg=cultured_pearl,
        fg="#a39a93",
        justify="center"
    )

    description.pack(pady=(8, 6))

    footer = tk.Label(
        content,
        text="point cloud registration and visual comparison",
        font=("Segoe UI", 10),
        bg=cultured_pearl,
        fg="#b8afa8"
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
    if shape_name == "3d glasses":
        return generate3DGlassesPoints(
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