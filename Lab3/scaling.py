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
# Scaling Matrix
# -----------------------------------------

sx = 1.5
sy = 1.5

S = np.array([
    [sx, 0,  0],
    [0,  sy, 0],
    [0,  0,  1]
], dtype=float)


# -----------------------------------------
# Apply Scaling
# -----------------------------------------

transformed = []

for point in triangle:
    new_point = S @ point
    transformed.append(new_point)

transformed = np.array(transformed)


# -----------------------------------------
# Display Matrix and Coordinates
# -----------------------------------------

print("Scaling Matrix:")
print(S)

print("\nOriginal Coordinates:")
print(triangle)

print("\nTransformed Coordinates:")
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


    # Scaled triangle
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

    # Flip image vertically
    image = image.transpose(
        Image.Transpose.FLIP_TOP_BOTTOM
    )

    image.save("scaling.png")

    print("\nImage saved as scaling.png")


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
        b"Experiment 3 - Scaling"
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