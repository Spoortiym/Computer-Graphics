
import os
import ctypes
import glfw
import numpy as np
from OpenGL.GL import *
from PIL import Image
import math
import time


# Vertex Shader
VERTEX_SHADER = """
#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

uniform mat4 uMVP;

out vec3 vertexColor;

void main()
{
    gl_Position = uMVP * vec4(aPos, 1.0);
    vertexColor = aColor;
}
"""


# Fragment Shader
FRAGMENT_SHADER = """
#version 330 core

in vec3 vertexColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(vertexColor, 1.0);
}
"""


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader)
        raise RuntimeError(str(error))

    return shader


def create_program():
    vs = compile_shader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fs = compile_shader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vs)
    glAttachShader(program, fs)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError(str(glGetProgramInfoLog(program)))

    glDeleteShader(vs)
    glDeleteShader(fs)

    return program


# Perspective projection matrix
def perspective(fov, aspect, near, far):
    f = 1.0 / math.tan(math.radians(fov) / 2.0)

    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far),
         (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ], dtype=np.float32)


# Camera view matrix
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


# Model rotation matrix
def rotation_y(angle):
    c = math.cos(angle)
    s = math.sin(angle)

    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)


# Generate colored cube triangles
def create_cube():
    faces = [
        ((0, 1, 2, 3), (1.0, 0.0, 0.0)),
        ((5, 4, 7, 6), (0.0, 1.0, 0.0)),
        ((4, 0, 3, 7), (0.0, 0.0, 1.0)),
        ((1, 5, 6, 2), (1.0, 1.0, 0.0)),
        ((3, 2, 6, 7), (1.0, 0.0, 1.0)),
        ((4, 5, 1, 0), (0.0, 1.0, 1.0))
    ]

    corners = [
        (-1, -1, -1), (1, -1, -1),
        (1, 1, -1), (-1, 1, -1),
        (-1, -1, 1), (1, -1, 1),
        (1, 1, 1), (-1, 1, 1)
    ]

    data = []

    for indices, color in faces:
        a, b, c, d = [corners[i] for i in indices]

        for point in (a, b, c, a, c, d):
            data.extend(point)
            data.extend(color)

    return np.array(data, dtype=np.float32)


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
    path = os.path.join(folder, "viewing_pipeline_output.png")

    image.save(path)
    print("Output image saved at:", path)


def main():
    if not glfw.init():
        raise RuntimeError("Could not initialize GLFW")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(
        glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE
    )

    window = glfw.create_window(
        800, 600, "3D Viewing Pipeline", None, None
    )

    if not window:
        glfw.terminate()
        raise RuntimeError("Could not create OpenGL window")

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

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

    stride = 6 * 4  # 6 floats per vertex

    glVertexAttribPointer(
        0, 3, GL_FLOAT, GL_FALSE,
        stride, ctypes.c_void_p(0)
    )
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(
        1, 3, GL_FLOAT, GL_FALSE,
        stride, ctypes.c_void_p(12)
    )
    glEnableVertexAttribArray(1)

    glBindVertexArray(0)

    mvp_location = glGetUniformLocation(program, "uMVP")

    view = look_at(
        [3, 2.5, 5],  # Camera position
        [0, 0, 0],    # Look at the cube
        [0, 1, 0]     # Up direction
    )

    saved = False
    start_time = time.time()

    while not glfw.window_should_close(window):
        width, height = glfw.get_framebuffer_size(window)

        if width == 0 or height == 0:
            glfw.poll_events()
            continue

        # Viewport mapping
        glViewport(0, 0, width, height)

        glClearColor(0.08, 0.08, 0.12, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Projection transformation
        projection = perspective(
            45.0, width / height, 0.1, 100.0
        )

        # Model transformation: rotate the cube
        angle = (time.time() - start_time) * 0.7
        model = rotation_y(angle)

        # Complete transformation: Projection * View * Model
        mvp = projection @ view @ model

        glUseProgram(program)

        # NumPy matrices are converted for OpenGL
        glUniformMatrix4fv(
            mvp_location, 1, GL_FALSE, mvp.T
        )

        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)

        # Save the first rendered frame
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
