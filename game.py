import pygame
import random

pygame.init()
pygame.mixer.init()

# Screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Game")

# Music & Sound
pygame.mixer.music.load("sounds/background.mp3")
pygame.mixer.music.play(-1)
crash_sound = pygame.mixer.Sound("sounds/crash.wav")

# Clock & Fonts
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)
score_font = pygame.font.SysFont(None, 36)

# Player
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 5

player_img = pygame.image.load("images/player.png")
player_img = pygame.transform.scale(player_img, (player_width, player_height))

# Enemies
enemy_width = 50
enemy_height = 50
enemy_speed = 4
enemy_count = 2

enemy_img = pygame.image.load("images/enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))
# Background
bg_img = pygame.image.load("images/space_bg.jpg")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))


enemies = []
for _ in range(enemy_count):
    x = random.randint(0, WIDTH - enemy_width)
    y = random.randint(-600, -50)
    enemies.append([x, y])

# Game state
score = 0
game_over = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                game_over = False
                score = 0
                enemy_speed = 4
                player_x = WIDTH // 2 - player_width // 2

                enemies.clear()
                for _ in range(enemy_count):
                    x = random.randint(0, WIDTH - enemy_width)
                    y = random.randint(-600, -50)
                    enemies.append([x, y])

                pygame.mixer.music.play(-1)

    screen.blit(bg_img, (0, 0))


    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        if player_x < 0:
            player_x = 0
        if player_x > WIDTH - player_width:
            player_x = WIDTH - player_width

        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > HEIGHT:
                enemy[1] = -enemy_height
                enemy[0] = random.randint(0, WIDTH - enemy_width)
                score += 1
                enemy_speed += 0.2

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
        if player_rect.colliderect(enemy_rect):
            crash_sound.play()
            pygame.mixer.music.stop()
            game_over = True

    # Draw sprites
    screen.blit(player_img, (player_x, player_y))
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))

    # Score
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Game over text
    if game_over:
        wasted_text = font.render("WASTED", True, (255, 255, 255))
        restart_text = score_font.render("[R] Go again", True, (200, 200, 200))

        screen.blit(wasted_text, (WIDTH // 2 - 120, HEIGHT // 2 - 40))
        screen.blit(restart_text, (WIDTH // 2 - 110, HEIGHT // 2 + 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
