
import os
from PIL import Image

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

angle = 0
saved = False


def init():
    glClearColor(0.05, 0.05, 0.10, 1.0)
    glEnable(GL_DEPTH_TEST)

    # Enable Phong-style lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Ambient light
    glLightfv(
        GL_LIGHT0, GL_AMBIENT,
        [0.2, 0.2, 0.2, 1.0]
    )

    # Diffuse light
    glLightfv(
        GL_LIGHT0, GL_DIFFUSE,
        [0.8, 0.8, 0.8, 1.0]
    )

    # Specular light
    glLightfv(
        GL_LIGHT0, GL_SPECULAR,
        [1.0, 1.0, 1.0, 1.0]
    )

    # Position of light source
    glLightfv(
        GL_LIGHT0, GL_POSITION,
        [2.0, 2.0, 3.0, 1.0]
    )

    # Material properties of sphere
    glMaterialfv(
        GL_FRONT, GL_AMBIENT,
        [0.2, 0.05, 0.05, 1.0]
    )

    glMaterialfv(
        GL_FRONT, GL_DIFFUSE,
        [0.8, 0.1, 0.1, 1.0]
    )

    glMaterialfv(
        GL_FRONT, GL_SPECULAR,
        [1.0, 1.0, 1.0, 1.0]
    )

    # Shininess controls highlight sharpness
    glMaterialf(GL_FRONT, GL_SHININESS, 64.0)

    # Smooth shading
    glShadeModel(GL_SMOOTH)


def save_output():
    glFinish()

    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)

    # Capture the rendered OpenGL image
    pixels = glReadPixels(
        0, 0, width, height,
        GL_RGB, GL_UNSIGNED_BYTE
    )

    image = Image.frombytes(
        "RGB", (width, height), pixels
    )

    # Flip image vertically
    image = image.transpose(
        Image.Transpose.FLIP_TOP_BOTTOM
    )

    # Save beside this Python file
    folder = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(
        folder, "phong_output.png"
    )

    image.save(output_path)
    print("Output image saved at:", output_path)


def display():
    global saved

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Set camera position
    gluLookAt(
        0, 0, 5,
        0, 0, 0,
        0, 1, 0
    )

    # Rotate the sphere
    glRotatef(angle, 0, 1, 0)

    # Draw the 3D sphere
    glutSolidSphere(1.0, 60, 60)

    # Save only the first rendered frame
    if not saved:
        save_output()
        saved = True

    glutSwapBuffers()


def reshape(width, height):
    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(
        45.0,
        width / max(height, 1),
        0.1,
        100.0
    )

    glMatrixMode(GL_MODELVIEW)


def update(value):
    global angle

    angle = (angle + 1) % 360

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def main():
    glutInit()
    glutInitDisplayMode(
        GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH
    )

    glutInitWindowSize(700, 600)
    glutCreateWindow(b"Phong Illumination Model")

    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glutTimerFunc(0, update, 0)

    glutMainLoop()


if __name__ == "__main__":
    main()
