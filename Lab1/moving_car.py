import glfw
from OpenGL.GL import *

# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW can't be initialized")

window = glfw.create_window(800, 600, "Moving Car Animation", None, None)

if not window:
    glfw.terminate()
    raise Exception("Window can't be created")

glfw.make_context_current(window)

car_x = -1.2
speed = 0.005

# Draw Circle (Wheel)
def draw_circle(cx, cy, r):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(cx, cy)

    for i in range(101):
        angle = 2 * 3.14159 * i / 100
        glVertex2f(
            cx + r * __import__('math').cos(angle),
            cy + r * __import__('math').sin(angle)
        )
    glEnd()

# Draw Car
def draw_car(x):

    # Car Body
    glColor3f(1, 0, 0)

    glBegin(GL_QUADS)
    glVertex2f(x-0.20, -0.10)
    glVertex2f(x+0.20, -0.10)
    glVertex2f(x+0.20,  0.05)
    glVertex2f(x-0.20,  0.05)
    glEnd()

    # Car Top
    glColor3f(0.8, 0.2, 0.2)

    glBegin(GL_POLYGON)
    glVertex2f(x-0.10, 0.05)
    glVertex2f(x+0.10, 0.05)
    glVertex2f(x+0.05, 0.15)
    glVertex2f(x-0.05, 0.15)
    glEnd()

    # Windows
    glColor3f(0.5, 0.8, 1)

    glBegin(GL_QUADS)
    glVertex2f(x-0.07, 0.06)
    glVertex2f(x-0.01, 0.06)
    glVertex2f(x-0.01, 0.13)
    glVertex2f(x-0.07, 0.13)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(x+0.01, 0.06)
    glVertex2f(x+0.07, 0.06)
    glVertex2f(x+0.07, 0.13)
    glVertex2f(x+0.01, 0.13)
    glEnd()

    # Wheels
    glColor3f(0,0,0)
    draw_circle(x-0.12, -0.10, 0.05)
    draw_circle(x+0.12, -0.10, 0.05)

# Main Loop
while not glfw.window_should_close(window):

    glfw.poll_events()

    glClearColor(0.5, 0.8, 1.0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    # Road
    glColor3f(0.2,0.2,0.2)
    glBegin(GL_QUADS)
    glVertex2f(-1,-0.15)
    glVertex2f(1,-0.15)
    glVertex2f(1,-1)
    glVertex2f(-1,-1)
    glEnd()

    # Road Divider
    glColor3f(1,1,0)
    for i in range(-10,10,2):
        glBegin(GL_QUADS)
        glVertex2f(i/10,-0.55)
        glVertex2f(i/10+0.10,-0.55)
        glVertex2f(i/10+0.10,-0.52)
        glVertex2f(i/10,-0.52)
        glEnd()

    # Draw Car
    draw_car(car_x)

    # Move Car
    car_x += speed

    if car_x > 1.3:
        car_x = -1.3

    glfw.swap_buffers(window)

glfw.terminate()