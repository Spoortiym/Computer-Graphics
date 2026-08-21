import matplotlib.pyplot as plt


# -----------------------------------------
# Midpoint Circle Drawing Algorithm
# -----------------------------------------

def midpoint_circle(radius):
    points = []

    x = 0
    y = radius

    # Initial decision parameter
    p = 1 - radius

    while x <= y:

        # Eight-way symmetry
        points.append((x, y))
        points.append((-x, y))
        points.append((x, -y))
        points.append((-x, -y))

        points.append((y, x))
        points.append((-y, x))
        points.append((y, -x))
        points.append((-y, -x))

        # Update decision parameter
        if p < 0:
            x = x + 1
            p = p + 2 * x + 1

        else:
            x = x + 1
            y = y - 1
            p = p + 2 * x - 2 * y + 1

    return points


# -----------------------------------------
# Parameters
# -----------------------------------------

radius = 10

points = midpoint_circle(radius)


# Remove duplicate points
points = list(set(points))


# Sort points around the circle
import math

points.sort(
    key=lambda p: math.atan2(p[1], p[0])
)


# Separate X and Y coordinates
x_values = [p[0] for p in points]
y_values = [p[1] for p in points]


# -----------------------------------------
# Plot
# -----------------------------------------

plt.figure(figsize=(10, 8))

plt.plot(
    x_values,
    y_values,
    '-o',
    markersize=5
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


# Axis labels
plt.xlabel("X")
plt.ylabel("Y")


# Title
plt.title(
    "Midpoint Circle Drawing Algorithm (Radius = 10)"
)


# Show integer ticks
plt.xticks(range(-10, 11, 2))
plt.yticks(range(-10, 11, 2))


# Save image
plt.savefig(
    "midpoint_circle.png",
    dpi=150,
    bbox_inches="tight"
)


plt.show()


print("Circle generated using Midpoint Circle Drawing Algorithm.")
print("Image saved as midpoint_circle.png")