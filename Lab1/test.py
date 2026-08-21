import glfw
from OpenGL.GL import *

if not glfw.init():
    print("GLFW initialization failed")
    exit()

window = glfw.create_window(800, 600, "OpenGL Test", None, None)

if not window:
    glfw.terminate()
    print("Window creation failed")
    exit()

glfw.make_context_current(window)

while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)

    glColor3f(1, 0, 0)
    glVertex2f(-0.5, -0.5)

    glColor3f(0, 1, 0)
    glVertex2f(0.5, -0.5)

    glColor3f(0, 0, 1)
    glVertex2f(0.0, 0.5)

    glEnd()

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()