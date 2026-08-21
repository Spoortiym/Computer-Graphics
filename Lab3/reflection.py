import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image


# -----------------------------------------
# Original Triangle using Homogeneous Coordinates
# -----------------------------------------

triangle = np.array([
    [-0.5, -0.5, 1],
    [ 0.5, -0.5, 1],
    [ 0.0,  0.5, 1]
], dtype=float)


# -----------------------------------------
# Reflection Matrix about X-axis
# -----------------------------------------

F = np.array([
    [1,  0, 0],
    [0, -1, 0],
    [0,  0, 1]
], dtype=float)


# -----------------------------------------
# Apply Reflection
# -----------------------------------------

transformed = []

for point in triangle:
    new_point = F @ point
    transformed.append(new_point)

transformed = np.array(transformed)


# -----------------------------------------
# Display Matrix and Coordinates
# -----------------------------------------

print("Reflection Matrix about X-axis:")
print(F)

print("\nOriginal Coordinates:")
print(triangle)

print("\nReflected Coordinates:")
print(transformed)


# -----------------------------------------
# Display Function
# -----------------------------------------

def display():

    glClear(GL_COLOR_BUFFER_BIT)

    # Original triangle
    glColor3f(0.6, 0.6, 0.6)

    glBegin(GL_LINE_LOOP)

    for point in triangle:
        glVertex2f(point[0], point[1])

    glEnd()


    # Reflected triangle
    glColor3f(0.0, 0.0, 1.0)

    glBegin(GL_TRIANGLES)

    for point in transformed:
        glVertex2f(point[0], point[1])

    glEnd()

    glFlush()


# -----------------------------------------
# Save Image
# -----------------------------------------

def save_image():

    glReadBuffer(GL_FRONT)

    pixels = glReadPixels(
        0,
        0,
        700,
        700,
        GL_RGB,
        GL_UNSIGNED_BYTE
    )

    image = Image.frombytes(
        "RGB",
        (700, 700),
        pixels
    )

    # OpenGL image is upside down
    image = image.transpose(
        Image.Transpose.FLIP_TOP_BOTTOM
    )

    image.save("reflection.png")

    print("\nImage saved as reflection.png")


# -----------------------------------------
# Display and Save
# -----------------------------------------

def display_and_save():

    display()

    save_image()


# -----------------------------------------
# Main Function
# -----------------------------------------

def main():

    glutInit()

    glutInitDisplayMode(
        GLUT_SINGLE | GLUT_RGB
    )

    glutInitWindowSize(
        700,
        700
    )

    glutCreateWindow(
        b"Experiment 3 - Reflection"
    )

    # White background
    glClearColor(
        1.0,
        1.0,
        1.0,
        1.0
    )

    # Coordinate system
    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluOrtho2D(
        -2,
        2,
        -2,
        2
    )

    glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(display_and_save)

    glutMainLoop()


# -----------------------------------------
# Start Program
# -----------------------------------------

if __name__ == "__main__":
    main()