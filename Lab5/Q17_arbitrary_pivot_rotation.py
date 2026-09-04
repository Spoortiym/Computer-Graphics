import numpy as np
import matplotlib.pyplot as plt
import math


# ------------------------------------------------
# Original Polygon
# ------------------------------------------------

polygon = np.array([
    [1, 1, 1],
    [3, 1, 1],
    [3, 3, 1],
    [1, 3, 1]
], dtype=float)


# ------------------------------------------------
# Pivot Point
# ------------------------------------------------

pivot_x = 2
pivot_y = 2


# Rotation angle
angle = 45

theta = math.radians(angle)


# ------------------------------------------------
# Translation Matrix
# ------------------------------------------------

def translation(tx, ty):

    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=float)


# ------------------------------------------------
# Rotation Matrix
# ------------------------------------------------

def rotation(angle):

    theta = math.radians(angle)

    return np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta),  math.cos(theta), 0],
        [0, 0, 1]
    ], dtype=float)


# ------------------------------------------------
# Transformation about Arbitrary Pivot
# ------------------------------------------------

T1 = translation(-pivot_x, -pivot_y)

R = rotation(angle)

T2 = translation(pivot_x, pivot_y)


# Combined transformation matrix

M = T2 @ R @ T1


# ------------------------------------------------
# Apply Transformation
# ------------------------------------------------

transformed_polygon = []

for point in polygon:

    new_point = M @ point

    transformed_polygon.append(new_point)


transformed_polygon = np.array(transformed_polygon)


# ------------------------------------------------
# Print Results
# ------------------------------------------------

print("Original Polygon:")
print(polygon)

print("\nTransformation Matrix:")
print(M)

print("\nRotated Polygon:")
print(transformed_polygon)


# ------------------------------------------------
# Prepare Polygon Coordinates
# ------------------------------------------------

original_x = polygon[:, 0]
original_y = polygon[:, 1]

rotated_x = transformed_polygon[:, 0]
rotated_y = transformed_polygon[:, 1]


# Close polygon

original_x = np.append(original_x, original_x[0])
original_y = np.append(original_y, original_y[0])

rotated_x = np.append(rotated_x, rotated_x[0])
rotated_y = np.append(rotated_y, rotated_y[0])


# ------------------------------------------------
# Plot
# ------------------------------------------------

plt.figure(figsize=(9, 7))


# Original polygon

plt.plot(
    original_x,
    original_y,
    '-o',
    label="Original Polygon"
)


# Rotated polygon

plt.plot(
    rotated_x,
    rotated_y,
    '-o',
    label="Rotated Polygon"
)


# Pivot point

plt.plot(
    pivot_x,
    pivot_y,
    'o',
    markersize=8,
    label="Pivot Point"
)


# Axes

plt.axhline(0, linewidth=1)

plt.axvline(0, linewidth=1)


# Grid

plt.grid(True, linestyle='--', alpha=0.6)


# Equal scale

plt.axis('equal')


# Labels

plt.xlabel("X")

plt.ylabel("Y")


# Title

plt.title(
    "Rotation of Polygon About an Arbitrary Pivot Point"
)


plt.legend()


# ------------------------------------------------
# Save Image
# ------------------------------------------------

plt.savefig(
    "Q17_arbitrary_pivot_rotation.png",
    dpi=150,
    bbox_inches="tight"
)


plt.show()


print(
    "\nImage saved as Q17_arbitrary_pivot_rotation.png"
)