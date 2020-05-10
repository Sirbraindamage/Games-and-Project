# explosion and laser sound fx created by Dklon on OpenGameArt.com
# Art created by Aztrakatze on itch.io
#
import random
import math
import pygame as py
from PlayerSprite import *

WIDTH = 800
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
py.init()
py.mixer.init()
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Dimensional Drifter")
clock = py.time.Clock()
# load background image
background = py.image.load(path.join(img_dir, "bg1.png")).convert()
background_rect = background.get_rect()

# allow for spawning of mob in one line instead of 3 lines
def NewNPC():
    n = NPC(player)
    all_sprites.add(n)
    NPCs.add(n)


def show_go_screen():
    draw_text(screen, "Dimensional Drifter!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "W,A,S,D keys to move, Click mouse 1 to fire", 18,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    py.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
            if event.type == py.KEYUP:
                waiting = False

# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = py.sprite.Group()
        NPCs = py.sprite.Group()
        bullets = py.sprite.Group()
        powerups = py.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(15):
            NewNPC()

        score = 0

    # keep loop running at the right speed
    clock.tick(FPS)

    for event in py.event.get():
        # check for closing window
        if event.type == py.QUIT:
            running = False
        elif event.type == py.MOUSEBUTTONDOWN:
            if event.button == 1:
                New_bullet = player.Shoot()
                all_sprites.add(New_bullet)
                bullets.add(New_bullet)
                laser_sound.play()

    # Update
    all_sprites.update()
    # check if there a collision between the bullet and NPC
    hits = py.sprite.groupcollide(NPCs, bullets, True, True, py.sprite.collide_circle)
    for hit in hits:
        score += 15
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        NewNPC()

    # check if there a collision between the player and NPC
    hits = py.sprite.spritecollide(player, NPCs, True, py.sprite.collide_circle)
    for hit in hits:
        player.health -= 15
        score -= 30
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        NewNPC()

        if player.health <= 0:
            Gamer_over = True

    # updates the position of of mouse and rotates it towards the mouse position
    mouse_x, mouse_y = py.mouse.get_pos()
    player.rotate(mouse_x, mouse_y)

    # render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 24, WIDTH / 2, 10)
    draw_health_bar(screen, 5, 5, player.health)
    # flip the display
    py.display.flip()

py.quit()
