import pygame
from constants import *
from player import Player

def game_loop(
        screen: pygame.Surface, 
        clock: pygame.time.Clock, 
        delta: int, 
        player: Player,
        updatable: pygame.sprite.Group,
        drawable: pygame.sprite.Group):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill("black")

        for object in updatable:
            object.update(delta)
        for object in drawable:
            object.draw(screen)
        
        pygame.display.flip()
        delta = clock.tick(60) / 1000

def main():
    pygame.init()

    print(f'''
Starting Asteroids!
Screen width: {SCREEN_WIDTH}
Screen height: {SCREEN_HEIGHT}
''')
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    game_loop(screen, clock, dt, player, updatable, drawable)

    pygame.quit()

if __name__ == "__main__":
    main()