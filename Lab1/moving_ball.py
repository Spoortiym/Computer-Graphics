import glfw
from OpenGL.GL import *
import math

# Initialize GLFW
if not glfw.init():
    raise Exception("GLFW cannot be initialized!")

# Create Window
window = glfw.create_window(800, 600, "Moving Ball", None, None)

if not window:
    glfw.terminate()
    raise Exception("GLFW window cannot be created!")

glfw.make_context_current(window)

# Ball properties
ball_x = -0.9
ball_y = 0.0
radius = 0.08
speed = 0.005

# Function to draw a filled circle
def draw_circle(x, y, r):
    glBegin(GL_TRIANGLE_FAN)

    # Center of circle
    glColor3f(1.0, 0.0, 0.0)  # Red
    glVertex2f(x, y)

    # Circle boundary
    for i in range(101):
        angle = 2 * math.pi * i / 100
        glVertex2f(
            x + math.cos(angle) * r,
            y + math.sin(angle) * r
        )

    glEnd()

# Main Loop
while not glfw.window_should_close(window):

    glfw.poll_events()

    # Background color (black)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw ball
    draw_circle(ball_x, ball_y, radius)

    # Move ball
    ball_x += speed

    # Reset position after reaching right side
    if ball_x > 1.1:
        ball_x = -1.1

    glfw.swap_buffers(window)

# Cleanup
glfw.terminate()