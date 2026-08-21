import glfw
from OpenGL.GL import *

# Plot the 8 symmetric points of the circle
def draw_circle_points(xc, yc, x, y):
    glVertex2i(xc + x, yc + y)
    glVertex2i(xc - x, yc + y)
    glVertex2i(xc + x, yc - y)
    glVertex2i(xc - x, yc - y)
    glVertex2i(xc + y, yc + x)
    glVertex2i(xc - y, yc + x)
    glVertex2i(xc + y, yc - x)
    glVertex2i(xc - y, yc - x)


# Bresenham Circle Algorithm
def bresenham_circle(xc, yc, r):
    x = 0
    y = r
    d = 3 - 2 * r

    glBegin(GL_POINTS)

    while x <= y:
        draw_circle_points(xc, yc, x, y)

        if d < 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1

        x += 1

    glEnd()


# Display Function
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1.0, 1.0, 1.0)

    # Draw circle
    bresenham_circle(300, 300, 150)

    glFlush()


def main():
    if not glfw.init():
        print("GLFW initialization failed")
        return

    window = glfw.create_window(600, 600, "Bresenham Circle", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Background color
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 600, 0, 600, -1, 1)

    glPointSize(2)

    while not glfw.window_should_close(window):
        display()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()