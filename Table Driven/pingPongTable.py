import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong with AI")

# Game variables
paddle_width, paddle_height = 100, 20
ball_radius = 10
ball_speed = [5, 5]
paddle_speed = 7
player_paddle_x = width // 2 - paddle_width // 2
ai_paddle_x = width // 2 - paddle_width // 2
paddle_y = height - paddle_height - 10
ai_paddle_y = 10
ball_x, ball_y = width // 2, height // 2

# AI difficulty (1 - easy, >1 - harder)
ai_difficulty = 0.9

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Control player paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_paddle_x > 0:
        player_paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and player_paddle_x < width - paddle_width:
        player_paddle_x += paddle_speed

    # AI paddle control
    if ai_paddle_x + paddle_width/2 < ball_x:
        ai_paddle_x += min(paddle_speed * ai_difficulty, ball_x - (ai_paddle_x + paddle_width/2))
    if ai_paddle_x + paddle_width/2 > ball_x:
        ai_paddle_x -= min(paddle_speed * ai_difficulty, (ai_paddle_x + paddle_width/2) - ball_x)

    # Keep AI paddle within screen
    ai_paddle_x = max(min(ai_paddle_x, width - paddle_width), 0)

    # Update ball position
    ball_x += ball_speed[0]
    ball_y += ball_speed[1]

    # Collision detection with walls
    if ball_x <= 0 or ball_x >= width - ball_radius:
        ball_speed[0] = -ball_speed[0]
    if ball_y <= 0 or ball_y >= height - ball_radius:
        ball_speed[1] = -ball_speed[1]

    # Collision with paddles
    if paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height and \
       player_paddle_x <= ball_x <= player_paddle_x + paddle_width:
        ball_speed[1] = -ball_speed[1]

    if ai_paddle_y + paddle_height >= ball_y - ball_radius >= ai_paddle_y and \
       ai_paddle_x <= ball_x <= ai_paddle_x + paddle_width:
        ball_speed[1] = -ball_speed[1]

    # Draw paddles and ball
    pygame.draw.rect(screen, (255, 255, 255), (player_paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, (255, 0, 0), (ai_paddle_x, ai_paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, (255, 255, 255), (ball_x, ball_y), ball_radius)

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()