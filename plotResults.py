import pandas as pd
import matplotlib.pyplot as plt
import os


def generate_plots():
    csv_path = 'results/experiment_results.csv'

    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} not found.")
        return

    df = pd.read_csv(csv_path)

    plots_dir = 'results/plots'
    os.makedirs(plots_dir, exist_ok=True)

    print("Starting plot generation...")

    #RMSE vs Noise (for cube, 1000 points)
    df_rmse = df[(df['shape'] == 'cube') & (df['points'] == 1000)]

    plt.figure(figsize=(10, 6))
    for method in df_rmse['method'].unique():
        method_data = df_rmse[df_rmse['method'] == method].sort_values(by='noise')
        plt.plot(method_data['noise'], method_data['rmse'], marker='o', linewidth=2.5, markersize=8, label=method)

    plt.title('Impact of Noise on Algorithm Accuracy (RMSE)\n[Shape: Cube, 1000 points]', fontsize=14, pad=15)
    plt.xlabel('Noise Level (Standard Deviation)', fontsize=12)
    plt.ylabel('RMSE Error (lower is better)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    plot1_path = os.path.join(plots_dir, '1_rmse_vs_noise.png')
    plt.savefig(plot1_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {plot1_path}")

    #Time vs Number of Points (for cloud without noise)
    df_time = df[(df['shape'] == 'cube') & (df['noise'] == 0.0)]

    plt.figure(figsize=(10, 6))
    for method in df_time['method'].unique():
        method_data = df_time[df_time['method'] == method].sort_values(by='points')
        plt.plot(method_data['points'], method_data['time'], marker='s', linewidth=2.5, markersize=8, label=method)

    plt.title('Algorithm Execution Time vs Number of Points\n[Shape: Cube, No noise]', fontsize=14,
              pad=15)
    plt.xlabel('Number of points in cloud', fontsize=12)
    plt.ylabel('Execution Time [s] (lower is better)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    plot2_path = os.path.join(plots_dir, '2_time_vs_points.png')
    plt.savefig(plot2_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {plot2_path}")

    print("\nSuccess! Plots are ready!")


if __name__ == "__main__":
    generate_plots()