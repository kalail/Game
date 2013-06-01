import PAL
import pygame
import theme
from .units import GameObject, Entity
import units.components as components

from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL as GL
import OpenGL.GL.shaders
import OpenGL

import ctypes
import numpy


def create_object(shader, vertices):
    # Create a new VAO (Vertex Array Object) and bind it
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray( vertex_array_object )
    # Generate buffers to hold our vertices
    vertex_buffer = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vertex_buffer)
    # Get the position of the 'position' in parameter of our shader and bind it.
    position = GL.glGetAttribLocation(shader, 'position')
    GL.glEnableVertexAttribArray(position)
    # Describe the position data layout in the buffer
    GL.glVertexAttribPointer(position, 4, GL.GL_FLOAT, False, 0, ctypes.c_void_p(0))
    # Send the data over to the buffer
    GL.glBufferData(GL.GL_ARRAY_BUFFER, 48, vertices, GL.GL_STATIC_DRAW)
    # Unbind the VAO first (Important)
    GL.glBindVertexArray( 0 )
    # Unbind other stuff
    GL.glDisableVertexAttribArray(position)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object

class OpenGLRenderer(object):
    """OpenGL Renderer

    Handles all rendering capabilities.

    """

    world_resolution = (640.0, 360.0)
    
    @staticmethod
    def get_world_aspect():
        return OpenGLRenderer.world_resolution[0] / OpenGLRenderer.world_resolution[1]

    @staticmethod
    def match_aspect((width, height)):
        if (width, height) == OpenGLRenderer.world_resolution:
            return (width, height)
        if width > OpenGLRenderer.world_resolution[0]:
            width = OpenGLRenderer.world_resolution[0]
            height = width / OpenGLRenderer.get_world_aspect()
        if height > OpenGLRenderer.world_resolution[1]:
            height = OpenGLRenderer.world_resolution[1]
            width =  height * OpenGLRenderer.get_world_aspect()
        return (int(width), int(height))

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
        gl_FragColor = vec4(0.0f, 0.0f, 0.0f, 1.0f);
    }
    """

    def __init__(self, resolution, fullscreen, clear_color):
        self.clear_color = clear_color
        self.fullscreen = fullscreen
        # Match and save resolution
        self.resolution = OpenGLRenderer.match_aspect(resolution)
        self.width = self.resolution[0]
        self.height = self.resolution[1]
        self.scale_factor = self.resolution[0] / OpenGLRenderer.world_resolution[0]

    def start(self):
        self.surface = PAL.create_surface(self.resolution, self.fullscreen)
        glClearColor(*self.clear_color)
        self.resize()
        # Compile shaders
        self.shader = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(OpenGLRenderer.vertex_shader, GL.GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(OpenGLRenderer.fragment_shader, GL.GL_FRAGMENT_SHADER)
        )
        vertices = [
            0.6, 0.6, 0.0, 1.0,
            -0.6, 0.6, 0.0, 1.0,
            0.0, -0.6, 0.0, 1.0
        ]

        vertices = numpy.array(vertices, dtype=numpy.float32)
        self.vertex_array_object = create_object(self.shader, vertices)


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
        # Reset to modelview
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw(self, entities):
        for e in entities:
            if isinstance(e, components.Renderable):
                pass
            elif isinstance(e, components.SimpleRenderable):
                if isinstance(e, components.Rotatable):
                    offset_vertices = [(v[0] + e.position[0], v[1] + e.position[1]) for v in e.rotated_vertices]
                else:
                    offset_vertices = [(v[0] + e.position[0], v[1] + e.position[1]) for v in e.vertices]
                pygame.draw.aalines(self.surface, e.color, True, offset_vertices, 3)
        
        GL.glUseProgram(self.shader)
        GL.glBindVertexArray(self.vertex_array_object)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        GL.glBindVertexArray( 0 )
        GL.glUseProgram(0)


        glBegin(GL_TRIANGLES);
        glColor(255, 0, 0);
        glVertex(0, 0);
        glVertex(0,1);
        # glColor(0, 0, 255);
        glColor(0, 255, 0);
        glVertex(1, 0);
        glEnd();

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    def flip(self):
        PAL.flip()