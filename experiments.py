import os
import csv
import time
import numpy as np

from shapes import generateCubePoints, generateSpherePoints, generateRubberDuckPoints, generate3DGlassesPoints
from transformations import transform_points
from icpNumpy import run_numpy_icp, calculate_rmse
from icpOpen3d import run_open3d_icp


def generate_shape_for_experiment(shape_name, n_points):
    """Helper function to generate point clouds without initial noise (noise will be added during transformation)"""
    if shape_name == "cube":
        return generateCubePoints(n_points=n_points, size=1.0, noise=0.0)
    elif shape_name == "sphere":
        return generateSpherePoints(n_points=n_points, radius=1.0, noise=0.0)
    elif shape_name == "rubber duck":
        return generateRubberDuckPoints(n_points=n_points, noise=0.0)
    elif shape_name == "3d glasses":
        return generate3DGlassesPoints(n_points=n_points, noise=0.0)
    else:
        raise ValueError("Unknown shape")


def run_all_experiments():
    shapes_list = ['cube', 'sphere', 'rubber duck', '3d glasses']
    points_sizes = [1000, 2000, 3000]
    noise_levels = [0.00, 0.01, 0.03, 0.05]

    os.makedirs('results', exist_ok=True)
    csv_filename = 'results/experiment_results.csv'
    headers = ['shape', 'points', 'noise', 'method', 'rmse', 'fitness', 'time']

    print(f"=== STARTING AUTOMATED TESTS ===")

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)

        test_id = 0

        for shape_name in shapes_list:
            for num_points in points_sizes:
                for noise in noise_levels:
                    test_id += 1
                    print(f"[{test_id}/48] Testing: {shape_name} | Points: {num_points} | Noise: {noise}")

                    target_cloud = generate_shape_for_experiment(shape_name, num_points)

                    source_cloud, _ = transform_points(
                        target_cloud,
                        angle_x=10, angle_y=20, angle_z=35,
                        translation=(1.0, 0.5, 0.3),
                        noise=noise
                    )

                    start_time = time.time()
                    aligned_source_np, _, _, _ = run_numpy_icp(
                        source_cloud, target_cloud, max_iterations=50, tolerance=1e-6, save_history=False
                    )
                    numpy_time = time.time() - start_time
                    numpy_rmse = calculate_rmse(aligned_source_np, target_cloud)

                    writer.writerow([shape_name, num_points, noise, 'Custom_NumPy', f"{numpy_rmse:.6f}", "N/A",
                                     f"{numpy_time:.4f}"])

                    start_time = time.time()
                    aligned_source_o3d, _, fitness_o3d, rmse_o3d, _ = run_open3d_icp(
                        source_cloud, target_cloud, max_distance=1.0, max_iteration=80, tolerance=1e-6
                    )
                    open3d_time = time.time() - start_time

                    writer.writerow([shape_name, num_points, noise, 'Open3D', f"{rmse_o3d:.6f}", f"{fitness_o3d:.4f}",
                                     f"{open3d_time:.4f}"])

                    csv_file.flush()

    print(f"\n=== SUCCESS! Results saved to: '{csv_filename}' ===")


if __name__ == "__main__":
    run_all_experiments()