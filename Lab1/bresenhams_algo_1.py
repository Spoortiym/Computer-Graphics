import matplotlib.pyplot as plt

x1, y1 = 20, 10
x2, y2 = 30, 18

dx = x2 - x1
dy = y2 - y1

p = 2 * dy - dx

x = x1
y = y1

points = []

while x <= x2:
    points.append((x, y))

    x = x + 1

    if p >= 0:
        y = y + 1
        p = p + 2 * dy - 2 * dx
    else:
        p = p + 2 * dy

print("Points:")
print(points)

# Plot
x_values = [p[0] for p in points]
y_values = [p[1] for p in points]

plt.plot(x_values, y_values, 'o-')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Bresenham Line: (20,10) to (30,18)")
plt.grid()
plt.show()