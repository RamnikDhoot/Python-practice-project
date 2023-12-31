import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Stars")

# Define colors and fonts
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
font = pygame.font.SysFont(None, 36)

# Load sounds
catch_sound = pygame.mixer.Sound("catch.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

# Game Variables
basket_x = WIDTH // 2
basket_y = HEIGHT - 50
basket_width = 100
basket_speed = 5

star_x = random.randint(0, WIDTH)
star_y = 0
star_speed = 3

score = 0
level = 1
clock = pygame.time.Clock()

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move basket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
        basket_x += basket_speed

    # Update star position
    star_y += star_speed
    if star_y > HEIGHT:
        game_over_sound.play()
        running = False

    # Check for catching the star
    if basket_y < star_y < basket_y + 30 and basket_x < star_x < basket_x + basket_width:
        score += 1
        catch_sound.play()
        star_y = 0
        star_x = random.randint(0, WIDTH)

        if score % 10 == 0:
            level += 1
            star_speed += 1

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (basket_x, basket_y, basket_width, 30))  # Basket
    pygame.draw.circle(screen, WHITE, (star_x, star_y), 10)  # Star

    # Display score and level
    score_text = font.render(f'Score: {score}', True, WHITE)
    level_text = font.render(f'Level: {level}', True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

# Game Over
screen.fill(BLACK)
game_over_text = font.render('Game Over', True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(2000)

pygame.quit()
