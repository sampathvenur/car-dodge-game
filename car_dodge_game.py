import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Dodge Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)

# Player Car
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 100, 50, 80)
player_speed = 7

# Obstacles (cars/barriers)
obstacles = []
obstacle_spawn_timer = 0
obstacle_speed = 6

# Score
font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

def draw(player, obstacles, score):
    WIN.fill(GRAY)
    
    # Road lines
    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(WIN, YELLOW, (WIDTH//2 - 5, i, 10, 20))
    
    # Player car
    pygame.draw.rect(WIN, BLUE, player)
    
    # Obstacles
    for obs in obstacles:
        pygame.draw.rect(WIN, BLACK, obs)
    
    # Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    WIN.blit(score_text, (10, 10))
    pygame.display.update()

def game_over_screen(score):
    WIN.fill(BLACK)
    msg = font.render("Game Over", True, YELLOW)
    scr = font.render(f"Your Score: {score}", True, WHITE)
    WIN.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 50))
    WIN.blit(scr, (WIDTH//2 - scr.get_width()//2, HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global obstacle_spawn_timer
    run = True
    obstacles.clear()

    while run:
        clock.tick(60)
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

        # Spawn obstacles
        obstacle_spawn_timer += 1
        if obstacle_spawn_timer > 30:
            obs = pygame.Rect(random.randint(0, WIDTH - 40), -60, 40, 60)
            obstacles.append(obs)
            obstacle_spawn_timer = 0

        # Move obstacles
        for obs in obstacles:
            obs.y += obstacle_speed
            if obs.colliderect(player):
                game_over_screen(seconds)
                return
        obstacles[:] = [obs for obs in obstacles if obs.y < HEIGHT]

        draw(player, obstacles, seconds)

if __name__ == "__main__":
    main()