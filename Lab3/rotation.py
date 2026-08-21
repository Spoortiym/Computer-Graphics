import math
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
# Rotation Matrix
# -----------------------------------------

angle = 45

theta = math.radians(angle)

R = np.array([
    [math.cos(theta), -math.sin(theta), 0],
    [math.sin(theta),  math.cos(theta), 0],
    [0,                0,               1]
], dtype=float)


# -----------------------------------------
# Apply Rotation
# -----------------------------------------

transformed = []

for point in triangle:
    new_point = R @ point
    transformed.append(new_point)

transformed = np.array(transformed)


# Print matrix
print("Rotation Matrix:")
print(R)

print("\nOriginal Coordinates:")
print(triangle)

print("\nTransformed Coordinates:")
print(transformed)


# -----------------------------------------
# Display Function
# -----------------------------------------

def display():

    glClear(GL_COLOR_BUFFER_BIT)

    # Draw original triangle
    glColor3f(0.6, 0.6, 0.6)

    glBegin(GL_LINE_LOOP)

    for point in triangle:
        glVertex2f(point[0], point[1])

    glEnd()


    # Draw rotated triangle
    glColor3f(0.0, 0.0, 1.0)

    glBegin(GL_TRIANGLES)

    for point in transformed:
        glVertex2f(point[0], point[1])

    glEnd()

    glFlush()


# -----------------------------------------
# Save OpenGL Window as Image
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

    image.save("rotation.png")

    print("\nImage saved as rotation.png")


# -----------------------------------------
# Main Display
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

    glutInitWindowSize(700, 700)

    glutCreateWindow(
        b"Experiment 3 - Rotation"
    )

    # White background
    glClearColor(
        1.0,
        1.0,
        1.0,
        1.0
    )

    # Set coordinate system
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
# Program Start
# -----------------------------------------

if __name__ == "__main__":
    main()