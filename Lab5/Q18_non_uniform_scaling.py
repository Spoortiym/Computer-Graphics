import numpy as np
import matplotlib.pyplot as plt


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
# Non-Uniform Scaling Factors
# ------------------------------------------------

sx = 2
sy = 0.5


# ------------------------------------------------
# Scaling Matrix
# ------------------------------------------------

S = np.array([
    [sx, 0,  0],
    [0,  sy, 0],
    [0,  0,  1]
], dtype=float)


# ------------------------------------------------
# Apply Scaling
# ------------------------------------------------

transformed_polygon = []

for point in polygon:

    new_point = S @ point

    transformed_polygon.append(new_point)


transformed_polygon = np.array(transformed_polygon)


# ------------------------------------------------
# Display Results
# ------------------------------------------------

print("Non-Uniform Scaling")

print("\nScaling Matrix:")
print(S)

print("\nOriginal Coordinates:")
print(polygon)

print("\nTransformed Coordinates:")
print(transformed_polygon)


# ------------------------------------------------
# Extract Coordinates
# ------------------------------------------------

original_x = polygon[:, 0]
original_y = polygon[:, 1]

scaled_x = transformed_polygon[:, 0]
scaled_y = transformed_polygon[:, 1]


# Close polygons

original_x = np.append(
    original_x,
    original_x[0]
)

original_y = np.append(
    original_y,
    original_y[0]
)

scaled_x = np.append(
    scaled_x,
    scaled_x[0]
)

scaled_y = np.append(
    scaled_y,
    scaled_y[0]
)


# ------------------------------------------------
# Plot
# ------------------------------------------------

plt.figure(figsize=(10, 7))


# Original polygon

plt.plot(
    original_x,
    original_y,
    '-o',
    label="Original Polygon"
)


# Scaled polygon

plt.plot(
    scaled_x,
    scaled_y,
    '-o',
    label="Non-Uniform Scaled Polygon"
)


# X-axis

plt.axhline(
    0,
    linewidth=1
)


# Y-axis

plt.axvline(
    0,
    linewidth=1
)


# Grid

plt.grid(
    True,
    linestyle='--',
    alpha=0.6
)


# Equal scale

plt.axis('equal')


# Labels

plt.xlabel("X")

plt.ylabel("Y")


# Title

plt.title(
    "Non-Uniform Scaling of a Polygon"
)


plt.legend()


# ------------------------------------------------
# Save Image
# ------------------------------------------------

plt.savefig(
    "Q18_non_uniform_scaling.png",
    dpi=150,
    bbox_inches="tight"
)


plt.show()


print(
    "\nImage saved as Q18_non_uniform_scaling.png"
)