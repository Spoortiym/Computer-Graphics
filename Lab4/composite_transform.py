
import os
import ctypes
import math

import glfw
import numpy as np
from OpenGL.GL import *
from PIL import Image


# Vertex Shader
VERTEX_SHADER = """
#version 330 core

layout (location = 0) in vec2 aPos;

uniform mat3 uTransform;
uniform bool uApplyTransform;

void main()
{
    vec3 position = vec3(aPos, 1.0);

    if (uApplyTransform)
        position = uTransform * position;

    gl_Position = vec4(position.xy, 0.0, 1.0);
}
"""


# Fragment Shader
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
        error = glGetShaderInfoLog(shader)
        raise RuntimeError(str(error))

    return shader


def create_shader_program():
    vertex = compile_shader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragment = compile_shader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program)
        raise RuntimeError(str(error))

    glDeleteShader(vertex)
    glDeleteShader(fragment)

    return program


# Translation matrix
def translation(tx, ty):
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=np.float32)


# Rotation matrix
def rotation(angle_degrees):
    angle = math.radians(angle_degrees)
    c = math.cos(angle)
    s = math.sin(angle)

    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ], dtype=np.float32)


# Scaling matrix
def scaling(sx, sy):
    return np.array([
        [sx, 0,  0],
        [0,  sy, 0],
        [0,  0,  1]
    ], dtype=np.float32)


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
    path = os.path.join(folder, "composite_output.png")

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
        800, 600, "Composite 2D Transformations", None, None
    )

    if not window:
        glfw.terminate()
        raise RuntimeError("Could not create OpenGL window")

    glfw.make_context_current(window)

    program = create_shader_program()

    # Original triangle vertices in 2D
    vertices = np.array([
         0.0,  0.25,
        -0.2, -0.15,
         0.2, -0.15
    ], dtype=np.float32)

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
        0, 2, GL_FLOAT, GL_FALSE,
        2 * 4, ctypes.c_void_p(0)
    )
    glEnableVertexAttribArray(0)

    glBindVertexArray(0)

    color_location = glGetUniformLocation(program, "uColor")
    transform_location = glGetUniformLocation(
        program, "uTransform"
    )
    apply_location = glGetUniformLocation(
        program, "uApplyTransform"
    )

    # Composite matrix: C = T * R * S
    T = translation(0.45, 0.10)
    R = rotation(30)
    S = scaling(1.5, 1.5)

    composite = T @ R @ S

    # OpenGL expects column-major matrix data
    matrix_data = np.ascontiguousarray(composite.T)

    saved = False

    while not glfw.window_should_close(window):
        width, height = glfw.get_framebuffer_size(window)

        if width == 0 or height == 0:
            glfw.poll_events()
            continue

        glViewport(0, 0, width, height)

        glClearColor(0.08, 0.08, 0.12, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(program)
        glBindVertexArray(vao)

        # Draw original triangle in grey
        glUniform1i(apply_location, GL_FALSE)
        glUniform3f(color_location, 0.65, 0.65, 0.65)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # Draw transformed triangle in orange
        glUniform1i(apply_location, GL_TRUE)
        glUniformMatrix3fv(
            transform_location,
            1,
            GL_FALSE,
            matrix_data
        )
        glUniform3f(color_location, 1.0, 0.45, 0.10)
        glDrawArrays(GL_TRIANGLES, 0, 3)

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
