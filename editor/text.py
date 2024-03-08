# FILE MANAGER
# Authors: Ewen B.
#          Thomas D.

# IMPORTS
import pygame


# CLASSES
class TextManager:
    def __init__(self, font_path: str, color=(255, 255, 255), size=20):
        self._FP = font_path
        self.FONT = pygame.font.Font(self._FP)
        self.COLOR = color
        self.SIZE = size


    def display(self, text: str, pos, surface: pygame.Surface):
        text_surface = self.FONT.render(text, False, self.COLOR)
        rect = text_surface.get_rect()
        rect.topleft = pos
        surface.blit(text_surface, rect)
