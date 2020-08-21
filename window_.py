import pygame

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
        self.render_tree = surface_tree(self.screen)

    

    def __str__(self) -> str:
        return f'<Window Object width={self.width} height={self.height} window_title={self.window_title}/>'

    def __repr__(self) -> str:
        return self.__str__()

    def run(self):
        self.event_loop(self)



class surface_tree():
    def __init__(self, element: pygame.Surface, event_handler=lambda x: 0, render_method=lambda: 0) -> None:
        self.element = element
        self.children = []
        self.event_handler = event_handler
        self.render_method = render_method
        self.updated = True


    def add_child(self, child: pygame.Surface, event_handler=lambda x: 0, render_method=lambda: 0):
        newnode = surface_tree(child, event_handler, render_method)
        self.children.append(newnode)
        return newnode

    def set_update(self):
        self.updated = True

    def update(self, events):
        self.event_handler(events)
        if self.updated:
            self.render_method()
            for child in self.children:
                child.set_update()
                self.surface.blit(child)
        for child in self.children:
            child.update(events)
        self.updated = False

    def get_element(self, element):
        if self.element == element:
            return self
        for child in self.children:
            child_search = child.get_element(element)
            if child_search != None:
                return child_search
        return None
