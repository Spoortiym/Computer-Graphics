
import os
import glfw
from OpenGL.GL import *
from PIL import Image


# Vertex Shader
vertex_shader_source = """
#version 330 core

layout (location = 0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos, 1.0);
}
"""


# Fragment Shader
fragment_shader_source = """
#version 330 core

out vec4 FragColor;

void main()
{
    FragColor = vec4(0.2, 0.6, 1.0, 1.0);
}
"""


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader)
        raise RuntimeError(
            "Shader compilation failed: " + str(error)
        )

    return shader


def create_shader_program():
    vertex_shader = compile_shader(
        vertex_shader_source, GL_VERTEX_SHADER
    )

    fragment_shader = compile_shader(
        fragment_shader_source, GL_FRAGMENT_SHADER
    )

    program = glCreateProgram()

    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program)
        raise RuntimeError(
            "Shader linking failed: " + str(error)
        )

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program


def save_output(width, height):
    # Read the rendered image from the back buffer
    glFinish()

    pixels = glReadPixels(
        0, 0, width, height,
        GL_RGB, GL_UNSIGNED_BYTE
    )

    image = Image.frombytes(
        "RGB", (width, height), pixels
    )

    # OpenGL image data starts from the bottom
    image = image.transpose(
        Image.Transpose.FLIP_TOP_BOTTOM
    )

    # Save beside this Python file
    folder = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(
        folder, "shader_output.png"
    )

    image.save(output_path)
    print("Output image saved at:", output_path)


def main():
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    # Request OpenGL 3.3 Core Profile
    glfw.window_hint(
        glfw.CONTEXT_VERSION_MAJOR, 3
    )
    glfw.window_hint(
        glfw.CONTEXT_VERSION_MINOR, 3
    )
    glfw.window_hint(
        glfw.OPENGL_PROFILE,
        glfw.OPENGL_CORE_PROFILE
    )

    window = glfw.create_window(
        700, 600,
        "Vertex and Fragment Shader",
        None, None
    )

    if not window:
        glfw.terminate()
        raise RuntimeError(
            "Could not create OpenGL window. "
            "Check OpenGL driver support."
        )

    glfw.make_context_current(window)

    # Three vertices of a triangle
    vertices = [
         0.0,  0.6, 0.0,
        -0.6, -0.5, 0.0,
         0.6, -0.5, 0.0
    ]

    # Create Vertex Array Object
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(
        GL_ARRAY_BUFFER,
        len(vertices) * 4,
        (GLfloat * len(vertices))(*vertices),
        GL_STATIC_DRAW
    )

    # Configure vertex position attribute
    glVertexAttribPointer(
        0, 3, GL_FLOAT, GL_FALSE,
        3 * 4, ctypes.c_void_p(0)
    )
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # Compile and link shaders
    shader_program = create_shader_program()

    saved = False

    # Main rendering loop
    while not glfw.window_should_close(window):
        width, height = glfw.get_framebuffer_size(window)

        glViewport(0, 0, width, height)
        glClearColor(0.08, 0.08, 0.12, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader_program)
        glBindVertexArray(VAO)

        # Draw the triangle
        glDrawArrays(GL_TRIANGLES, 0, 3)

        glBindVertexArray(0)

        # Save the first rendered frame
        if not saved and width > 0 and height > 0:
            save_output(width, height)
            saved = True

        glfw.swap_buffers(window)
        glfw.poll_events()

    # Release resources
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteProgram(shader_program)

    glfw.terminate()


if __name__ == "__main__":
    main()
