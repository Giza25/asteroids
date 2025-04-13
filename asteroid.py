import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, ASTEROID_KINDS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        angle = random.uniform(20, 50)
        self.__create_asteroid(angle)
        self.__create_asteroid(-angle)

    def __create_asteroid(self, angle):
        vector = self.velocity.rotate(angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        ast = Asteroid(self.position.x, self.position.y, new_radius)
        ast.velocity = vector * 1.2

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, "red", self.position, self.radius, 2)

    def update(self, dt: int):
        self.position += self.velocity * dt