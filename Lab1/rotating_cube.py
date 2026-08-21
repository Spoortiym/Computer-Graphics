import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# -----------------------------
# Initialize GLFW
# -----------------------------
if not glfw.init():
    raise Exception("GLFW Initialization Failed")

window = glfw.create_window(800, 600, "3D Rotating Cube", None, None)

if not window:
    glfw.terminate()
    raise Exception("Window Creation Failed")

glfw.make_context_current(window)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

angle = 0

# -----------------------------
# Draw Cube
# -----------------------------
def draw_cube():

    glBegin(GL_QUADS)

    # Front (Red)
    glColor3f(1,0,0)
    glVertex3f(-1,-1,1)
    glVertex3f(1,-1,1)
    glVertex3f(1,1,1)
    glVertex3f(-1,1,1)

    # Back (Green)
    glColor3f(0,1,0)
    glVertex3f(-1,-1,-1)
    glVertex3f(-1,1,-1)
    glVertex3f(1,1,-1)
    glVertex3f(1,-1,-1)

    # Left (Blue)
    glColor3f(0,0,1)
    glVertex3f(-1,-1,-1)
    glVertex3f(-1,-1,1)
    glVertex3f(-1,1,1)
    glVertex3f(-1,1,-1)

    # Right (Yellow)
    glColor3f(1,1,0)
    glVertex3f(1,-1,-1)
    glVertex3f(1,1,-1)
    glVertex3f(1,1,1)
    glVertex3f(1,-1,1)

    # Top (Cyan)
    glColor3f(0,1,1)
    glVertex3f(-1,1,-1)
    glVertex3f(-1,1,1)
    glVertex3f(1,1,1)
    glVertex3f(1,1,-1)

    # Bottom (Magenta)
    glColor3f(1,0,1)
    glVertex3f(-1,-1,-1)
    glVertex3f(1,-1,-1)
    glVertex3f(1,-1,1)
    glVertex3f(-1,-1,1)

    glEnd()

# -----------------------------
# Main Loop
# -----------------------------
while not glfw.window_should_close(window):

    glfw.poll_events()

    glClearColor(0.1, 0.1, 0.15, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 50)

    # Model View
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Camera
    glTranslatef(0, 0, -7)

    # Rotate Cube
    glRotatef(angle, 1, 1, 0)

    draw_cube()

    glfw.swap_buffers(window)

    angle += 0.5

glfw.terminate()