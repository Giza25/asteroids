import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from shield import Shield

def game_loop(
        screen: pygame.Surface, 
        clock: pygame.time.Clock, 
        delta: int,
        player: Player,
        shield: Shield,
        points_font: pygame.font.Font,
        updatable: pygame.sprite.Group,
        drawable: pygame.sprite.Group,
        asteroids: pygame.sprite.Group,
        shots: pygame.sprite.Group):
    """
    This function serves the role of the game loop as name suggests.
    It takes these parameters:
        screen: pygame Surface class, we are drawing on it
        clock: an in game clock for fps limiting
        delta: an integer working with clock
        player: an object referencing the player
        points_font: A font style used for scoring system
        updatable, drawable, asterouds, shots: pygame Groups that allows us to
            expand the game with more potential objects
    """
    points = 0 # amount of points a player have
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill("black")

        for object in updatable: # update all the objects on the screen
            object.update(delta)

        """
        Checks asteroids behaviour: 
        they should collide with the player resulting in a loss 
        and be splitted as they are being shot
        """
        for asteroid in asteroids: 
            if asteroid.collision_with_player(player):
                if not shield.shield_is_up:
                    running = game_over(screen, points_font, points)
                    drawable.empty()
                    asteroids.empty()
                    points = 0
                    player = player.reset()
                else:
                    shield.shield_is_up = False
                    asteroid.kill()
            for shot in shots:
                if asteroid.collision_check(shot):
                    shot.kill()
                    asteroid.split()
                    points += 1

        for object in drawable: # draws all the objects
            object.draw(screen)
        points_surface = points_font.render(f"Score: {points}", True, "white", "black")

        screen.blit(points_surface, (10, 10))
        pygame.display.flip()
        delta = clock.tick(SCREEN_FPS) / 1000

def game_over(screen: pygame.Surface, score: pygame.font.Font, points: int):
    """
    Create a Game Over message
    """
    game_over_font = pygame.font.Font(None, 120)
    game_over_surface = game_over_font.render("Game Over!", True, "red", "black")
    game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    
    """
    Create a Final Score message
    """
    score_screen = score.render(f"Final Score: {points}", True, "white", "black")
    score_rect = score_screen.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))   

    """
    Create a tip message at the bottom of the screen with potential actions for the user
    """
    tip_font = pygame.font.Font(None, 25)
    tip_screen = tip_font.render("Press Esc to exit. Press R to restart", True, "white", "black")
    tip_rect = tip_screen.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))

    """
    This bit fill the screen with black colour, then displays every text message
    """
    screen.fill("black")
    screen.blit(game_over_surface, game_over_rect)
    screen.blit(score_screen, score_rect)
    screen.blit(tip_screen, tip_rect)
    pygame.display.flip()
    
    """
    This loop waits for user's action:
    - Quit by pressing X on the window
    - Quit by pressing Esc key
    - Restart the game by pressing R
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r:
                    return True


def main():
    pygame.init()
    
    """
    Assigns a name of the containers 
    """
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    """
    Creating objects used in the game
    """
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 50)
    
    """
    Assigns containers to classes
    """
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Shield.containers = (updatable, drawable)

    """
    Creating Asteroid Field and a Player
    """
    AsteroidField() # Calling this class' constructor to create asteroids
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    shield = Shield(player)

    """
    Calling game loop where the game happens
    """
    game_loop(screen, clock, dt, player, shield, font, updatable, drawable, asteroids, shots)

    pygame.quit()

if __name__ == "__main__":
    main()