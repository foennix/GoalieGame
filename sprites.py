import pygame
from assets import (
    create_surface_from_art,
    PLAYER_IDLE,
    PLAYER_DIVE_LEFT,
    PLAYER_DIVE_RIGHT,
    PLAYER_JUMP,
    BALL
)

class Goal(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((screen_width - 100, screen_height - 100), pygame.SRCALPHA)

        # Draw goal posts
        post_color = (200, 200, 200)
        post_width = 10

        # Left post
        pygame.draw.rect(self.image, post_color, (0, 0, post_width, self.image.get_height()))
        # Right post
        pygame.draw.rect(self.image, post_color, (self.image.get_width() - post_width, 0, post_width, self.image.get_height()))
        # Top bar
        pygame.draw.rect(self.image, post_color, (0, 0, self.image.get_width(), post_width))

        # Net pattern
        for x in range(0, self.image.get_width(), 20):
             pygame.draw.line(self.image, (255, 255, 255, 50), (x, 0), (x, self.image.get_height()), 1)
        for y in range(0, self.image.get_height(), 20):
             pygame.draw.line(self.image, (255, 255, 255, 50), (0, y), (self.image.get_width(), y), 1)

        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)

class Ball(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, speed=5, scale=4):
        super().__init__()
        self.image = create_surface_from_art(BALL, scale)
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        self.start_pos = pygame.math.Vector2(start_pos)
        self.target_pos = pygame.math.Vector2(target_pos)
        self.position = pygame.math.Vector2(start_pos)

        direction = self.target_pos - self.start_pos
        if direction.length() > 0:
            direction = direction.normalize()
        self.velocity = direction * speed

        # Scaling effect to simulate depth
        self.scale = scale
        self.base_image = self.image.copy()

    def update(self):
        self.position += self.velocity
        self.rect.center = (int(self.position.x), int(self.position.y))

        # Increase size as it gets closer (simulating 3D)
        # Assuming moving from top (far) to bottom (near)??
        # Wait, if we are the goalie, the ball comes FROM the kicker (far) TO us (near/goal).
        # So it should get bigger.

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
    def __init__(self, x, y, scale=5):
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
        self.original_x = x
        self.original_y = y

        # Cooldown for actions
        self.action_end_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()

        # Return to idle if action time is over
        if self.state != 'idle' and current_time > self.action_end_time:
            self.state = 'idle'
            self.image = self.animations['idle']
            # Re-center rect but keep bottom position
            bottom = self.rect.bottom
            self.rect = self.image.get_rect()
            self.rect.midbottom = (self.original_x, bottom)

    def dive_left(self):
        if self.state == 'idle':
            self.state = 'dive_left'
            self.image = self.animations['dive_left']
            self.rect = self.image.get_rect()
            # Position the dive to the left of the center
            self.rect.bottomright = (self.original_x, self.original_y)
            self.action_end_time = pygame.time.get_ticks() + 1000 # 1 second action

    def dive_right(self):
        if self.state == 'idle':
            self.state = 'dive_right'
            self.image = self.animations['dive_right']
            self.rect = self.image.get_rect()
            # Position the dive to the right of the center
            self.rect.bottomleft = (self.original_x, self.original_y)
            self.action_end_time = pygame.time.get_ticks() + 1000

    def jump(self):
        if self.state == 'idle':
            self.state = 'jump'
            self.image = self.animations['jump']
            self.rect = self.image.get_rect()
            self.rect.midbottom = (self.original_x, self.original_y)
            self.action_end_time = pygame.time.get_ticks() + 1000

    def duck(self):
        # For now, duck just keeps us idle but maybe we can add a 'ready' state
        # Or maybe it cancels a dive early?
        pass
