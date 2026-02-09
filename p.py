import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SKY_BLUE = (135, 206, 235)
BUILDING_COLOR = (80, 80, 90)
WINDOW_COLOR = (255, 255, 200)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cheryl and Brett's Cat Adventure")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)
title_font = pygame.font.SysFont("Arial", 60, bold=True)

class Heart(pygame.sprite.Sprite):
    """Simple heart animation that floats up and fades."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # Draw a simple 8-bit heart
        color = (255, 50, 50)
        pygame.draw.rect(self.image, color, (4, 0, 4, 4))
        pygame.draw.rect(self.image, color, (12, 0, 4, 4))
        pygame.draw.rect(self.image, color, (0, 4, 20, 8))
        pygame.draw.rect(self.image, color, (4, 12, 12, 4))
        pygame.draw.rect(self.image, color, (8, 16, 4, 4))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.alpha = 255
        self.speed_y = -2

    def update(self, scroll_speed):
        self.rect.y += self.speed_y
        self.rect.x -= scroll_speed
        self.alpha -= 5  # Fade effect
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(self.alpha)

class Cat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((35, 25), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        # (Same drawing logic as previous response)
        BODY_COLOR = (255, 140, 0)
        pygame.draw.rect(self.image, BODY_COLOR, (5, 10, 20, 12))
        pygame.draw.rect(self.image, BODY_COLOR, (20, 5, 10, 10))
        pygame.draw.rect(self.image, (0,0,0), (22, 6, 2, 2))
        pygame.draw.rect(self.image, (0,0,0), (27, 6, 2, 2))

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        if self.rect.right < 0: self.kill()

class Building(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.stories = random.choice([4, 5])
        self.image = pygame.Surface((180, self.stories * 100))
        self.image.fill(BUILDING_COLOR)
        for s in range(self.stories):
            win_y = 20 + (s * 90)
            pygame.draw.rect(self.image, WINDOW_COLOR, (30, win_y, 40, 50))
            pygame.draw.rect(self.image, WINDOW_COLOR, (110, win_y, 40, 50))
        self.rect = self.image.get_rect(bottomleft=(x, SCREEN_HEIGHT))

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        if self.rect.right < 0: self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.cheryl_img = pygame.image.load("cheryl.png").convert_alpha()
            self.cheryl_img = pygame.transform.scale(self.cheryl_img, (64, 64))

            self.brett_img = pygame.image.load("brett.png").convert_alpha()
            self.brett_img = pygame.transform.scale(self.brett_img, (64, 64))
        except:
            self.brett_img = pygame.Surface((64, 64)); self.brett_img.fill((0,255,0))
            self.cheryl_img = pygame.Surface((64, 64)); self.cheryl_img.fill((255,0,255))
        self.image = self.cheryl_img
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_y = 0
        self.is_cheryl = True
        self.score = 0

    def toggle_character(self):
        self.is_cheryl = not self.is_cheryl
        self.image = self.cheryl_img if self.is_cheryl else self.brett_img

    def update(self):
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0

# --- Game Functions ---
def show_intro():
    screen.fill(SKY_BLUE)
    title_text = title_font.render("Cheryl and Brett's Cat Adventure", True, (0, 0, 0))
    start_text = font.render("Press SPACE to Start", True, (50, 50, 50))
    instruct_text = font.render("Arrows to move, Space to jump, C to swap", True, (80, 80, 80))
    
    screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 150))
    screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 300))
    screen.blit(instruct_text, (SCREEN_WIDTH//2 - instruct_text.get_width()//2, 400))
    pygame.display.flip()

# Groups
buildings = pygame.sprite.Group()
cats = pygame.sprite.Group()
hearts = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle(Player(100, SCREEN_HEIGHT - 100))

def spawn_building(x_pos):
    b = Building(x_pos)
    buildings.add(b)
    win_x = b.rect.x + random.choice([50, 130])
    win_y = b.rect.top + (random.randint(0, b.stories - 1) * 90) + 45
    cats.add(Cat(win_x, win_y))

# Initial buildings
for i in range(3): spawn_building(400 + (i * 300))

# --- Main Loop ---
state = "INTRO"
running = True

while running:
    if state == "INTRO":
        show_intro()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = "PLAYING"
    
    elif state == "PLAYING":
        screen.fill(SKY_BLUE)
        scroll_speed = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: player_group.sprite.toggle_character()
                if event.key == pygame.K_SPACE and player_group.sprite.rect.bottom >= SCREEN_HEIGHT:
                    player_group.sprite.vel_y = -35

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]: scroll_speed = 5
        
        # Update
        player_group.update()
        buildings.update(scroll_speed)
        cats.update(scroll_speed)
        hearts.update(scroll_speed)

        # Collision & Heart Spawning
        collided_cats = pygame.sprite.spritecollide(player_group.sprite, cats, True)
        for cat in collided_cats:
            player_group.sprite.score += 1
            hearts.add(Heart(cat.rect.centerx, cat.rect.centery))

        if len(buildings) < 4:
            last_b = max([b.rect.right for b in buildings])
            spawn_building(last_b + 120)

        # Draw
        buildings.draw(screen)
        cats.draw(screen)
        hearts.draw(screen)
        player_group.draw(screen)
        
        score_text = font.render(f"Cats Petted: {player_group.sprite.score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()