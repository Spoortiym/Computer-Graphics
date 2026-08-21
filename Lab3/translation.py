import numpy as np
from PIL import Image

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


# Original triangle
triangle = np.array([
    [-0.5, -0.5, 1],
    [ 0.5, -0.5, 1],
    [ 0.0,  0.5, 1]
], dtype=float)


# Translation matrix
tx = 0.8
ty = 0.5

T = np.array([
    [1, 0, tx],
    [0, 1, ty],
    [0, 0, 1]
], dtype=float)


# Apply transformation
transformed = []

for point in triangle:
    new_point = T @ point
    transformed.append(new_point)

transformed = np.array(transformed)


def display():

    glClear(GL_COLOR_BUFFER_BIT)

    # Original triangle
    glColor3f(0.7, 0.7, 0.7)

    glBegin(GL_LINE_LOOP)

    for point in triangle:
        glVertex2f(point[0], point[1])

    glEnd()


    # Translated triangle
    glColor3f(0.0, 0.0, 1.0)

    glBegin(GL_TRIANGLES)

    for point in transformed:
        glVertex2f(point[0], point[1])

    glEnd()

    glFlush()

    # Save image
    glReadBuffer(GL_FRONT)

    pixels = glReadPixels(
        0, 0,
        700, 700,
        GL_RGB,
        GL_UNSIGNED_BYTE
    )

    image = Image.frombytes(
        "RGB",
        (700, 700),
        pixels
    )

    image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    image.save("translation.png")

    print("Translation image saved as translation.png")


def main():

    glutInit()

    glutInitDisplayMode(
        GLUT_SINGLE | GLUT_RGB
    )

    glutInitWindowSize(700, 700)

    glutCreateWindow(
        b"2D Translation"
    )

    glClearColor(
        1.0, 1.0, 1.0, 1.0
    )

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluOrtho2D(-2, 2, -2, 2)

    glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(display)

    glutMainLoop()


if __name__ == "__main__":
    main()