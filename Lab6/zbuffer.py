
import os
import ctypes
import math

import glfw
import numpy as np
from OpenGL.GL import *
from PIL import Image


# Vertex shader
VERTEX_SHADER = """
#version 330 core

layout (location = 0) in vec3 aPos;

uniform mat4 uMVP;

void main()
{
    gl_Position = uMVP * vec4(aPos, 1.0);
}
"""


# Fragment shader
FRAGMENT_SHADER = """
#version 330 core

uniform vec3 uColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(uColor, 1.0);
}
"""


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(
            glGetShaderInfoLog(shader).decode()
        )

    return shader


def create_program():
    vertex = compile_shader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragment = compile_shader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError(
            glGetProgramInfoLog(program).decode()
        )

    glDeleteShader(vertex)
    glDeleteShader(fragment)

    return program


def perspective(fov, aspect, near, far):
    f = 1.0 / math.tan(math.radians(fov) / 2.0)

    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far),
         (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ], dtype=np.float32)


def look_at(eye, target, up):
    eye = np.array(eye, dtype=np.float32)
    target = np.array(target, dtype=np.float32)
    up = np.array(up, dtype=np.float32)

    forward = target - eye
    forward /= np.linalg.norm(forward)

    side = np.cross(forward, up)
    side /= np.linalg.norm(side)

    up_vector = np.cross(side, forward)

    return np.array([
        [side[0], side[1], side[2],
         -np.dot(side, eye)],
        [up_vector[0], up_vector[1], up_vector[2],
         -np.dot(up_vector, eye)],
        [-forward[0], -forward[1], -forward[2],
         np.dot(forward, eye)],
        [0, 0, 0, 1]
    ], dtype=np.float32)


def translation(x, y, z):
    matrix = np.eye(4, dtype=np.float32)
    matrix[0, 3] = x
    matrix[1, 3] = y
    matrix[2, 3] = z
    return matrix


def rotation_y(angle):
    c = math.cos(angle)
    s = math.sin(angle)

    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)


def create_cube():
    corners = [
        (-0.5, -0.5, -0.5),
        ( 0.5, -0.5, -0.5),
        ( 0.5,  0.5, -0.5),
        (-0.5,  0.5, -0.5),
        (-0.5, -0.5,  0.5),
        ( 0.5, -0.5,  0.5),
        ( 0.5,  0.5,  0.5),
        (-0.5,  0.5,  0.5)
    ]

    faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 4, 7, 3),
        (1, 5, 6, 2),
        (3, 2, 6, 7),
        (0, 1, 5, 4)
    ]

    vertices = []

    for face in faces:
        a, b, c, d = face

        for index in (a, b, c, a, c, d):
            vertices.extend(corners[index])

    return np.array(vertices, dtype=np.float32)


def save_output(width, height):
    glFinish()
    glReadBuffer(GL_BACK)

    pixels = glReadPixels(
        0, 0, width, height,
        GL_RGB, GL_UNSIGNED_BYTE
    )

    image = Image.frombytes("RGB", (width, height), pixels)
    image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "zbuffer_output.png")

    image.save(path)
    print("Output image saved at:", path)


def main():
    if not glfw.init():
        raise RuntimeError("GLFW initialization failed")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(
        glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE
    )

    window = glfw.create_window(
        800, 600, "Z-Buffer Hidden Surface Removal", None, None
    )

    if not window:
        glfw.terminate()
        raise RuntimeError("Could not create OpenGL window")

    glfw.make_context_current(window)

    # Enable Z-buffer (depth testing)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    program = create_program()
    vertices = create_cube()

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes,
        vertices,
        GL_STATIC_DRAW
    )

    glVertexAttribPointer(
        0, 3, GL_FLOAT, GL_FALSE,
        3 * 4, ctypes.c_void_p(0)
    )
    glEnableVertexAttribArray(0)

    glBindVertexArray(0)

    mvp_location = glGetUniformLocation(program, "uMVP")
    color_location = glGetUniformLocation(program, "uColor")

    view = look_at(
        [3, 2.5, 5],
        [0, 0, 0],
        [0, 1, 0]
    )

    projection = perspective(45, 800 / 600, 0.1, 100)

    saved = False

    while not glfw.window_should_close(window):
        width, height = glfw.get_framebuffer_size(window)

        if width == 0 or height == 0:
            glfw.poll_events()
            continue

        glViewport(0, 0, width, height)

        # Clear both color and depth buffers every frame
        glClearColor(0.08, 0.08, 0.12, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(program)
        glBindVertexArray(vao)

        # First cube: red, positioned behind
        model1 = translation(-0.35, 0.0, -0.35)
        mvp1 = projection @ view @ model1

        glUniformMatrix4fv(
            mvp_location, 1, GL_TRUE, mvp1
        )
        glUniform3f(color_location, 1.0, 0.15, 0.15)
        glDrawArrays(GL_TRIANGLES, 0, 36)

        # Second cube: blue, positioned in front
        model2 = translation(0.35, 0.0, 0.45)
        mvp2 = projection @ view @ model2

        glUniformMatrix4fv(
            mvp_location, 1, GL_TRUE, mvp2
        )
        glUniform3f(color_location, 0.15, 0.45, 1.0)
        glDrawArrays(GL_TRIANGLES, 0, 36)

        glBindVertexArray(0)

        # Save the first rendered frame only
        if not saved:
            save_output(width, height)
            saved = True

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [vbo])
    glDeleteProgram(program)

    glfw.terminate()


if __name__ == "__main__":
    main()
