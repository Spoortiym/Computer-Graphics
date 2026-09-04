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
# Transformation Functions
# ------------------------------------------------

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


# ------------------------------------------------
# Display Menu
# ------------------------------------------------

print("\n===================================")
print("  2D TRANSFORMATION MENU")
print("===================================")

print("1. Translation")
print("2. Rotation")
print("3. Scaling")
print("4. Reflection about y = x")
print("5. Shearing")
print("6. Exit")

choice = int(input("\nEnter your choice: "))


# ------------------------------------------------
# Select Transformation
# ------------------------------------------------

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

    sx = float(input("Enter scaling factor Sx: "))
    sy = float(input("Enter scaling factor Sy: "))

    M = scaling(sx, sy)

    title = "Scaling"


elif choice == 4:

    M = reflection_y_equals_x()

    title = "Reflection about y = x"


elif choice == 5:

    shx = float(input("Enter X shear factor: "))
    shy = float(input("Enter Y shear factor: "))

    M = shearing(shx, shy)

    title = "Shearing"


elif choice == 6:

    print("Program terminated.")

    exit()


else:

    print("Invalid choice.")

    exit()


# ------------------------------------------------
# Apply Transformation
# ------------------------------------------------

transformed_polygon = []

for point in polygon:

    new_point = M @ point

    transformed_polygon.append(new_point)


transformed_polygon = np.array(
    transformed_polygon
)


# ------------------------------------------------
# Print Results
# ------------------------------------------------

print("\n===================================")
print("Transformation Matrix:")
print("===================================")

print(M)

print("\nOriginal Polygon:")
print(polygon)

print("\nTransformed Polygon:")
print(transformed_polygon)


# ------------------------------------------------
# Extract Coordinates
# ------------------------------------------------

original_x = polygon[:, 0]
original_y = polygon[:, 1]

transformed_x = transformed_polygon[:, 0]
transformed_y = transformed_polygon[:, 1]


# Close polygons

original_x = np.append(
    original_x,
    original_x[0]
)

original_y = np.append(
    original_y,
    original_y[0]
)

transformed_x = np.append(
    transformed_x,
    transformed_x[0]
)

transformed_y = np.append(
    transformed_y,
    transformed_y[0]
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


# Transformed polygon

plt.plot(
    transformed_x,
    transformed_y,
    '-o',
    label="Transformed Polygon"
)


# Axes

plt.axhline(
    0,
    linewidth=1
)

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
    "Menu-Driven 2D Transformation - " + title
)


plt.legend()


# ------------------------------------------------
# Save Image
# ------------------------------------------------

plt.savefig(
    "Q20_menu_transformations.png",
    dpi=150,
    bbox_inches="tight"
)


plt.show()


print(
    "\nImage saved as Q20_menu_transformations.png"
)