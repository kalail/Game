import PAL
import pygame
# import theme
# from .entities import GameObject, Entity
import entities.components as components

from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL as GL
import OpenGL.GL.shaders
import OpenGL

import ctypes
import numpy


def create_object(shader, vertices):
    # Create a new VAO (Vertex Array Object) and bind it
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)
    # Generate buffers to hold our vertices
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    # Get the position of the 'position' parameter of our shader and bind it.
    i_position = glGetAttribLocation(shader, 'position')
    glEnableVertexAttribArray(i_position)
    # Describe the position data layout in the buffer
    glVertexAttribPointer(i_position, 4, GL_FLOAT, False, 0, ctypes.c_void_p(0))
    # Send the data over to the buffer
    glBufferData(GL_ARRAY_BUFFER, 48, vertices, GL_STATIC_DRAW)
    # Unbind the VAO first (Important)
    GL.glBindVertexArray( 0 )
    # Unbind other stuff
    glDisableVertexAttribArray(i_position)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vertex_array_object

class OpenGLRenderer(object):
    """OpenGL Renderer

    Handles all rendering capabilities.

    """
    
    @staticmethod
    def to_engine((x, y)):
        w = self.viewport_size[0] * 2.0
        h = self.viewport_size[1] * 2.0
        _x = self.engine.level.size[0]/2.0 + (x  * self.engine.level.size[0]/2.0)
        _y = self.engine.level.size[1]/2.0 + (x  * self.engine.level.size[1]/2.0)
        return (_x, _y)

    @staticmethod
    def to_renderer((x, y)):
        _x = (x - self.engine.level.size[0]/2.0) / (self.engine.level.size[0]/2.0) * self.viewport_size[0]
        _y = (self.engine.level.size[1]/2.0 - y) / (self.engine.level.size[1]/2.0) * self.viewport_size[1]
        return (_x, _y)

    @staticmethod
    def match_aspect((i_width, i_height), (width, height)):
        aspect = float(width) / height
        i_aspect = float(i_width) / i_height
        if i_aspect > aspect:
            i_width = i_height * aspect
        elif i_aspect < aspect:
            i_height = i_width / aspect
        return (int(i_width), int(i_height))

    vertex_shader = """
    #version 330

    in vec4 position;
    void main()
    {
        gl_Position = position;
    }
    """

    fragment_shader = """
    #version 330

    void main()
    {
        gl_FragColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
    }
    """

    def __init__(self, engine):
        self.engine = engine
        config = engine.config
        self.clear_color = engine.level.theme['clear']
        self.fullscreen = config['fullscreen']
        # Match and save resolution
        self.resolution = OpenGLRenderer.match_aspect(config['resolution'], engine.level.size)
        self.scale_factor = self.resolution[0] / engine.level.size[0]

    def start(self):
        self.surface = PAL.create_surface(self.resolution, self.fullscreen)
        glClearColor(*self.clear_color)
        self.resize()
        # Compile shaders
        
        self.vertices = numpy.array(
            [
                -0.1, -0.1, 0.0, 1.0,
                0.1, -0.1, 0.0, 1.0,
                0.1, 0.1, 0.0, 1.0,
                -0.1, 0.1, 0.0, 1.0
            ],
            dtype=numpy.float32
        )

    def compile_program(self):
        self.shader = GL.shaders.compileProgram(
            GL.shaders.compileShader(self.engine.asset_manager.get('shaders/basic.v.glsl'), GL_VERTEX_SHADER),
            GL.shaders.compileShader(self.engine.asset_manager.get('shaders/basic.f.glsl'), GL_FRAGMENT_SHADER)
        )

    def resize(self):
        # Resize viewport
        width = self.resolution[0]
        height = self.resolution[1]
        glViewport(0, 0, width, height)
        # Resize projection
        aspect = OpenGLRenderer.get_world_aspect()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Calculate bounds
        if width >= height:
            left   = -1.0 * aspect
            right  =  1.0 * aspect
            bottom = -1.0
            top    =  1.0
        else:
            left   = -1.0
            right  =  1.0
            bottom = -1.0 / aspect
            top    =  1.0 / aspect
        gluOrtho2D(left, right, bottom, top)
        self.viewport_size = (right, top)
        # Reset to modelview
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw(self, entities):
        for e in entities:
            if isinstance(e, components.Renderable):
                pass
            elif isinstance(e, components.SimpleRenderable):
                    e.draw()
                # if isinstance(e, components.Rotatable):
                    # offset_vertices = [(v[0] + e.position[0], v[1] + e.position[1]) for v in e.rotated_vertices]
                # else:
                    # offset_vertices = [(v[0] + e.position[0], v[1] + e.position[1]) for v in e.vertices]
                # pygame.draw.aalines(self.surface, e.color, True, offset_vertices, 3)

        self.vertices += (PAL.get_pointer_position()[1]/720.0 - 0.5) * 0.001
        vertex_array_object = create_object(self.shader, self.vertices)
        GL.glUseProgram(self.shader)
        GL.glBindVertexArray(vertex_array_object)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)


        glBegin(GL_TRIANGLES);
        glColor(255, 0, 0);
        glVertex(0, 0);
        glVertex(0,1);
        # glColor(0, 0, 255);
        glColor(0, 255, 0);
        vertices = self.to_renderer(PAL.get_pointer_position())
        glVertex(*vertices)
        glEnd();

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    def flip(self):
        PAL.flip()