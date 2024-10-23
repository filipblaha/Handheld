import pygame

# Inicializace Pygame
pygame.init()

# Velikost okna
width, height = 800, 600
window = pygame.display.set_mode((width, height))

# Barvy
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Nastavení FPS
clock = pygame.time.Clock()
fps = 60

# Nastavení hráče
player_size = 10
player_x, player_y = width // 2, height // 2
player_speed = 5

# Nastavení projektilu
bullet_size = 5
bullet_speed = 10
bullets = []
last_direction = None

# Načtení zvuku
shoot_sound = pygame.mixer.Sound('/Users/tomasfikart/Documents/3Rocnik/Handheld/Sounds/laser-shot-ingame-230500.mp3')

# Hlavní smyčka
running = True
while running:
    window.fill(black)

    # Zpracování vstupu
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_y -= player_speed
        last_direction = 'up'
    if keys[pygame.K_s]:
        player_y += player_speed
        last_direction = 'down'
    if keys[pygame.K_a]:
        player_x -= player_speed
        last_direction = 'left'
    if keys[pygame.K_d]:
        player_x += player_speed
        last_direction = 'right'

    # Střelba projektilu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and last_direction:
                # Přehraje se zvuk střely
                shoot_sound.play()

                # Vytvoření projektilu na základě posledního směru
                if last_direction == 'up':
                    bullets.append([player_x, player_y, 0, -bullet_speed])
                elif last_direction == 'down':
                    bullets.append([player_x, player_y, 0, bullet_speed])
                elif last_direction == 'left':
                    bullets.append([player_x, player_y, -bullet_speed, 0])
                elif last_direction == 'right':
                    bullets.append([player_x, player_y, bullet_speed, 0])

    # Aktualizace pozice projektilů
    for bullet in bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
        pygame.draw.rect(window, red, (bullet[0], bullet[1], bullet_size, bullet_size))

    # Vykreslení hráče
    pygame.draw.rect(window, white, (player_x, player_y, player_size, player_size))

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
