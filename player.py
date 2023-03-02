import pygame
from app import *
from settings import *
vec = pygame.math.Vector2


class Player:
    """Class of player."""
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(0, -1)
        self.stored_direction = None
        self.able_to_move = True
        self.life = 3

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        self.grid_pos[0] = self.pix_pos[0] // self.app.cell_width
        self.grid_pos[1] = self.pix_pos[1] // self.app.cell_height

    def draw(self):
        rect = self.app.mini_player_images[self.app.current_level - 1].get_rect()
        rect.center = (self.pix_pos.x, self.pix_pos.y)
        self.app.screen.blit(self.app.mini_player_images[self.app.current_level - 1], rect)

    def on_trap(self):
        if self.grid_pos in self.app.traps:
            return True
        return False

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec(self.grid_pos.x * self.app.cell_width + self.app.cell_width // 2,
                   self.grid_pos.y * self.app.cell_height + self.app.cell_height // 2)

    def time_to_move(self):
        if int(self.pix_pos.x + 5) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True
        if int(self.pix_pos.y + 5) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        for trap in self.app.traps:
            if vec(self.grid_pos) == trap:
                return False
        for door in self.app.doors:
            if vec(self.grid_pos + self.direction) == door:
                return False
        return True
