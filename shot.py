import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def update(self, dt: int):
        self.position += self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(screen, "purple", self.position, self.radius, 2)