import os
import math
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# Single function to apply any transformation matrix
# ---------------------------------------------------------
def apply_transformation(matrix, points):
    """
    Apply a transformation matrix to all points.

    matrix -> 3x3 transformation matrix
    points -> points represented using homogeneous coordinates
    """

    transformed_points = []

    for point in points:
        new_point = matrix @ point
        transformed_points.append(new_point)

    return np.array(transformed_points)


# ---------------------------------------------------------
# Transformation matrices
# ---------------------------------------------------------

def translation(tx, ty):
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=float)


def rotation(angle):
    theta = math.radians(angle)

    return np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta),  math.cos(theta), 0],
        [0, 0, 1]
    ], dtype=float)


def scaling(sx, sy):
    return np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ], dtype=float)


def reflection_y_equals_x():
    return np.array([
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ], dtype=float)


def shearing(shx, shy):
    return np.array([
        [1, shx, 0],
        [shy, 1, 0],
        [0, 0, 1]
    ], dtype=float)


# ---------------------------------------------------------
# Original polygon
# ---------------------------------------------------------

polygon = np.array([
    [1, 1, 1],
    [4, 1, 1],
    [4, 3, 1],
    [1, 3, 1]
], dtype=float)


# ---------------------------------------------------------
# Display polygon
# ---------------------------------------------------------

def draw_polygon(points, label):

    x = points[:, 0]
    y = points[:, 1]

    # Close the polygon
    x = np.append(x, x[0])
    y = np.append(y, y[0])

    plt.plot(
        x,
        y,
        marker="o",
        linewidth=2,
        label=label
    )


# ---------------------------------------------------------
# Menu
# ---------------------------------------------------------

print("\n========== TRANSFORMATION MENU ==========")
print("1. Translation")
print("2. Rotation")
print("3. Scaling")
print("4. Reflection about y = x")
print("5. Shearing")
print("6. Exit")

choice = int(input("\nEnter your choice: "))


# ---------------------------------------------------------
# Select transformation
# ---------------------------------------------------------

if choice == 1:

    tx = float(input("Enter translation in X: "))
    ty = float(input("Enter translation in Y: "))

    M = translation(tx, ty)
    title = "Translation"


elif choice == 2:

    angle = float(input("Enter rotation angle: "))

    M = rotation(angle)
    title = "Rotation"


elif choice == 3:

    sx = float(input("Enter scaling factor X: "))
    sy = float(input("Enter scaling factor Y: "))

    M = scaling(sx, sy)
    title = "Scaling"


elif choice == 4:

    M = reflection_y_equals_x()
    title = "Reflection about y = x"


elif choice == 5:

    shx = float(input("Enter shearing factor X: "))
    shy = float(input("Enter shearing factor Y: "))

    M = shearing(shx, shy)
    title = "Shearing"


elif choice == 6:

    print("Program terminated.")
    exit()


else:

    print("Invalid choice.")
    exit()


# ---------------------------------------------------------
# Apply transformation using ONE function
# ---------------------------------------------------------

transformed_polygon = apply_transformation(
    M,
    polygon
)


# ---------------------------------------------------------
# Print matrices
# ---------------------------------------------------------

print("\nOriginal Points:")
print(polygon)

print("\nTransformation Matrix:")
print(M)

print("\nTransformed Points:")
print(transformed_polygon)


# ---------------------------------------------------------
# Plot result
# ---------------------------------------------------------

plt.figure(figsize=(8, 7))

draw_polygon(
    polygon,
    "Original Polygon"
)

draw_polygon(
    transformed_polygon,
    "Transformed Polygon"
)

# X-axis
plt.axhline(
    0,
    linewidth=1.5
)

# Y-axis
plt.axvline(
    0,
    linewidth=1.5
)

plt.grid(True)

plt.xlabel("X-axis")
plt.ylabel("Y-axis")

plt.title(
    "Q23 - " + title
)

plt.legend()

plt.axis("equal")

plt.xlim(-8, 10)
plt.ylim(-8, 10)

plt.tight_layout()


# ---------------------------------------------------------
# Save image
# ---------------------------------------------------------

folder = os.path.dirname(
    os.path.abspath(__file__)
)

output_path = os.path.join(
    folder,
    "Q23_single_matrix_function.png"
)

plt.savefig(
    output_path,
    dpi=150
)

plt.show()

print("\nOutput image saved at:")
print(output_path)