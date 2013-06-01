import PAL
import pygame
import theme
from .units import GameObject, Entity
import units.components as components

class Renderer(object):
    def __init__(self, resolution, fullscreen, clear_color):
        self.clear_color = clear_color
        self.surface = PAL.create_surface(resolution, fullscreen)

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
        PAL.clear_screen(self.surface, self.clear_color)

    def flip(self):
        PAL.flip()