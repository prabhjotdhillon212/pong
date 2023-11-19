import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 60
BALL_SIZE = 15
WHITE = (255, 255, 255)
BALL_SPEED = 7
PADDLE_SPEED = 7
AI_PADDLE_SPEED = 5  # Default AI speed
FONT = pygame.font.Font(None, 36)
WINNING_SCORE = 10

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Pong")

# Initialize game state variables
player_score = 0
ai_score = 0
game_running = False
game_paused = False
difficulty_level = "Normal"  # Can be "Easy", "Normal", or "Hard"

# Function to set AI difficulty
def set_ai_difficulty(difficulty):
    global AI_PADDLE_SPEED
    if difficulty == "Easy":
        AI_PADDLE_SPEED = 3
    elif difficulty == "Hard":
        AI_PADDLE_SPEED = 7
    else:
        AI_PADDLE_SPEED = 5

# Set the AI difficulty
set_ai_difficulty(difficulty_level)

# Paddle and Ball positions
player_paddle = pygame.Rect(10, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH//2 - BALL_SIZE//2, SCREEN_HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Ball movement direction
ball_dx = random.choice([1, -1]) * BALL_SPEED
ball_dy = random.choice([1, -1]) * BALL_SPEED

# Function to draw the score
def draw_score():
    player_score_text = FONT.render(str(player_score), True, WHITE)
    ai_score_text = FONT.render(str(ai_score), True, WHITE)
    screen.blit(player_score_text, (SCREEN_WIDTH // 4, 20))
    screen.blit(ai_score_text, (SCREEN_WIDTH * 3 // 4, 20))

# Function to draw the middle dashed line
def draw_middle_line():
    for y in range(0, SCREEN_HEIGHT, 20):
        if y % 40 == 0:
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 2, y, 4, 10))

# Function to check for a winner
def check_for_winner():
    if player_score >= WINNING_SCORE:
        return "Player"
    elif ai_score >= WINNING_SCORE:
        return "AI"
    return None

# Function to reset the game
def reset_game():
    global player_score, ai_score, ball, ball_dx, ball_dy
    player_score = 0
    ai_score = 0
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_dx = random.choice([1, -1]) * BALL_SPEED
    ball_dy = random.choice([1, -1]) * BALL_SPEED

# Function to draw menu
def draw_menu(menu_text):
    screen.fill((0, 0, 0))
    text_surface = FONT.render(menu_text, True, WHITE)
    screen.blit(text_surface, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()

# Start and pause menu
while not game_running:
    draw_menu("Press SPACE to start")
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_running = True
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_paused = not game_paused

    if game_paused:
        draw_menu("Paused - Press ESC to continue")
        continue

    # Player paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_paddle.bottom < SCREEN_HEIGHT:
        player_paddle.y += PADDLE_SPEED

    # AI paddle movement (Advanced Logic)
    if ball_dx > 0:  # Only move AI paddle if the ball is moving towards it
        predicted_y = ball.y + ((ai_paddle.x - ball.x) / ball_dx) * ball_dy
        if ai_paddle.centery < predicted_y and ai_paddle.bottom < SCREEN_HEIGHT:
            ai_paddle.y += min(AI_PADDLE_SPEED, predicted_y - ai_paddle.centery)
        elif ai_paddle.centery > predicted_y and ai_paddle.top > 0:
            ai_paddle.y -= min(AI_PADDLE_SPEED, ai_paddle.centery - predicted_y)

    # Ball movement
    ball.x += ball_dx
    ball.y += ball_dy

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_dy *= -1

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
        ball_dx *= -1

    # Check if the ball goes out of bounds
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        # Update score
        if ball.left <= 0: ai_score += 1
        if ball.right >= SCREEN_WIDTH: player_score += 1

        # Check for a winner
        winner = check_for_winner()
        if winner:
            draw_menu(f"{winner} Wins! - Press SPACE to restart")
            pygame.display.flip()
            time.sleep(3)
            reset_game()
            continue

        # Reset the ball
        ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ball_dx = random.choice([1, -1]) * BALL_SPEED
        ball_dy = random.choice([1, -1]) * BALL_SPEED

    # Drawing
    screen.fill((0, 0, 0))
    draw_middle_line()
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, ai_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    draw_score()
    pygame.display.flip()
    pygame.time.Clock().tick(60)
