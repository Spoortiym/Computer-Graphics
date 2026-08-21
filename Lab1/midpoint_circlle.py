import matplotlib.pyplot as plt

# User input
xc = int(input("Enter center x: "))
yc = int(input("Enter center y: "))
r = int(input("Enter radius: "))

x = 0
y = r

p = 1 - r

points = []

while x <= y:

    # 8-way symmetry
    points.append((xc + x, yc + y))
    points.append((xc - x, yc + y))
    points.append((xc + x, yc - y))
    points.append((xc - x, yc - y))

    points.append((xc + y, yc + x))
    points.append((xc - y, yc + x))
    points.append((xc + y, yc - x))
    points.append((xc - y, yc - x))

    if p < 0:
        p = p + 2 * x + 3
    else:
        p = p + 2 * (x - y) + 5
        y = y - 1

    x = x + 1

# Plot
x_values = [p[0] for p in points]
y_values = [p[1] for p in points]

plt.scatter(x_values, y_values, color='red')

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Midpoint Circle Drawing Algorithm")
plt.grid()
plt.axis("equal")
plt.show()