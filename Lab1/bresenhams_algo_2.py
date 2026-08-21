import matplotlib.pyplot as plt

x1, y1 = 2, 2
x2, y2 = 5, 9

dx = x2 - x1
dy = y2 - y1

p = 2 * dx - dy

x = x1
y = y1

points = []

while y <= y2:
    points.append((x, y))

    y = y + 1

    if p >= 0:
        x = x + 1
        p = p + 2 * dx - 2 * dy
    else:
        p = p + 2 * dx

print("Points:")
print(points)

# Plot
x_values = [p[0] for p in points]
y_values = [p[1] for p in points]

plt.plot(x_values, y_values, 'o-')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Bresenham Line: (2,2) to (5,9)")
plt.grid()
plt.show()

