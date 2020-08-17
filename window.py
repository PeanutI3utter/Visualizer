import pygame
from threading import Thread
import numpy as np
import time

class window(object):
    """
    class representing a window

    params:
        width:        int  - width of the window
        height:       int  - height of the window
        window_title: str  - Title of the window
        event_loop:   func - event loop function
    """
    def __init__(self, width=800, height=600, window_title='Title placeholder', event_loop=lambda : None) -> None:
        self.width = width
        self.height = height
        self.window_title = window_title
        self.event_loop = event_loop
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(window_title)
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(1, 30)


    def __str__(self) -> str:
        return f'<Window Object width={self.width} height={self.height} window_title={self.window_title}/>'

    def __repr__(self) -> str:
        return self.__str__()

    def run(self):
        self.event_loop(self)
