import pygame
import random
import sys
import os
import json
from sprites import Player, Ball, Goal

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BG_COLOR = (34, 139, 34) # Grass Green
HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    try:
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, 'r') as f:
                return int(f.read().strip())
    except Exception:
        pass
    return 0

def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, 'w') as f:
            f.write(str(score))
    except Exception:
        pass

def draw_text(screen, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Neuer: The Goalkeeper Game")
    clock = pygame.time.Clock()

    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    balls = pygame.sprite.Group()

    # Create Goal (Background)
    goal = Goal(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites.add(goal)

    # Create Player (Foreground)
    # Position player at bottom center
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
    all_sprites.add(player)

    # Gameplay variables
    score = 0
    highscore = load_highscore()
    lives = 3
    base_speed = 3
    game_active = True

    ball_spawn_delay = 2000 # 2 seconds initially
    last_spawn_time = pygame.time.get_ticks()

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_active:
                    if event.key == pygame.K_LEFT:
                        player.dive_left()
                    elif event.key == pygame.K_RIGHT:
                        player.dive_right()
                    elif event.key == pygame.K_UP:
                        player.jump()
                    elif event.key == pygame.K_DOWN:
                        player.duck()
                else:
                    if event.key == pygame.K_SPACE:
                        # Reset Game
                        score = 0
                        lives = 3
                        base_speed = 3
                        game_active = True
                        balls.empty()
                        all_sprites.empty()
                        all_sprites.add(goal)
                        all_sprites.add(player)
                        last_spawn_time = current_time

        if game_active:
            # Spawn Balls
            if current_time - last_spawn_time > ball_spawn_delay:
                # Spawn a ball
                start_x = SCREEN_WIDTH // 2
                start_y = SCREEN_HEIGHT // 2 + 60

                target_x = random.randint(100 + 20, SCREEN_WIDTH - 100 - 20)
                target_y = SCREEN_HEIGHT - 50

                ball = Ball((start_x, start_y), (target_x, target_y), speed=base_speed)
                balls.add(ball)
                all_sprites.add(ball)

                last_spawn_time = current_time
                ball_spawn_delay = random.randint(1500, 2500)

            # 2. Update
            all_sprites.update()

            # Collision Detection
            hits = pygame.sprite.spritecollide(player, balls, True, pygame.sprite.collide_mask)
            if hits:
                score += 100
                print(f"SAVE! Score: {score}")
                if score % 500 == 0:
                    base_speed += 1
                    print("Level Up! Ball speed increased.")

            for ball in balls:
                if ball.rect.top > SCREEN_HEIGHT:
                    ball.kill()
                    lives -= 1
                    print(f"GOAL! Lives left: {lives}")
                    if lives <= 0:
                        game_active = False

        # 3. Draw
        screen.fill(BG_COLOR)

        # Draw the "Penalty Box" or field lines to give perspective
        # Top line
        pygame.draw.line(screen, (255, 255, 255), (0, SCREEN_HEIGHT//2 + 50), (SCREEN_WIDTH, SCREEN_HEIGHT//2 + 50), 2)
        # Side lines
        pygame.draw.line(screen, (255, 255, 255), (100, SCREEN_HEIGHT), (250, SCREEN_HEIGHT//2 + 50), 2)
        pygame.draw.line(screen, (255, 255, 255), (SCREEN_WIDTH - 100, SCREEN_HEIGHT), (SCREEN_WIDTH - 250, SCREEN_HEIGHT//2 + 50), 2)

        all_sprites.draw(screen)

        # UI
        draw_text(screen, f"Score: {score}", 30, SCREEN_WIDTH // 2, 10)
        draw_text(screen, f"Lives: {lives}", 30, SCREEN_WIDTH - 100, 10)
        draw_text(screen, f"High Score: {highscore}", 30, 100, 10)

        if not game_active:
            if score > highscore:
                highscore = score
                save_highscore(highscore)

            draw_text(screen, "GAME OVER", 100, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, (255, 0, 0))
            draw_text(screen, f"Final Score: {score}", 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            draw_text(screen, "Press SPACE to Play Again", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
