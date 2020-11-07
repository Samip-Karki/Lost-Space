import pygame
import sys
import random

pygame.init()


class SpaceShip(pygame.sprite.Sprite):

    def __init__(self, _path_charged, _path_uncharged, _x, _y):
        super().__init__()
        self._charged = pygame.image.load(_path_charged)
        self._uncharged = pygame.image.load(_path_uncharged)
        self.image = self._charged
        self.rect = self.image.get_rect(center=(_x, _y))
        self.shield_surface = pygame.image.load("assets/shield.png")
        self.health = 5

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_constrain()
        self.display_shield()

    def screen_constrain(self):
        if self.rect.right >= 1200:
            self.rect.right = 1200
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 710:
            self.rect.bottom = 710

    def display_shield(self):
        for _index, shield in enumerate(range(self.health)):
            screen.blit(self.shield_surface, (10 + _index * 40, 10))

    def get_damage(self):
        self.health -= 1

    def charged(self):
        self.image = self._charged

    def uncharged(self):
        self.image = self._uncharged


class Meteor(pygame.sprite.Sprite):
    def __init__(self, _path, _x, _y, x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load(_path)
        self.rect = self.image.get_rect(center=(_x, _y))
        self.x_sp = x_speed
        self.y_sp = y_speed

    def update(self):
        self.rect.centerx += self.x_sp
        self.rect.centery += self.y_sp
        if self.rect.centery >= 730:
            self.kill()


class Laser(pygame.sprite.Sprite):

    def __init__(self, _path, pos, speed):
        super().__init__()
        self.image = pygame.image.load(_path)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.centery <= 100:
            self.kill()


def main_game():
    global laser_charge
    laser_group.draw(screen)
    laser_group.update()

    ship_group.draw(screen)
    ship_group.update()

    meteor_group.draw(screen)
    meteor_group.update()

    # Collision
    if pygame.sprite.spritecollide(ship, meteor_group, True):
        ship.get_damage()
    for laser in laser_group:
        pygame.sprite.spritecollide(laser, meteor_group, True)

    # Laser
    if pygame.time.get_ticks() - laser_timer >= 700:
        laser_charge = True
        ship.charged()


def endgame():
    text = font.render("Game over", True, (255, 255, 255))
    screen.blit(text, (460, 355))


def display_score():
    text = font1.render(f'Score:{score}', True, (255, 255, 255))
    screen.blit(text, (1050, 0))


# Game variables
font = pygame.font.Font("assets/LazenbyCompSmooth.ttf", 50)
font1 = pygame.font.Font("assets/LazenbyCompSmooth.ttf", 30)
score = 0
laser_timer = 0
laser_charge = True

# Game screen
screen = pygame.display.set_mode((1200, 710))
pygame.display.set_caption("Lost Space")

# General Surfaces
ship = SpaceShip("assets/spaceship_charged.png", "assets/spaceship.png", 600, 350)
ship_group = pygame.sprite.Group()
ship_group.add(ship)

laser_group = pygame.sprite.Group()

SCORE_EVENT = pygame.USEREVENT
pygame.time.set_timer(SCORE_EVENT, 1000)

meteor_group = pygame.sprite.Group()
METEOR_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(METEOR_EVENT, 200)

# Clock
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and laser_charge:
            new_laser = Laser("assets/Laser.png", event.pos, 15)
            laser_group.add(new_laser)
            laser_timer = pygame.time.get_ticks()
            laser_charge = False
            ship.uncharged()

        if event.type == METEOR_EVENT:
            x = random.randrange(0, 1100)
            y = random.randrange(-600, -40)
            x_spd = random.randint(-1, 1)
            y_spd = random.randint(3, 10)
            path = random.choice([f'assets/Meteor{i}.png' for i in range(1, 4)])
            meteor = Meteor(path, x, y, x_spd, y_spd)
            meteor_group.add(meteor)

        if ship.health > 0 and event.type == SCORE_EVENT:
            score += 5

        if ship.health == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ship.health = 5
                    score = 0
                    meteor_group.empty()

    screen.fill((42, 45, 51))

    if ship.health > 0:
        main_game()
        display_score()
    else:
        endgame()
        display_score()

    pygame.display.update()
    clock.tick(90)
