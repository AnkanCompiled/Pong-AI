import pygame
import settings
from paddle import Paddle
from ball import Ball

# Initialize pygame
pygame.init()

# Set up the game window
WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Pong")

# Font for displaying scores
SCORE_FONT = pygame.font.SysFont("roboto", 50)

def draw(win, paddles, ball, left_score, right_score):
    """Draws the game elements onto the window"""
    win.fill(settings.BLACK)  # Fill background with black

    # Render score texts
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, settings.WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, settings.WHITE)

    # Display scores on the screen
    win.blit(left_score_text, (settings.WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (settings.WIDTH * (3/4) - right_score_text.get_width() // 2, 20))

    # Draw paddles
    for paddle in paddles:
        paddle.draw(win)

    # Draw the middle dashed line
    for i in range(10, settings.HEIGHT, settings.HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, settings.WHITE, (settings.WIDTH // 2 - 5, i, 10, settings.HEIGHT // 20))

    # Draw the ball
    ball.draw(win)

    pygame.display.update()

def handle_paddle_movement(keys, left_paddle, right_paddle):
    """Handles paddle movement based on key inputs"""
    # Left paddle movement (W/S keys)
    if keys[pygame.K_w] and left_paddle.y - settings.VEL >= 0:
        left_paddle.move(True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height + settings.VEL <= settings.HEIGHT:
        left_paddle.move(False)

    # Right paddle movement (Arrow Up/Down keys)
    if keys[pygame.K_UP] and right_paddle.y - settings.VEL >= 0:    
        right_paddle.move(True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height + settings.VEL <= settings.HEIGHT:
        right_paddle.move(False)

def handle_collision(ball, left_paddle, right_paddle):
    """Handles ball collision with walls and paddles"""
    # Bounce off top and bottom walls
    if ball.y - ball.radius <= 0 or ball.y + ball.radius >= settings.HEIGHT:
        ball.y_vel *= -1

    # Determine which paddle the ball is approaching
    paddle = left_paddle if ball.x_vel < 0 else right_paddle
    
    # Check collision with the paddle
    if paddle.y <= ball.y <= paddle.y + paddle.height and abs(ball.x - (paddle.x + (paddle.width if ball.x_vel < 0 else 0))) <= ball.radius:
        ball.x_vel *= -1  # Reverse horizontal direction

        # Adjust ball's vertical speed based on the hit position on the paddle
        middle_y = paddle.y + paddle.height // 2
        difference_in_y = ball.y - middle_y
        reduction_factor = (paddle.height // 2) / settings.MAX_VEL
        ball.y_vel = difference_in_y / reduction_factor

def main():
    """Main game loop"""
    run = True
    clock = pygame.time.Clock()
    
    # Initialize paddles and ball
    left_paddle = Paddle(10, settings.HEIGHT // 2 - settings.PADDLE_HEIGHT // 2, settings.PADDLE_WIDTH, settings.PADDLE_HEIGHT)
    right_paddle = Paddle(settings.WIDTH - 10 - settings.PADDLE_WIDTH, settings.HEIGHT // 2 - settings.PADDLE_HEIGHT // 2, settings.PADDLE_WIDTH, settings.PADDLE_HEIGHT)
    ball = Ball(settings.WIDTH // 2, settings.HEIGHT // 2, settings.BALL_RADIUS)

    # Initialize scores
    left_score = 0
    right_score = 0

    while run:
        # Control frame rate
        clock.tick(settings.FPS)  
        # Draw game elements
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)  

        # Handle quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Handle paddle movement
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        # Move the ball
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Check if a player scored
        if ball.x < 0 or ball.x > settings.WIDTH:
            if ball.x < 0:
                right_score += 1
            else:
                left_score += 1 
            
            # Reset ball and paddles after scoring
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
