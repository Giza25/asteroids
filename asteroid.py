import pygame
from math import sqrt
import random
from circleshape import CircleShape
from player import Player
from constants import ASTEROID_MIN_RADIUS, ASTEROID_KINDS

class Asteroid(CircleShape):
    __asteroid_image = pygame.image.load("resources/Asteroid.png")

    def __init__(self, x, y, radius, kind):
        super().__init__(x, y, radius)
        self.__kind = kind
        self.mass = pow(self.__kind, 0.7)
        
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
        ast = Asteroid(self.position.x, self.position.y, new_radius, self.__kind - 1)
        ast.velocity = vector * 1.2

    """
    This function calculates the distance between a player triangle and 
    a center of the asteroid:
    - for each side it calculates the distance between a side (a segment) and a point 
    - returns the minimal distance calculated
    """
    def get_distance_between_triangle_and_point(self, triangle: list[float, float, float]):
        point = self.position
        x1, y1 = triangle[0].x, triangle[0].y
        x2, y2 = triangle[1].x, triangle[1].y
        x3, y3 = triangle[2].x, triangle[2].y
        
        top = [(point.x - x1) * (x2 - x1) + (point.y - y1) * (y2 - y1),
               (point.x - x2) * (x3 - x2) + (point.y - y2) * (y3 - y2),
               (point.x - x3) * (x1 - x3) + (point.y - y1) * (y1 - y3)]
        bottom = [pow(x2 - x1, 2) + pow(y2 - y1, 2),
                  pow(x3 - x2, 2) + pow(y3 - y2, 2),
                  pow(x1 - x3, 2) + pow(y1 - y3, 2)]
        
        t = []
        for i in range(3):
            t.append(top[i] / bottom[i])
            if t[i] < 0:
                t[i] = 0
            elif t[i] > 1:
                t[i] = 1
        
        distance = [sqrt(pow(x1 - point.x + t[0] * (x2 - x1), 2) + pow(y1 - point.y + t[0] * (y2 - y1), 2)),
                    sqrt(pow(x2 - point.x + t[1] * (x3 - x2), 2) + pow(y2 - point.y + t[1] * (y3 - y2), 2)),
                    sqrt(pow(x3 - point.x + t[2] * (x1 - x3), 2) + pow(y3 - point.y + t[2] * (y1 - y3), 2))]
        
        return min(distance)

    def collision_with_player(self, player: Player):
        distance = self.get_distance_between_triangle_and_point(player.triangle())
        if distance <= self.radius:
            return True
        return False
    
    def collision_check(self, other: "CircleShape"):
        distance = pygame.math.Vector2.distance_to(self.position, other.position)
        if distance < (self.radius + other.radius):
            return True
        return False

    """
    This method draws asteroids and makes them appear as a png image stored in /resources
    """
    def draw(self, screen: pygame.Surface):
        scaled_asteroid = pygame.transform.scale(Asteroid.__asteroid_image, (self.radius + ASTEROID_MIN_RADIUS * self.__kind, self.radius + ASTEROID_MIN_RADIUS * self.__kind))
        scaled_asteroid_rect = scaled_asteroid.get_rect()
        scaled_asteroid_rect.center = self.position
        screen.blit(scaled_asteroid, scaled_asteroid_rect)

        # this line is used to draw an actual hitbox of the asteroid
        pygame.draw.circle(screen, "purple", self.position, self.radius, 3)

    def update(self, dt: int):
        self.position += self.velocity * dt