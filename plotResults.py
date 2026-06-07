import pandas as pd
import matplotlib.pyplot as plt
import os


def generate_plots():
    csv_path = 'results/experiment_results.csv'

    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} not found.")
        return

    # Load data
    df = pd.read_csv(csv_path)

    # Create directory for plots
    plots_dir = 'results/plots'
    os.makedirs(plots_dir, exist_ok=True)

    print("Starting plot generation...")

    # PLOT 1 RMSE vs Noise (for cube, 1000 points)
    df_rmse_cube = df[(df['shape'] == 'cube') & (df['points'] == 1000)]
    plt.figure(figsize=(10, 6))
    for method in df_rmse_cube['method'].unique():
        method_data = df_rmse_cube[df_rmse_cube['method'] == method].sort_values(by='noise')
        plt.plot(method_data['noise'], method_data['rmse'], marker='o', linewidth=2.5, markersize=8, label=method)
    plt.title('Impact of Noise on Algorithm Accuracy (RMSE)\n[Shape: Cube, 1000 points]', fontsize=14, pad=15)
    plt.xlabel('Noise Level', fontsize=12)
    plt.ylabel('RMSE Error', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(plots_dir, '1_rmse_vs_noise_cube.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 2 Time vs Points (for sphere, 0.0 noise)
    df_time = df[(df['shape'] == 'sphere') & (df['noise'] == 0.0)]
    plt.figure(figsize=(10, 6))
    for method in df_time['method'].unique():
        method_data = df_time[df_time['method'] == method].sort_values(by='points')
        plt.plot(method_data['points'], method_data['time'], marker='s', linewidth=2.5, markersize=8, label=method)
    plt.title('Algorithm Execution Time vs Number of Points\n[Shape: Sphere, No noise]', fontsize=14, pad=15)
    plt.xlabel('Number of points in cloud', fontsize=12)
    plt.ylabel('Execution Time [s] (lower is better)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(plots_dir, '2_time_vs_points_sphere.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 3 RMSE vs Noise (Complex Shape - Rubber Duck)
    df_rmse_duck = df[(df['shape'] == 'rubber duck') & (df['points'] == 3000)]
    plt.figure(figsize=(10, 6))
    for method in df_rmse_duck['method'].unique():
        method_data = df_rmse_duck[df_rmse_duck['method'] == method].sort_values(by='noise')
        plt.plot(method_data['noise'], method_data['rmse'], marker='^', linewidth=2.5, markersize=8, label=method)
    plt.title('Impact of Noise on Complex Geometry Alignment (RMSE)\n[Shape: Rubber Duck, 3000 points]', fontsize=14,
              pad=15)
    plt.xlabel('Noise Level (Standard Deviation)', fontsize=12)
    plt.ylabel('RMSE Error (lower is better)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(plots_dir, '3_rmse_vs_noise_duck.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # PLOT 4: Bar Chart - Time per Shape (Fixed points & noise)
    df_shapes = df[(df['points'] == 2000) & (df['noise'] == 0.01)]

    pivot_df = df_shapes.pivot(index='shape', columns='method', values='time')

    ax = pivot_df.plot(kind='bar', figsize=(10, 6), colormap='Set1', width=0.7)
    plt.title('Execution Time Comparison Across Different Shapes\n[2000 points, 0.01 noise]', fontsize=14, pad=15)
    plt.xlabel('Shape', fontsize=12)
    plt.ylabel('Execution Time [s]', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='Method', fontsize=11)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(plots_dir, '4_time_comparison_shapes.png'), dpi=300, bbox_inches='tight')
    plt.close()

    print("Success! 4 Plots are ready in the 'results/plots/' folder.\n")

    # SUMMARY TABLE
    print("=" * 60)
    print("                 SUMMARY DATA TABLE")
    print("          (Copy this to Excel or PowerPoint)")
    print("=" * 60)

    # Calculate average time and error across all tests for each method
    summary_table = df.groupby('method').agg(
        Average_Time_sec=('time', 'mean'),
        Average_RMSE=('rmse', 'mean')
    ).reset_index()

    print(summary_table.to_string(index=False))
    print("=" * 60)
    print("CONCLUSION:")
    print("-> Both methods achieve nearly identical precision (RMSE).")
    print("-> Open3D is significantly faster on average.")


if __name__ == "__main__":
    generate_plots()