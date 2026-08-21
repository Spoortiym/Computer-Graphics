import glfw
from OpenGL.GL import *
import random
import math
import time

# -------------------------
# Initialize GLFW
# -------------------------
if not glfw.init():
    raise Exception("GLFW Failed")

window = glfw.create_window(800, 600, "Catch The Ball - Part 2", None, None)

if not window:
    glfw.terminate()
    raise Exception("Window Failed")

glfw.make_context_current(window)

# -------------------------
# Game Variables
# -------------------------
basket_x = 0.0
basket_width = 0.30

ball_x = random.uniform(-0.9, 0.9)
ball_y = 0.95
ball_radius = 0.05

ball_speed = 0.003

score = 0
lives = 3

# -------------------------
# Draw Circle
# -------------------------
def circle(x, y, r):

    glBegin(GL_TRIANGLE_FAN)

    glVertex2f(x, y)

    for i in range(101):
        angle = 2 * math.pi * i / 100

        glVertex2f(
            x + r * math.cos(angle),
            y + r * math.sin(angle)
        )

    glEnd()


print("=================================")
print("       CATCH THE BALL")
print("=================================")
print("Controls : LEFT and RIGHT Arrow")
print("Lives :", lives)
print("---------------------------------")

# -------------------------
# Main Loop
# -------------------------
while not glfw.window_should_close(window):

    glfw.poll_events()

    # -------------------------
    # Basket Movement
    # -------------------------
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        basket_x -= 0.02

    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        basket_x += 0.02

    if basket_x < -0.85:
        basket_x = -0.85

    if basket_x > 0.85:
        basket_x = 0.85

    # -------------------------
    # Ball Movement
    # -------------------------
    ball_y -= ball_speed

    # -------------------------
    # Catch or Miss
    # -------------------------
    if ball_y <= -0.78:

        if basket_x - basket_width/2 <= ball_x <= basket_x + basket_width/2:

            score += 1
            print("✅ Score :", score)

            # Increase speed slightly
            if ball_speed < 0.01:
                ball_speed += 0.0002

        else:

            lives -= 1
            print("❌ Missed! Lives :", lives)

            if lives == 0:
                print("\n========== GAME OVER ==========")
                print("Final Score :", score)
                break

        # Reset Ball
        ball_x = random.uniform(-0.9, 0.9)
        ball_y = 0.95

    # -------------------------
    # Draw Background
    # -------------------------
    glClearColor(0.5, 0.8, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # Ground
    glColor3f(0.0, 0.7, 0.0)

    glBegin(GL_QUADS)
    glVertex2f(-1, -0.6)
    glVertex2f(1, -0.6)
    glVertex2f(1, -1)
    glVertex2f(-1, -1)
    glEnd()

    # Basket
    glColor3f(1, 1, 0)

    glBegin(GL_QUADS)
    glVertex2f(basket_x - basket_width/2, -0.85)
    glVertex2f(basket_x + basket_width/2, -0.85)
    glVertex2f(basket_x + basket_width/2, -0.78)
    glVertex2f(basket_x - basket_width/2, -0.78)
    glEnd()

    # Ball
    glColor3f(1, 0, 0)
    circle(ball_x, ball_y, ball_radius)

    glfw.swap_buffers(window)

    time.sleep(0.01)

glfw.terminate()