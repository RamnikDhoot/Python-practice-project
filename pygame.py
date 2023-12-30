import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Stars")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

basket_x = WIDTH // 2
basket_y = HEIGHT - 50
basket_width = 100
basket_speed = 5

star_x = random.randint(0, WIDTH)
star_y = 0
star_speed = 3

score = 0
clock = pygame.time.Clock()

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
        star_y = 0
        star_x = random.randint(0, WIDTH)

    # Check for catching the star
    if basket_y < star_y < basket_y + 30 and basket_x < star_x < basket_x + basket_width:
        score += 1
        star_y = 0
        star_x = random.randint(0, WIDTH)

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (basket_x, basket_y, basket_width, 30)) # Basket
    pygame.draw.circle(screen, WHITE, (star_x, star_y), 10) # Star

    # Display score
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
