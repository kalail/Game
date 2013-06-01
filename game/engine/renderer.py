import PAL
import pygame
import theme
from .units import GameObject, Entity
import units.components as components

from OpenGL.GL import *
from OpenGL.GLU import *

class OpenGLRenderer(object):
    """OpenGL Renderer

    Handles all rendering capabilities.

    """

    def __init__(self, resolution, fullscreen, clear_color):
        self.clear_color = clear_color
        self.resolution = resolution
        self.surface = PAL.create_surface(resolution, fullscreen)
        self.resize()

        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_FLAT)
        glClearColor(*clear_color)
        glEnable(GL_COLOR_MATERIAL)

    def resize(self):
        width = self.resolution[0]
        height = self.resolution[1]
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, float(width)/height, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw(self, entities):
        for e in entities:
            if isinstance(e, components.Renderable):
                pygame.draw.circle(self.surface, theme.red, e.position, 10, 0)
            elif isinstance(e, components.SimpleRenderable):
                if isinstance(e, components.Rotatable):
                    offset_vertices = [(v[0] + e.position[0], v[1] + e.position[1]) for v in e.rotated_vertices]
                else:
                    offset_vertices = [(v[0] + e.position[0], v[1] + e.position[1]) for v in e.vertices]
                pygame.draw.aalines(self.surface, e.color, True, offset_vertices, 3)
        # self.object_manager.draw(self.renderer.surface)

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    def flip(self):
        PAL.flip()