import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------
# Original Polygon
# ------------------------------------------------

polygon = np.array([
    [1, 2, 1],
    [4, 2, 1],
    [4, 4, 1],
    [1, 4, 1]
], dtype=float)


# ------------------------------------------------
# Reflection Matrix about y = x
# ------------------------------------------------

R = np.array([
    [0, 1, 0],
    [1, 0, 0],
    [0, 0, 1]
], dtype=float)


# ------------------------------------------------
# Apply Reflection
# ------------------------------------------------

transformed_polygon = []

for point in polygon:

    new_point = R @ point

    transformed_polygon.append(new_point)


transformed_polygon = np.array(transformed_polygon)


# ------------------------------------------------
# Display Results
# ------------------------------------------------

print("Reflection about the line y = x")

print("\nReflection Matrix:")
print(R)

print("\nOriginal Coordinates:")
print(polygon)

print("\nReflected Coordinates:")
print(transformed_polygon)


# ------------------------------------------------
# Extract Coordinates
# ------------------------------------------------

original_x = polygon[:, 0]
original_y = polygon[:, 1]

reflected_x = transformed_polygon[:, 0]
reflected_y = transformed_polygon[:, 1]


# Close the polygons

original_x = np.append(
    original_x,
    original_x[0]
)

original_y = np.append(
    original_y,
    original_y[0]
)

reflected_x = np.append(
    reflected_x,
    reflected_x[0]
)

reflected_y = np.append(
    reflected_y,
    reflected_y[0]
)


# ------------------------------------------------
# Plot
# ------------------------------------------------

plt.figure(figsize=(10, 8))


# Original polygon

plt.plot(
    original_x,
    original_y,
    '-o',
    label="Original Polygon"
)


# Reflected polygon

plt.plot(
    reflected_x,
    reflected_y,
    '-o',
    label="Reflected Polygon"
)


# ------------------------------------------------
# Draw y = x line
# ------------------------------------------------

x_line = np.linspace(-6, 6, 100)

plt.plot(
    x_line,
    x_line,
    '--',
    label="y = x"
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


# Equal scaling

plt.axis('equal')


# Labels

plt.xlabel("X")

plt.ylabel("Y")


# Title

plt.title(
    "Reflection of Polygon About the Line y = x"
)


plt.legend()


# ------------------------------------------------
# Save Image
# ------------------------------------------------

plt.savefig(
    "Q19_reflection_y_equals_x.png",
    dpi=150,
    bbox_inches="tight"
)


plt.show()


print(
    "\nImage saved as Q19_reflection_y_equals_x.png"
)