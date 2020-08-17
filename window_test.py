from math import ceil, floor
import pygame
import numpy as np
from window import window
from color import *


class coordinate_system(window):
    def __init__(self, width=800, height=600, window_title='Title placeholder',  resolution=20, origin=np.array([0, 0]), invert_y=False, show_grid=True, tick=1, tick_size=4, show_pos=False, full_screen=True, plot_surf_size=(-1, -1)) -> None:
        super().__init__(width, height, window_title, self.handle_event)
        self.screen.fill(LIGHTGREY)
        if plot_surf_size[0] < 0:
            plot_surf_size_x = width - 40
        else:
            plot_surf_size_x = plot_surf_size[0]
        if plot_surf_size[1] < 0:
            plot_surf_size_y = height - 40
        else:
            plot_surf_size_y = plot_surf_size[1]
        if full_screen:
            self.plotter_w = width
            self.plotter_h = height
            self.plot_surface = self.screen.subsurface((0, 0, width, height))
        else:
            self.plotter_w = plot_surf_size_x
            self.plotter_h = plot_surf_size_y
            self.plot_surface = self.screen.subsurface((width - plot_surf_size_x, height - plot_surf_size_y, plot_surf_size_x, plot_surf_size_y))
        self.resolution = resolution
        self.origin = origin
        self.invert_y = invert_y
        self.show_grid = show_grid
        self.tick = tick
        self.tick_size = tick_size
        self.show_pos = show_pos
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 20)


    def handle_event(self, *args):
        running = True
        if self.show_grid:
            self.draw_grid()
        if self.show_pos:
            self.render_pos()
        pygame.display.update()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
        pygame.quit()


    def normalize_coords(self, disp_coord):
        x = (disp_coord[0] - self.origin[0]) / self.resolution
        y = (disp_coord[1] - self.origin[1]) / self.resolution * -1 if self.invert_y else (disp_coord[1] - self.origin[1]) / self.resolution
        return np.array([x, y])


    def display_coords(self, norm_coords):
        x = norm_coords[0] * self.resolution + self.origin[0]
        y = norm_coords[1] * self.resolution * -1 + self.origin[1] if self.invert_y else norm_coords[1] * self.resolution + self.origin[1]
        return np.array([x, y], dtype=int)


    def draw_grid(self):
        # draw axis x
        x_ax = self.origin[1]
        if x_ax > self.plotter_h:
            x_ax = self.plotter_h
        elif x_ax < 0:
            x_ax = 0
        pygame.draw.line(self.plot_surface, BLACK, (0, x_ax), (self.plotter_w, x_ax))

        # draw ticks x axis
        border_left = self.normalize_coords(np.array([0, 0]))[0] # get normalized coordinate of left edge
        border_right = self.normalize_coords(np.array([self.plotter_w, 0]))[0]
        start = int(ceil(border_left / self.tick) * self.tick)
        end = int(floor(border_right / self.tick) * self.tick)
        tick = start
        while tick <= end:
            u = self.normalize_coords((0, (x_ax + self.tick_size)))[1]
            l = self.normalize_coords((0, (x_ax - self.tick_size)))[1]
            tick_u = self.display_coords((tick , u))
            tick_l = self.display_coords((tick , l))
            pygame.draw.line(self.plot_surface, BLACK, tick_u, tick_l)
            tick += self.tick


        # draw y axis
        y_ax = self.origin[0]
        if y_ax > self.plotter_w:
            y_ax = self.plotter_w
        elif y_ax < 0:
            y_ax = 0
        pygame.draw.line(self.plot_surface, BLACK, (y_ax, 0), (y_ax, self.plotter_h))
        # draw ticks y axis

        if self.invert_y:
            border_high = self.normalize_coords(np.array([0, 0]))[1]
            border_low = self.normalize_coords(np.array([0, self.plotter_h]))[1]
        else:
            border_high = self.normalize_coords(np.array([0, self.plotter_w]))[1]
            border_low = self.normalize_coords(np.array([0, 0]))[1]
        start = int(ceil(border_low / self.tick) * self.tick)
        end = int(floor(border_high / self.tick) * self.tick)
        tick = start
        while tick <= end:
            r = self.normalize_coords(((y_ax + self.tick_size), 0))[0]
            l = self.normalize_coords(((y_ax - self.tick_size), 0))[0]
            tick_r = self.display_coords((r , tick))
            tick_l = self.display_coords((l , tick))
            pygame.draw.line(self.plot_surface, BLACK, tick_r, tick_l)
            tick += self.tick



w = coordinate_system(origin=np.array([380, 280]), full_screen=False)
w.run()