import pygame
from Base import element, on_click_element


class Button(on_click_element):
    def __init__(self, width, height, x, y, background=(255, 255, 255), color=(0, 0, 0), text="", font="Arial", font_size=10, alpha=100, ref="") -> None:
        self.backgroud = background
        self.color = color
        self.alpha = alpha
        self.text = text
        self.font = pygame.font.SysFont(font, font_size)
        super().__init__(width, height, x, y, ref, pygame.Surface((width, height)))


    def __str__(self) -> str:
        return f"<Button ({self.x}, {self.y})>"


    def __repr__(self) -> str:
        return self.__str__()


    def render(self):
        self.surface.fill(self.color)
        self.surface.set_alpha(self.alpha)