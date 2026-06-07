# ICP Point Cloud Registration

## Contributors

This project was created by:

- [@karolinaa05](https://github.com/karolinaa05)
- [@karolinaflorek10](https://github.com/karolinaflorek10)
- [@dabkowicz](https://github.com/dabkowicz)

# ICP Point Cloud Registration

## Project description

This project presents a custom implementation of the Iterative Closest Point (ICP) algorithm for 3D point cloud registration.

The main goal of the project is to show how two 3D point clouds can be aligned by estimating the rigid transformation between them. The algorithm works iteratively by finding corresponding points, calculating the best rotation and translation, and applying the transformation until convergence.

The project also includes a comparison with the ready-to-use ICP implementation from the Open3D library. In addition, the application provides visualizations, error analysis, and animations showing how the source cloud gradually aligns with the target cloud.

## Main features

- Generating custom 3D point clouds
- Available shapes:
  - cube
  - sphere
  - rubber duck
  - 3D glasses
- Applying rotation and translation to a point cloud
- Finding nearest neighbours using KDTree
- Estimating transformation using SVD
- Custom NumPy-based ICP implementation
- Comparison with Open3D ICP
- RMSE calculation
- Error analysis in each iteration
- Visualization before and after registration
- ICP animation showing step-by-step alignment
- Simple graphical interface for choosing visualization mode and shape

## Technologies

- Python
- NumPy
- SciPy
- Matplotlib
- Open3D
- Tkinter

## Algorithm steps

1. Generate a selected 3D point cloud.
2. Create a transformed source point cloud using rotation and translation.
3. Find nearest neighbours between the transformed source and the target cloud.
4. Estimate the best rotation and translation using SVD.
5. Apply the estimated transformation to the source cloud.
6. Calculate the mean error and RMSE.
7. Repeat the process until convergence.
8. Visualize and compare the result.

## Visualization modes

The project provides several visualization modes:

- Matplotlib before and after comparison
- Open3D before and after comparison
- Matplotlib ICP animation
- Open3D ICP animation

The animation mode shows how the source point cloud changes its position in each ICP iteration until it aligns with the target cloud.

## Project structure

```text
.
├── main.py
├── shapes.py
├── transformations.py
├── icpNumpy.py
├── icpOpen3d.py
├── visualizations.py
├── experiments.py
├── results/
└── README.md
```

## Custom ICP implementation

The custom ICP implementation is based on the following operations:

- nearest neighbour search using KDTree
- centroid calculation for both point clouds
- covariance matrix construction
- Singular Value Decomposition
- rotation and translation estimation
- iterative transformation update
- convergence check based on the error change

The implemented algorithm aligns the transformed source point cloud to the target point cloud step by step. In each iteration, the closest corresponding points are found, the best rigid transformation is calculated, and the source cloud is moved closer to the target cloud.

## Metrics

The project uses the following metrics to evaluate the quality of point cloud registration:

- mean error in each ICP iteration
- RMSE after alignment
- execution time
- number of iterations
- Open3D fitness value

These metrics make it possible to compare the custom NumPy implementation with the Open3D implementation and analyze how accurately the point clouds were aligned.

## How to run

Install the required libraries:

```bash
pip install numpy scipy matplotlib open3d
