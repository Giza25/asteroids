import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    """
    Destroys shots as they leave the screen boundaries
    """
    def __handle_out_of_bounds(self):
        if self.position.y <= -self.radius:
            self.kill()
        if self.position.y >= SCREEN_HEIGHT + self.radius:
            self.kill()
        if self.position.x <= -self.radius:
            self.kill()
        if self.position.x >= SCREEN_WIDTH + self.radius:
            self.kill()

    def update(self, dt: int):
        self.position += self.velocity * dt
        self.__handle_out_of_bounds()

    def draw(self, screen):
        pygame.draw.circle(screen, "purple", self.position, self.radius, 2)