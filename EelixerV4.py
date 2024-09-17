import pygame
import random
import os
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eelixer Of Life Clean Water Quest V4")

# Load images
current_dir = os.path.dirname(__file__)
img_dir = os.path.join(current_dir, "sprites")

def load_image(name):
    return pygame.image.load(os.path.join(img_dir, name)).convert_alpha()

eel_img_right = load_image("eel.png")
eel_img_right = pygame.transform.scale(eel_img_right, (80, 40))
eel_img_left = pygame.transform.flip(eel_img_right, True, False)

background = pygame.image.load(os.path.join(img_dir, "sea.jpg")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load rubbish sprites
rubbish_images = {
    "bottle": load_image("plastic_bottle.png"),
    "can": load_image("can.png"),
    "bag": load_image("plastic_bag.png"),
    "tire": load_image("tires.png")
}

# Scale rubbish images
for key in ["bottle", "can", "bag"]:
    rubbish_images[key] = pygame.transform.scale(rubbish_images[key], (30, 30))
rubbish_images["tire"] = pygame.transform.scale(rubbish_images["tire"], (60, 60))

fish_img = load_image("fish.png")
fish_img = pygame.transform.scale(fish_img, (40, 40))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load icons
edible_icons = {
    "bottle": pygame.transform.scale(rubbish_images["bottle"], (40, 40)),
    "can": pygame.transform.scale(rubbish_images["can"], (40, 40)),
    "bag": pygame.transform.scale(rubbish_images["bag"], (40, 40))
}

dangerous_fish_icon = pygame.transform.scale(fish_img, (50, 50))

# Eel class
class Eel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = eel_img_right
        self.image_left = eel_img_left
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 9
        self.health = 100
        self.direction = "right"

    def update(self):
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = "left"
            moved = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = "right"
            moved = True
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            moved = True
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            moved = True

        if moved:
            self.image = self.image_left if self.direction == "left" else self.image_right

        # Keep eel on screen
        self.rect.clamp_ip(screen.get_rect())

# Rubbish class
class Rubbish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(list(rubbish_images.keys()))
        self.image = rubbish_images.get(self.type)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

# Fish class
class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = fish_img
        self.image_left = pygame.transform.flip(fish_img, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.uniform(0.5, 1.5)
        self.direction = random.choice([-1, 1])
        self.damage = random.randint(5, 7)  # Random damage value for each fish

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.direction > 0:
            self.image = self.image_right
        else:
            self.image = self.image_left

        if self.rect.right > WIDTH or self.rect.left < 0:
            self.direction *= -1
            self.rect.y += random.randint(-30, 30)
            self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

# Jellyfish class
class Jellyfish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(load_image("jellyfish.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = 1.5
        self.angle = random.uniform(0, 2 * math.pi)
        self.damage = 15

    def update(self):
        # Move jellyfish in erratic manner
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)

        # Bounce off screen edges
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.angle = math.pi - self.angle
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.angle = -self.angle

        # Adjust angle randomly
        self.angle += random.uniform(-0.05, 0.05)

# Shark class
class Shark(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = pygame.transform.scale(load_image("shark.png"), (100, 50))
        self.image_left = pygame.transform.flip(self.image_right, True, False)  # Flip the shark for left direction
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = 0.9  
        self.damage = 30

    def update(self):
        # Move shark horizontally and vertically toward the eel
        if self.rect.x < eel.rect.x:
            self.rect.x += self.speed
            self.image = self.image_right  # Face right
        if self.rect.x > eel.rect.x:
            self.rect.x -= self.speed
            self.image = self.image_left  # Face left
        if self.rect.y < eel.rect.y:
            self.rect.y += self.speed
        if self.rect.y > eel.rect.y:
            self.rect.y -= self.speed

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Informational popups
popups = [
    "Eels are fascinating creatures! They can breathe through their skin and some species can produce electricity.",
    "Pollution harms marine life. Plastic waste can be mistaken for food, causing health issues for sea creatures.",
    "You can help protect eels and other marine life by reducing plastic use and properly disposing of waste."
]

# Introduction texts
intro_texts = [
    "Welcome to Eelixer of Life!",
    "You are a mutated eel that eats rubbish.",
    "Collect rubbish to gain score to clean up the ocean .",
    "Use arrow keys to navigate and avoid enemies.",
    "Good luck on your underwater adventure!"
]

def show_popup(surface, text, size=30):
    popup_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    popup_surface.blit(background, (0, 0))
    popup_rect = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 200)
    pygame.draw.rect(popup_surface, WHITE, popup_rect)
    pygame.draw.rect(popup_surface, BLACK, popup_rect, 3)

    font = pygame.font.Font(None, size)
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] < popup_rect.width - 20:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))

    y = popup_rect.top + 20
    for line in lines:
        text_surface = font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(centerx=popup_rect.centerx, top=y)
        popup_surface.blit(text_surface, text_rect)
        y += text_rect.height + 5

    surface.blit(popup_surface, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def show_instructions():
    show_popup(screen, '\n'.join(intro_texts), size=24)

def reset_game():
    global eel, all_sprites, rubbish_group, fish_group, jellyfish_group, shark_group, score, game_over
    all_sprites = pygame.sprite.Group()
    rubbish_group = pygame.sprite.Group()
    fish_group = pygame.sprite.Group()
    jellyfish_group = pygame.sprite.Group()
    shark_group = pygame.sprite.Group()

    eel = Eel()
    all_sprites.add(eel)

    for _ in range(10):
        rubbish = Rubbish()
        all_sprites.add(rubbish)
        rubbish_group.add(rubbish)

    for _ in range(5):
        fish = Fish()
        all_sprites.add(fish)
        fish_group.add(fish)

    score = 0
    game_over = False

def update_enemy_spawns():
    global score
    if score >= 95 and len(jellyfish_group) < 5:
        if random.randint(0, 120) == 0:  # Adjust spawn rate as needed
            new_jellyfish = Jellyfish()
            all_sprites.add(new_jellyfish)
            jellyfish_group.add(new_jellyfish)

    if score >= 175 and len(shark_group) < 1:
        if random.randint(0, 120) == 0:  # Adjust spawn rate as needed
            new_shark = Shark()
            all_sprites.add(new_shark)
            shark_group.add(new_shark)

# Set up the game
clock = pygame.time.Clock()
reset_game()

restart_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 100, 100, 50, "Restart", GREEN, BLACK)

# Show instructions at the beginning
show_instructions()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_button.is_clicked(event.pos):
                reset_game()
                show_instructions()

    if not game_over:
        # Update
        all_sprites.update()

        # Adjust fish, jellyfish, and shark spawning based on score
        update_enemy_spawns()

        # Check collisions
        rubbish_collected = pygame.sprite.spritecollide(eel, rubbish_group, True)
        for rubbish in rubbish_collected:
            if rubbish.type == "tire":
                score += 3
            else:
                score += 1
            new_rubbish = Rubbish()
            all_sprites.add(new_rubbish)
            rubbish_group.add(new_rubbish)

        fish_collided = pygame.sprite.spritecollide(eel, fish_group, False)
        if fish_collided:
            for fish in fish_collided:
                eel.health -= fish.damage
                fish.kill()
                new_fish = Fish()
                all_sprites.add(new_fish)
                fish_group.add(new_fish)

            if eel.health <= 0:
                eel.health = 0  # Ensure health doesn't go below zero
                game_over = True
                show_popup(screen, random.choice(popups))

        jellyfish_collided = pygame.sprite.spritecollide(eel, jellyfish_group, False)
        if jellyfish_collided:
            for jellyfish in jellyfish_collided:
                eel.health -= jellyfish.damage
                if eel.health <= 0:
                    eel.health = 0  # Ensure health doesn't go below zero
                    game_over = True
                    show_popup(screen, random.choice(popups))
                jellyfish.kill()

        shark_collided = pygame.sprite.spritecollide(eel, shark_group, False)
        if shark_collided:
            eel.health -= shark_collided[0].damage
            if eel.health <= 0:
                eel.health = 0  # Ensure health doesn't go below zero
                game_over = True
                show_popup(screen, random.choice(popups))
            shark_collided[0].kill()

        # Draw
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        # Display score and health bar
        font = pygame.font.Font(None, 36)

        # Draw health bar on the left
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = 10
        health_bar_y = 50
        pygame.draw.rect(screen, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
        pygame.draw.rect(screen, GREEN, (health_bar_x, health_bar_y, (eel.health / 100) * health_bar_width, health_bar_height))
        health_text = font.render(f"Health: {eel.health}", True, WHITE)
        screen.blit(health_text, (health_bar_x, health_bar_y - 30))

        # Draw score bar on the right
        score_text = font.render(f"Score: {score}", True, WHITE)
        score_text_rect = score_text.get_rect(right=WIDTH - 10, top=10)
        screen.blit(score_text, score_text_rect)

    else:
        # Game over screen with background
        screen.blit(background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over", True, RED)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
        screen.blit(score_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
        restart_button.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
