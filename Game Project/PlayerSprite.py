import pygame as py
import math
import random
from os import path

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
# initializes sound
py.mixer.init()

# import images and sounds from files
img_dir = path.join(path.dirname(__file__), 'Img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# load images
player_img = py.image.load(path.join(img_dir, "Playeridle1.png"))
bullet_img = py.image.load(path.join(img_dir, "Energyball.png"))
# below add three different types of drones to a list
NPC_images = []
NPC_list = ['drone1.png', 'drone2.png', 'drone3.png']
for img in NPC_list:
    NPC_images.append(py.image.load(path.join(img_dir, img)))

# load the Explosion images with a loop, scales them down then load it into list
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
for i in range(12):
    filename = 'Explosion_{}.png'.format(i)
    img = py.image.load(path.join(img_dir, filename))
    img.set_colorkey(BLACK)
    img_lg = py.transform.scale(img, (75, 75))
    expl_anim['lg'].append(img_lg)
    img_sm = py.transform.scale(img, (15, 15))
    expl_anim['sm'].append(img_sm)

powerup_anim = {}
powerup_anim['HP'] = []
for i in range(4):
    filename = "Health_{}.png".format(i)
    img = py.image.load(path.join(img_dir, filename))
    img_HP = py.transform.scale(img, (16, 16))
    powerup_anim['HP'].append(img_HP)

# load sounds
laser_sound = py.mixer.Sound(path.join(snd_dir, "laser7.wav"))
expl_sounds = []
for snd in ['boom8.wav', 'boom9.wav']:
    expl_sounds.append(py.mixer.Sound(path.join(snd_dir, snd)))

# define font made general to work on all devices
font_name = py.font.match_font('arial')


# function to draw text on screen
def draw_text(surf, text, size, x, y):
    font = py.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_health_bar(surf, x, y, pct, ):
    if pct < 0:
        pct = 0
    Bar_length = 100
    Bar_height = 10
    fill = (pct / 100) * Bar_length
    outline_rect = py.Rect(x, y, Bar_length, Bar_height)
    fill_rect = py.Rect(x, y, fill, Bar_height)
    py.draw.rect(surf, GREEN, fill_rect)
    py.draw.rect(surf, WHITE, outline_rect, 2)


class Player(py.sprite.Sprite):
    def __init__(self):
        py.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.radius = 22
        # py.draw.circle(self.image, RED, self.rect.center,self.radius )
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT / 2
        self.Yspeed = 0
        self.rotatableimage = self.image
        self.health = 100

    def update(self):
        self.Xspeed = 0
        self.Yspeed = 0
        # line below allow for key press to equate to move of sprite
        keypreesed = py.key.get_pressed()
        if keypreesed[py.K_a]:
            self.Xspeed = - 11
        if keypreesed[py.K_d]:
            self.Xspeed = 11
        if keypreesed[py.K_w]:
            self.Yspeed = - 11
        if keypreesed[py.K_s]:
            self.Yspeed = 11
        self.rect.x += self.Xspeed
        self.rect.y += self.Yspeed
        # line below allow the sprite to wrap around the screen
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.top = 0
        if self.rect.bottom < 0:
            self.rect.bottom = HEIGHT

    def rotate(self, mouse_x, mouse_y):
        rel_x = mouse_x - self.rect.x
        rel_y = mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        self.image = py.transform.rotate(self.rotatableimage, int(angle))
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
        return

    def Shoot(self):
        pos = self.rect.centerx, self.rect.centery
        mpos = py.mouse.get_pos()
        direction = py.math.Vector2(mpos[0] - pos[0], mpos[1] - pos[1])
        direction.scale_to_length(10)
        return Bullet(pos[0], pos[1], round(direction[0]), round(direction[1]))


class NPC(py.sprite.Sprite):
    def __init__(self, player):
        py.sprite.Sprite.__init__(self)
        self.player = player
        self.image = random.choice(NPC_images)  # this randomises the drones from the NPC_images list
        self.originalimage = self.image
        self.rect = self.image.get_rect()
        self.radius = 18
        # py.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.spawn()

    # allows of spawning from all four side of the screen and set the x, y speed and spawn position
    def spawn(self):
        self.direction = random.randrange(4)
        if self.direction == 0:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.Xspeed = random.randrange(-2, 2)
            self.Yspeed = random.randrange(4, 8)
        elif self.direction == 1:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(HEIGHT, HEIGHT + 60)
            self.Xspeed = random.randrange(-2, 2)
            self.Yspeed = -random.randrange(4, 8)
        elif self.direction == 2:
            self.rect.x = random.randrange(-100, -40)
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.Xspeed = random.randrange(4, 8)
            self.Yspeed = random.randrange(-2, 2)
        elif self.direction == 3:
            self.rect.x = random.randrange(WIDTH, WIDTH + 60)
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.Xspeed = -random.randrange(4, 8)
            self.Yspeed = random.randrange(-2, 2)

    def update(self):
        self.rect.x += self.Xspeed
        self.rect.y += self.Yspeed
        # makes it so that NPC point to wards the player as it passes from side to side
        dir_x, dir_y = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
        self.rot = (180 / math.pi) * math.atan2(-dir_x, -dir_y)
        self.image = py.transform.rotate(self.originalimage, self.rot)
        # Respawns the NPC when they hit an side
        if self.direction == 0:
            if self.rect.top > HEIGHT + 10:
                self.spawn()
        elif self.direction == 1:
            if self.rect.bottom < -10:
                self.spawn()
        elif self.direction == 2:
            if self.rect.left > WIDTH + 10:
                self.spawn()
        elif self.direction == 3:
            if self.rect.right < -10:
                self.spawn()


class Bullet(py.sprite.Sprite):
    def __init__(self, x, y, Xspeed, Yspeed):
        py.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.radius = 9
        # py.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.bottom = y
        self.rect.centerx = x
        self.Xspeed = Xspeed
        self.Yspeed = Yspeed

    def update(self):
        self.rect.x += self.Xspeed
        self.rect.y += self.Yspeed
        # kill if moved of screen
        if self.rect.bottom > HEIGHT + 20 or self.rect.top < -20:
            self.kill()
        if self.rect.right > WIDTH + 20 or self.rect.left < -20:
            self.kill()


class Pow(py.sprite.Sprite):
    def __init__(self, center):
        py.sprite.Sprite.__init__(self)
        self.image = powerup_anim['HP']
        self.rect = self.image.get_rect()
        self.rect.center = center
        # py.draw.circle(self.image, RED, self.rect.center, self.radius)

    def update(self):
        # kill if moved of screen
        if self.rect.bottom > HEIGHT + 20 or self.rect.top < -20:
            self.kill()
        if self.rect.right > WIDTH + 20 or self.rect.left < -20:
            self.kill()


class Explosion(py.sprite.Sprite):
    def __init__(self, center, size, ):
        py.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = py.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = py.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = expl_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
