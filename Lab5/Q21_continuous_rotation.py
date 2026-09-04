import os
import math
import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image


# Window size
WIDTH = 700
HEIGHT = 700

# Rotation angle
angle = 0.0

# To save the output image only once
image_saved = False


# ---------------------------------------------------------
# Rotation matrix using homogeneous coordinates
# ---------------------------------------------------------
def rotation_matrix(angle):
    theta = math.radians(angle)

    return np.array([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta),  math.cos(theta), 0],
        [0, 0, 1]
    ], dtype=float)


# ---------------------------------------------------------
# Draw coordinate grid
# ---------------------------------------------------------
def draw_grid():
    glColor3f(0.85, 0.85, 0.85)
    glLineWidth(1)

    glBegin(GL_LINES)

    # Vertical grid lines
    for x in range(-10, 11):
        glVertex2f(x, -10)
        glVertex2f(x, 10)

    # Horizontal grid lines
    for y in range(-10, 11):
        glVertex2f(-10, y)
        glVertex2f(10, y)

    glEnd()


# ---------------------------------------------------------
# Draw X and Y axes
# ---------------------------------------------------------
def draw_axes():

    glLineWidth(2)

    # X-axis
    glColor3f(0, 0, 0)

    glBegin(GL_LINES)
    glVertex2f(-10, 0)
    glVertex2f(10, 0)

    # Y-axis
    glVertex2f(0, -10)
    glVertex2f(0, 10)

    glEnd()


# ---------------------------------------------------------
# Draw the original polygon
# ---------------------------------------------------------
def draw_original_object():

    # Square
    polygon = [
        [-2, -2, 1],
        [ 2, -2, 1],
        [ 2,  2, 1],
        [-2,  2, 1]
    ]

    glColor3f(0.5, 0.5, 0.5)
    glLineWidth(2)

    glBegin(GL_LINE_LOOP)

    for point in polygon:
        glVertex2f(point[0], point[1])

    glEnd()


# ---------------------------------------------------------
# Draw rotated object
# ---------------------------------------------------------
def draw_rotated_object():

    polygon = np.array([
        [-2, -2, 1],
        [ 2, -2, 1],
        [ 2,  2, 1],
        [-2,  2, 1]
    ], dtype=float)

    # Create rotation matrix
    R = rotation_matrix(angle)

    # Apply rotation
    transformed_polygon = []

    for point in polygon:
        new_point = R @ point
        transformed_polygon.append(new_point)

    # Draw filled rotated polygon
    glColor3f(0.2, 0.5, 0.8)

    glBegin(GL_POLYGON)

    for point in transformed_polygon:
        glVertex2f(point[0], point[1])

    glEnd()

    # Draw outline
    glColor3f(0, 0, 0)
    glLineWidth(2)

    glBegin(GL_LINE_LOOP)

    for point in transformed_polygon:
        glVertex2f(point[0], point[1])

    glEnd()


# ---------------------------------------------------------
# Display function
# ---------------------------------------------------------
def display():

    glClear(GL_COLOR_BUFFER_BIT)

    # Draw grid
    draw_grid()

    # Draw coordinate axes
    draw_axes()

    # Draw original object
    draw_original_object()

    # Draw continuously rotated object
    draw_rotated_object()

    glutSwapBuffers()


# ---------------------------------------------------------
# Timer function for continuous rotation
# ---------------------------------------------------------
def update(value):

    global angle

    # Increase angle
    angle += 2

    # Reset after 360 degrees
    if angle >= 360:
        angle = 0

    # Redisplay the object
    glutPostRedisplay()

    # Call update again after 30 milliseconds
    glutTimerFunc(30, update, 0)


# ---------------------------------------------------------
# Save one frame as PNG
# ---------------------------------------------------------
def save_image(value):

    global image_saved

    if image_saved:
        return

    # Read pixels from the front buffer
    glReadBuffer(GL_FRONT)

    pixels = glReadPixels(
        0,
        0,
        WIDTH,
        HEIGHT,
        GL_RGB,
        GL_UNSIGNED_BYTE
    )

    # Convert pixels to PIL image
    image = Image.frombytes(
        "RGB",
        (WIDTH, HEIGHT),
        pixels
    )

    # OpenGL image is upside down, so flip it
    image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    # Save in the same folder as Python file
    folder = os.path.dirname(os.path.abspath(__file__))

    output_path = os.path.join(
        folder,
        "Q21_continuous_rotation.png"
    )

    image.save(output_path)

    print("Output image saved at:")
    print(output_path)

    image_saved = True


# ---------------------------------------------------------
# Initialize OpenGL
# ---------------------------------------------------------
def init():

    glClearColor(1, 1, 1, 1)

    # Set coordinate system
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(-10, 10, -10, 10)

    glMatrixMode(GL_MODELVIEW)


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------
def main():

    glutInit()

    glutInitDisplayMode(
        GLUT_DOUBLE | GLUT_RGB
    )

    glutInitWindowSize(WIDTH, HEIGHT)

    glutCreateWindow(
        b"Q21 - Continuous Rotation"
    )

    init()

    # Display function
    glutDisplayFunc(display)

    # Start animation
    glutTimerFunc(30, update, 0)

    # Save first frame after window starts
    glutTimerFunc(500, save_image, 0)

    # Start OpenGL loop
    glutMainLoop()


# Run program
if __name__ == "__main__":
    main()