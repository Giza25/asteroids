import pygame
from constants import *
from player import Player

def game_loop(
        screen: pygame.Surface, 
        clock: pygame.time.Clock, 
        delta: int, 
        player: Player):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill("black")

        player.update(delta)
        player.draw(screen)
        
        pygame.display.flip()
        delta = clock.tick(60) / 1000

def main():
    pygame.init()

    print(f'''
Starting Asteroids!
Screen width: {SCREEN_WIDTH}
Screen height: {SCREEN_HEIGHT}
''')
    
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    game_loop(screen, clock, dt, player)

if __name__ == "__main__":
    main()