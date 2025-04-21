import pygame
from circleshape import CircleShape
from shot import Shot
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_ACCELERATION, PLAYER_SPEED_CAP, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_DELAY, PLAYER_MASS

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.__mass = PLAYER_MASS
        self.__speed = 0
        self.__clock = PLAYER_SHOOT_DELAY
    
    def triangle(self, position):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = position + forward * self.radius
        b = position - forward * self.radius - right
        c = position - forward * self.radius + right
        return [a, b, c]
    
    def reset(self):
        self.kill()
        return Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def rotate(self, dt: int):
        self.rotation += PLAYER_TURN_SPEED * dt

    def __update_speed(self, dt: int):
        if abs(self.__speed) <= PLAYER_SPEED_CAP:
            self.__speed += PLAYER_ACCELERATION * dt
        
    def move(self, dt: int):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * self.__speed * dt

    def __handle_out_of_bounds(self):
        if self.position.y <= 0:
            self.position.y = 0
        if self.position.y >= SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT
        if self.position.x <= 0:
            self.position.x = 0
        if self.position.x >= SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH

    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    
    def update(self, dt: int):
        keys = pygame.key.get_pressed()
        self.__clock += dt
        ready_to_shoot = False
        if self.__clock >= PLAYER_SHOOT_DELAY:
            ready_to_shoot = True
        
        if self.__speed > 0:
            self.__speed -= self.__mass
        elif self.__speed < 0:
            self.__speed += self.__mass
        self.move(dt)
        self.__handle_out_of_bounds()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.__update_speed(dt)
        if keys[pygame.K_s]:
            self.__update_speed(-dt)
        if keys[pygame.K_SPACE] and ready_to_shoot:
            self.__clock = 0
            self.shoot()

    def draw(self, screen: pygame.Surface):
        pygame.draw.polygon(screen, "white", self.triangle(self.position), 2)