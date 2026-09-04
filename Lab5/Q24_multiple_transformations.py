import os
import math
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Transformation functions
# ---------------------------------------------------------

def translation(tx, ty):
    """Create a 2D translation matrix."""
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=float)


def rotation(angle):
    """Create a 2D rotation matrix."""
    theta = math.radians(angle)

    return np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta),  math.cos(theta), 0],
        [0, 0, 1]
    ], dtype=float)


def scaling(sx, sy):
    """Create a 2D scaling matrix."""
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ], dtype=float)


def shearing(shx, shy):
    """Create a 2D shearing matrix."""
    return np.array([
        [1, shx, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ], dtype=float)


# ---------------------------------------------------------
# Apply transformation
# ---------------------------------------------------------

def apply_transformation(matrix, polygon):
    """
    Apply a transformation matrix to every point
    of the polygon.
    """

    transformed = []

    for point in polygon:
        new_point = matrix @ point
        transformed.append(new_point)

    return np.array(transformed)


# ---------------------------------------------------------
# Complex polygon
# ---------------------------------------------------------
# This polygon represents a simple house-like object.

polygon = np.array([
    [1, 1, 1],
    [5, 1, 1],
    [5, 4, 1],
    [3, 6, 1],
    [1, 4, 1]
], dtype=float)


# ---------------------------------------------------------
# Create individual transformation matrices
# ---------------------------------------------------------

# 1. Scaling
S = scaling(1.3, 1.3)

# 2. Rotation
R = rotation(30)

# 3. Shearing
H = shearing(0.2, 0)

# 4. Translation
T = translation(2, 1)


# ---------------------------------------------------------
# Combine all transformations
# ---------------------------------------------------------
# Transformations are applied from right to left:
#
# Final = T × H × R × S × Original
#
# First scaling
# Then rotation
# Then shearing
# Finally translation

M = T @ H @ R @ S


# ---------------------------------------------------------
# Apply combined transformation
# ---------------------------------------------------------

transformed_polygon = apply_transformation(
    M,
    polygon
)


# ---------------------------------------------------------
# Print results
# ---------------------------------------------------------

print("\n========== Q24 MULTIPLE TRANSFORMATIONS ==========")

print("\nOriginal Polygon:")
print(polygon)

print("\nScaling Matrix:")
print(S)

print("\nRotation Matrix:")
print(R)

print("\nShearing Matrix:")
print(H)

print("\nTranslation Matrix:")
print(T)

print("\nCombined Transformation Matrix:")
print(M)

print("\nTransformed Polygon:")
print(transformed_polygon)


# ---------------------------------------------------------
# Plot polygon
# ---------------------------------------------------------

plt.figure(figsize=(9, 8))


# Original polygon
original_x = np.append(
    polygon[:, 0],
    polygon[0, 0]
)

original_y = np.append(
    polygon[:, 1],
    polygon[0, 1]
)

plt.plot(
    original_x,
    original_y,
    marker="o",
    linewidth=2,
    label="Original Polygon"
)


# Transformed polygon
new_x = np.append(
    transformed_polygon[:, 0],
    transformed_polygon[0, 0]
)

new_y = np.append(
    transformed_polygon[:, 1],
    transformed_polygon[0, 1]
)

plt.plot(
    new_x,
    new_y,
    marker="o",
    linewidth=2,
    label="After Multiple Transformations"
)


# ---------------------------------------------------------
# Coordinate axes
# ---------------------------------------------------------

plt.axhline(
    0,
    linewidth=1.5
)

plt.axvline(
    0,
    linewidth=1.5
)


# Grid
plt.grid(True)


# Labels
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

plt.title(
    "Q24 - Multiple Transformations on a Complex Polygon"
)

plt.legend()

plt.axis("equal")

plt.xlim(-5, 12)
plt.ylim(-5, 12)


# ---------------------------------------------------------
# Save output
# ---------------------------------------------------------

folder = os.path.dirname(
    os.path.abspath(__file__)
)

output_path = os.path.join(
    folder,
    "Q24_multiple_transformations.png"
)

plt.savefig(
    output_path,
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print("\nOutput image saved at:")
print(output_path)