import pygame
import circleshape
import player

class Shield(circleshape.CircleShape):
    def __init__(self, player: player.Player):
        super().__init__(player.position.x, player.position.y, player.radius + 5)
        self.shield_is_up = True
        self.__player = player

    def __update_position(self, player: player.Player):
        self.position = player.position

    def update(self, dt: int):
        self.__update_position(self.__player)

    def draw(self, screen):
        if self.shield_is_up:
            pygame.draw.circle(screen, "blue", self.position, self.radius, 2)