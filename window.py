import pygame
import sys

class window(object):
    """
    Abstract class for a window application

    Attributes
    ----------
    width : int
        width of the window
    height : int
        height of the window
    window_title : str
        title of the window
    screen : Pygame surface
        surface object on which everything is rendered on
    window_elements : window_element
        Child elements that are part of application and are drawn onto the screen surface

    Methods
    -------
    event_loop() : () -> None
        event loop of the application
    run() : () -> None
        starts the event loop
    """
    def __init__(self, width, height, window_title="Title") -> None:
        """
        Parameters
        ----------
        width : int
            width of the window
        height : int
            height of the window
        window_title : str
            title of the window       
        """
        self.width = width
        self.height = height
        self.window_title = window_title
        self.run = False
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.window_title)
        self.window_elements = render_element(self.width, self.height, 0, 0, ref="root", surface=self.screen)


    
    def event_loop(self):
        """
        Event loop of the application. Events are polled and passed to the window elements of the application.
        After the event handeling elements are rerendered if they are tagged to be updated.
        """
        while self.run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
            self.window_elements.handle_events(events)
            self.window_elements.update(False)
        pygame.quit(); sys.exit()


    def __str__(self) -> str:
        return f'<Window Object width={self.width} height={self.height} window_title={self.window_title}/>'


    def __repr__(self) -> str:
        return self.__str__()


    def start(self):
        """
        Launches the event loop of the application
        """
        self.run = True
        self.event_loop()


class render_element:
    """
    An element that is rendered in the window. Each element has its own pygame surface, render method and event handler.

    Attributes
    ----------
    width : int
        width of the window element
    height : int
        height of the window element
    x : int
        absolute x coordinate (w.r.t the window)
    y : int
        absolute y coordinate (w.r.t the window)
    children : list
        List of all the children window elements
    state_changed : Bool
        Set to True if state has changed and element needs to be rerendered
    ref : str
        String used to refer to window element. Used to search element in the window element tree. 
    surface : Pygame Surface
        Render surface of the window element
    """
    def __init__(self, width, height, x, y, ref="", surface=None):
        """
        Parameters
        ----------
        width : int
            width of the window element
        height : int
            height of the window element
        x : int
            absolute x coordinate (w.r.t the window)
        y : int
            absolute y coordinate (w.r.t the window)
        children : list
            List of all the children window elements
        state_changed : Bool
            Set to True if state has changed and element needs to be rerendered
        ref : str
            String used to refer to window element. Used to search element in the window element tree. 
        surface : Pygame Surface
            Render surface of the window element
        layer : int 
            elements with higher layer are drawn after elements with lower layer
        overlaps : list<render_elements>
            elements which surface overlaps with the rendering surfaces of other elements in the render tree(except direct children)
        """
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.children = []
        self.__update__ = True
        self.ref = ref
        if surface is None:
            self.surface = pygame.Surface((width, height))  
        else:
            self.surface = surface
        self.layer = -1
        self.overlaps = []


    def __str__(self):
        return f"<Window Element Object ref={self.ref}>"


    def __repr__(self) -> str:
        return self.__str__()


    def handle_events(self, event, **kwargs):
        """
        Event handler of the element

        Parameters
        ----------
        event : pygame.event
            events polled from pygame
        kwargs : dic
            extra arguments for event_handlers, specified by implementer

        Returns
        -------
        Specified by implementer
        """
        pass


    def render(self):
        """
        Render method of the element
        """
        if self.surface is None:
            raise Exception("Surface has not been initiated for window element")
        pass


    def add_child(self, child):
        """
        Add a child window element to the parent element

        Parameter
        ---------
        child : window_element
            Child window element
        """
        self.children.append(child)


    def remove_child(self, child):
        """
        Removes a child element from parent element

        Parameter
        ---------
        child : window_element
            Child to be removed
        """
        for c in self.children:
            if c == child:
                self.children.remove(child)
            else:
                c.remove_child(child)


    def remove_child_by_ref(self, ref, count=sys.maxsize, curr_count=0):
        """
        Removes a child element from parent element by reference string

        Parameter
        ---------
        ref : str
            reference string of the child to be removed
        """
        if curr_count >= count: 
            return
        for c in self.children:
            if c.ref == ref:
                self.children.remove(c)
                curr_count += 1
            c.remove_child(c, count, curr_count)
        if curr_count >= count:
            return
        

    def get_element_by_ref(self, ref):
        """
        Searches for an element by reference string and returns it if found

        Parameter
        ---------
        ref : str
            Reference string of the searched window element

        Returns
        -------
        None if element was not found
        window_element else
            window element matching the reference string
        """
        if ref is None:
            return None
        if self.ref == ref:
            return self
        else:
            for child in self.children:
                traverse_res = child.get_element(ref)
                if traverse_res == ref:
                    return traverse_res
            return None
    

    def update(self, force_update):
        """
        Updates the rendering of the window element if __update__ or force_update is set to True

        Parameter
        ---------
        force_update : Bool
            forces the window element to rerender
        """
        if self.__update__ or force_update:
            self.render()
            for child in self.children:
                child.update(True)
                self.surface.blit(child.surface)
