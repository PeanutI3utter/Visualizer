import pygame

class window(object):
    def __init__(self, width, height, window_title="Title") -> None:
        self.width = width
        self.height = height
        self.window_title = window_title
        self.init()
        self.window_elements = window_elements()

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.window_title)


    def event_loop(self):
        pass

    def __str__(self) -> str:
        return f'<Window Object width={self.width} height={self.height} window_title={self.window_title}/>'

    def __repr__(self) -> str:
        return self.__str__()

    def run(self):
        self.event_loop(self)


class window_elements:
    def __init__(self):
        pass