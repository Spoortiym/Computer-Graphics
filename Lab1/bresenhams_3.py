import matplotlib.pyplot as plt

# User input
x1 = int(input("Enter x1: "))
y1 = int(input("Enter y1: "))
x2 = int(input("Enter x2: "))
y2 = int(input("Enter y2: "))

dx = abs(x2 - x1)
dy = abs(y2 - y1)

sx = 1 if x2 > x1 else -1
sy = 1 if y2 > y1 else -1

x = x1
y = y1

points = []

if dx > dy:
    p = 2 * dy - dx

    for i in range(dx + 1):
        points.append((x, y))

        x = x + sx

        if p >= 0:
            y = y + sy
            p = p + 2 * dy - 2 * dx
        else:
            p = p + 2 * dy

else:
    p = 2 * dx - dy

    for i in range(dy + 1):
        points.append((x, y))

        y = y + sy

        if p >= 0:
            x = x + sx
            p = p + 2 * dx - 2 * dy
        else:
            p = p + 2 * dx

# Display points
print("\nBresenham Points:")
print(points)

# Plot
x_values = [p[0] for p in points]
y_values = [p[1] for p in points]

plt.plot(x_values, y_values, 'o-',color="black")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Bresenham Line Drawing Algorithm")
plt.grid()
plt.show()