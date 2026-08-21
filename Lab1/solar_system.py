import glfw
from OpenGL.GL import *
import math

# ----------------------------
# Initialize GLFW
# ----------------------------
if not glfw.init():
    raise Exception("GLFW initialization failed!")

window = glfw.create_window(800, 800, "Solar System", None, None)

if not window:
    glfw.terminate()
    raise Exception("Window creation failed!")

glfw.make_context_current(window)

# ----------------------------
# Draw Circle Function
# ----------------------------
def draw_circle(x, y, radius, r, g, b):
    glColor3f(r, g, b)

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)

    for i in range(101):
        angle = 2 * math.pi * i / 100
        glVertex2f(
            x + radius * math.cos(angle),
            y + radius * math.sin(angle)
        )

    glEnd()

# ----------------------------
# Animation Variables
# ----------------------------
earth_angle = 0
moon_angle = 0

# ----------------------------
# Main Loop
# ----------------------------
while not glfw.window_should_close(window):

    glfw.poll_events()

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    # ----------------------------
    # SUN
    # ----------------------------
    draw_circle(0, 0, 0.12, 1.0, 1.0, 0.0)

    # ----------------------------
    # EARTH POSITION
    # ----------------------------
    earth_x = 0.45 * math.cos(math.radians(earth_angle))
    earth_y = 0.45 * math.sin(math.radians(earth_angle))

    draw_circle(earth_x, earth_y, 0.06, 0.0, 0.3, 1.0)

    # ----------------------------
    # MOON POSITION
    # ----------------------------
    moon_x = earth_x + 0.12 * math.cos(math.radians(moon_angle))
    moon_y = earth_y + 0.12 * math.sin(math.radians(moon_angle))

    draw_circle(moon_x, moon_y, 0.025, 0.8, 0.8, 0.8)

    # ----------------------------
    # Update Angles
    # ----------------------------
    earth_angle += 0.5
    moon_angle += 2

    if earth_angle >= 360:
        earth_angle = 0

    if moon_angle >= 360:
        moon_angle = 0

    glfw.swap_buffers(window)

glfw.terminate()