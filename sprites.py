import pygame
from assets import (
    create_surface_from_art,
    PLAYER_IDLE,
    PLAYER_DIVE_LEFT,
    PLAYER_DIVE_RIGHT,
    PLAYER_JUMP,
    BALL
)
from constants import *

class Goal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Surface covers the goal area + some buffer for posts
        self.image = pygame.Surface((GOAL_WIDTH + 20, GOAL_HEIGHT + 20), pygame.SRCALPHA)

        # Draw goal posts
        post_color = (200, 200, 200)
        post_width = 10

        # Relative coordinates on the surface
        # Left post
        pygame.draw.rect(self.image, post_color, (0, 0, post_width, GOAL_HEIGHT))
        # Right post
        pygame.draw.rect(self.image, post_color, (GOAL_WIDTH + 10, 0, post_width, GOAL_HEIGHT))
        # Top bar
        pygame.draw.rect(self.image, post_color, (0, 0, GOAL_WIDTH + 20, post_width))

        # Net pattern
        for x in range(0, GOAL_WIDTH + 20, 20):
             pygame.draw.line(self.image, (255, 255, 255, 50), (x, 0), (x, GOAL_HEIGHT), 1)
        for y in range(0, GOAL_HEIGHT, 20):
             pygame.draw.line(self.image, (255, 255, 255, 50), (0, y), (GOAL_WIDTH + 20, y), 1)

        self.rect = self.image.get_rect()
        # Align bottom of goal with ground
        self.rect.bottom = GROUND_Y
        self.rect.centerx = SCREEN_WIDTH // 2

class Ball(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, duration_ticks=1000, scale=4):
        super().__init__()
        self.image = create_surface_from_art(BALL, scale)
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.start_pos = pygame.math.Vector2(start_pos)
        self.target_pos = pygame.math.Vector2(target_pos)
        self.position = pygame.math.Vector2(start_pos)

        # Calculate velocity to reach target in duration_ticks
        # velocity is pixels per tick (ms) * frames?? No, update runs per frame.
        # Let's rely on frames for simplicity if FPS is constant, but tick-based is better.
        # Let's assume constant velocity vector calculated once.
        # We need speed = distance / total_frames.
        # But we are passed duration in ms (ticks).
        # We need to know FPS to convert duration to frames, OR use time delta.
        # Let's use simple frame-based calculation assuming 60 FPS for simplicity in this retro game.
        # duration_ticks / 1000 * 60 = total_frames
        total_frames = (duration_ticks / 1000.0) * 60
        if total_frames < 1: total_frames = 1

        self.velocity = (self.target_pos - self.start_pos) / total_frames

        # Scaling effect to simulate depth
        self.scale = scale
        self.base_image = self.image.copy()

    def update(self):
        self.position += self.velocity
        self.rect.center = (int(self.position.x), int(self.position.y))

        # Increase size as it gets closer (simulating 3D)
        # We determine progress based on Y coordinate relative to start/target?
        # Or just distance. Distance is safer.

        dist_total = (self.target_pos - self.start_pos).length()
        dist_current = (self.position - self.start_pos).length()

        if dist_total > 0:
            progress = dist_current / dist_total
            # Scale from 0.5x to 1.5x for example
            current_scale = 0.5 + (progress * 1.0)

            # This constant resizing might be expensive but let's try
            new_size = (int(self.base_image.get_width() * current_scale), int(self.base_image.get_height() * current_scale))
            self.image = pygame.transform.scale(self.base_image, new_size)
            # Update rect to keep center
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=10):
        super().__init__()
        self.scale = scale
        self.animations = {
            'idle': create_surface_from_art(PLAYER_IDLE, scale),
            'dive_left': create_surface_from_art(PLAYER_DIVE_LEFT, scale),
            'dive_right': create_surface_from_art(PLAYER_DIVE_RIGHT, scale),
            'jump': create_surface_from_art(PLAYER_JUMP, scale)
        }
        self.state = 'idle'
        self.image = self.animations[self.state]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

        self.vel_x = 0
        self.move_speed = 5

        # Cooldown for actions
        self.action_end_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()

        # Movement (only if idle)
        if self.state == 'idle':
            self.rect.x += self.vel_x

            # Clamp to goal area + padding
            if self.rect.left < GOAL_LEFT_X - 50:
                self.rect.left = GOAL_LEFT_X - 50
            if self.rect.right > GOAL_RIGHT_X + 50:
                self.rect.right = GOAL_RIGHT_X + 50

        # Return to idle if action time is over
        if self.state != 'idle' and current_time > self.action_end_time:
            self.state = 'idle'
            self.image = self.animations['idle']

            # Re-center rect based on current position, ensuring feet are on ground
            current_center_x = self.rect.centerx

            self.rect = self.image.get_rect()
            self.rect.midbottom = (current_center_x, GROUND_Y)

    def dive_left(self):
        if self.state == 'idle':
            self.state = 'dive_left'
            self.image = self.animations['dive_left']
            old_center_x = self.rect.centerx
            self.rect = self.image.get_rect()

            # Lunge to the left
            self.rect.midbottom = (old_center_x - 100, GROUND_Y)
            self.action_end_time = pygame.time.get_ticks() + 800

    def dive_right(self):
        if self.state == 'idle':
            self.state = 'dive_right'
            self.image = self.animations['dive_right']
            old_center_x = self.rect.centerx
            self.rect = self.image.get_rect()

            # Lunge to the right
            self.rect.midbottom = (old_center_x + 100, GROUND_Y)
            self.action_end_time = pygame.time.get_ticks() + 800

    def jump(self):
        if self.state == 'idle':
            self.state = 'jump'
            self.image = self.animations['jump']
            old_center_x = self.rect.centerx
            self.rect = self.image.get_rect()

            # Move up significantly
            self.rect.midbottom = (old_center_x, GROUND_Y - 120)
            self.action_end_time = pygame.time.get_ticks() + 800

    def duck(self):
        pass
