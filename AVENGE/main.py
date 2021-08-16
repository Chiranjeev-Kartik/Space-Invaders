"""
Author: Kartikay Chiranjeev Gupta
Last Modified: 8/16/2021
"""

import pygame
from pygame.locals import *
import os
import sys
from itertools import cycle
import random
from pygame import mixer

# Setting Display.......................................................................................................


pygame.init()
pygame.mixer.init()
pygame.font.init()
WIDTH, HEIGHT = 1180, 670
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AVENGE - A SPACE INVADERS GAME')
FPS = 60  # Frames per second.
DIFFICULTY = 3  # Frequency of Shoots per second.
GOON_STEPS = 20  # To Set Distance between each goon.
GOON_X_OFFSET = 102  # For deploying goons on screen.
GOON_Y_OFFSET = 125  # For deploying goons on screen.
GOON_HEALTH = 10  # Goon Health.
HERO_HEALTH = 1000  # Player Health.
HEALTH_REWARD = 100  # Health Reward for player after each level.
GOON_DAMAGE = 10  # Damage of Goons laser.
HERO_DAMAGE = 20  # Damage of Player laser.
VILLAIN_DAMAGE = 50  # Damage of Villain laser.
VILLAIN_HEALTH = 500  # Villains Health.
ENEMY_LASERS = []  # Contains all Enemy's Lasers.
HERO_LASERS = []  # Contains all Player's Lasers.
COOL_DOWN = 300  # Cool down Threshold.
LASER_VEL = 5  # Velocity of laser.
SHOOT_OFFSET = 92  # Tune Laser position.
H_VEL = 5  # Player Horizontal movement velocity.
V_VEL = 5  # Player vertical movement velocity.
OPTIMIZATION = 20  # To Tune Goon movement.
DOWN_SPEED = 0.1  # Velocity of enemies moving down.

# Load all Images.......................................................................................................

HERO_1 = pygame.image.load(os.path.join('assets', 'Hero_1.png'))
HERO_2 = pygame.image.load(os.path.join('assets', 'Hero_2.png'))
HERO_3 = pygame.image.load(os.path.join('assets', 'Hero_3.png'))
HERO_4 = pygame.image.load(os.path.join('assets', 'Hero_4.png'))
VILLAIN_1 = pygame.image.load(os.path.join('assets', 'Villain_1.png'))
VILLAIN_2 = pygame.image.load(os.path.join('assets', 'Villain_2.png'))
VILLAIN_3 = pygame.image.load(os.path.join('assets', 'Villain_3.png'))
GOON = pygame.image.load(os.path.join('assets', 'Goon.png'))
LASER_HERO = pygame.image.load(os.path.join('assets', 'Laser_Hero.png'))
LASER_VILLAIN = pygame.image.load(os.path.join('assets', 'Laser_Villain.png'))
LASER_GOON = pygame.image.load(os.path.join('assets', 'Laser_Goon.png'))
BACKGROUND = pygame.image.load(os.path.join('assets', 'Space.jpg'))
# Load all sounds.......................................................................................................
HERO_SHOOT_SOUND = mixer.Sound(os.path.join('assets', 'Sounds', 'Hero_shoot.mp3'))
GOON_SHOOT_SOUND = mixer.Sound(os.path.join('assets', 'Sounds', 'Goon_shoot.mp3'))
VILLAIN1_SHOOT_SOUND = mixer.Sound(os.path.join('assets', 'Sounds', 'Villain_1_shoot.mp3'))
VILLAIN2_SHOOT_SOUND = mixer.Sound(os.path.join('assets', 'Sounds', 'Villain_2_shoot.mp3'))
VILLAIN3_SHOOT_SOUND = mixer.Sound(os.path.join('assets', 'Sounds', 'Villain_3_shoot.mp3'))
EXPLODE_SOUND = mixer.Sound(os.path.join('assets', 'Sounds', 'Explode.mp3'))
BURNOUT = mixer.Sound(os.path.join('assets', 'Sounds', 'Burnout.mp3'))
WIN = mixer.Sound(os.path.join('assets', 'Sounds', 'Winning.mp3'))


# Miscellaneous functions...............................................................................................
def auto_shoot(counter, threshold, ship, off_xs, off_y, _lis, sound):
    """
    Use to automate enemy shooting.
    :param counter: Global variable.
    :param threshold: Frequency of shooting.
    :param ship: Ship object.
    :param off_xs: List of shoot() offset.
    :param off_y: shoot() offset.
    :param _lis: List object to add Laser object.
    :param sound: Shooting sound.
    """
    if counter >= threshold:
        for _x_off in off_xs:
            ship.shoot(ship.y + off_y, _lis, _x_off)
        sound.play()
        return 0
    return counter


def collide(obj_1, obj_2):
    """
    Use to check if two objects collide each other.
    :param obj_1: Ship or Laser object.
    :param obj_2: Ship or Laser object.
    :return: bool
    """
    off_x = int(obj_2.x - obj_1.x)
    off_y = int(obj_2.y - obj_1.y)
    return obj_1.mask.overlap(obj_2.mask, (off_x, off_y)) is not None


def generate_move(start, steps, length, optimization=0):
    """
    Generates x coordinates for Goons.
    :param start: Starting x coordinate.
    :param steps: Difference between two coordinates.
    :param length: Number of coordinates. Usually FPS.
    :param optimization: Use to generate less number of coordinates (For Tuning purpose).
    :return: list of coordinates.
    """
    moves = []
    c = steps / (length - optimization)
    for _ in range(length):
        moves.append(start)
        start = start + c
    moves.extend(moves[::-1])
    return list(map(int, moves))


def _goon_plot(places, pos_x=10, pos_y=0):
    """
    Places Goons according to places (a 2-D list containing 0 and 1)
    :param places: 2-D list.
    :param pos_x: Starting x coordinate.
    :param pos_y: Starting y coordinate.
    :return: list of all Goons placed.
    """
    _goons = []
    temp = pos_x
    for row in places:
        for place in row:
            if place == 1:
                _goons.append(Goon(pos_x, pos_y, GOON_HEALTH, GOON, LASER_GOON, GOON_DAMAGE))
            pos_x += GOON_X_OFFSET
        pos_y += GOON_Y_OFFSET
        pos_x = temp
    return _goons


def move_player(plyr, a, w, d, s):
    """
    Updates Player's x and y coordinate and Prevent Player from moving offscreen.
    :param plyr: Player object.
    :param a: bool for right button.
    :param w: bool for forward button.
    :param d: bool for right button.
    :param s: bool for backward button.
    :return: None
    """
    if a and 0 <= plyr.x - H_VEL <= WIDTH:
        plyr.x -= H_VEL
    elif w and 0 <= plyr.y - V_VEL <= HEIGHT:
        plyr.y -= V_VEL
    elif d and 0 <= plyr.x + H_VEL <= WIDTH - plyr.img_x:
        plyr.x += H_VEL
    elif s and 0 <= plyr.y + V_VEL <= HEIGHT - plyr.img_y:
        plyr.y += V_VEL


def draw_text(win, text, size, font, x, y, bg_code, count, sec=-1, bold=False):
    """
    Draws Text on Screen for a given amount of seconds.
    :param win: Surface object to blit text.
    :param text: Message to be displayed.
    :param size: Size of text.
    :param font: Style of text.
    :param x: x coordinate of text.
    :param y: y coordinate of text.
    :param bg_code: background colour code.
    :param count: count (Global variable).
    :param sec: Number of second message to be displayed.
    :param bold: bool
    :return: None
    """
    if count == sec:
        style = pygame.font.SysFont(font, size, bold)
        txt_obj = style.render(text, True, bg_code)
        win.blit(txt_obj, (x, y))
    elif sec == -1:
        style = pygame.font.SysFont(font, size, bold)
        txt_obj = style.render(text, True, bg_code)
        win.blit(txt_obj, (x, y))
    else:
        pass


def draw_button(win, colour, l_t_w_h):
    """
    Creates a Rect object.
    :param win: Display object.
    :param colour: Colour of Button.
    :param l_t_w_h: (left, top, width, height)
    :return: Rect object.
    """
    button = pygame.Rect(l_t_w_h)
    pygame.draw.rect(win, colour, button, width=4, border_radius=60)
    return button


def reset_watch(count, fps):
    """
    Use to handle event in time.
    :param count: counter variable (Global count).
    :param fps: FPS
    :return: int
    """
    if count == fps:
        return 0
    return count


# Classes...............................................................................................................
class Laser:
    def __init__(self, x, y, laser_img, laser_damage):
        self.x = x
        self.y = y
        self.laser_img = laser_img
        self.damage = laser_damage
        self.mask = pygame.mask.from_surface(self.laser_img)

    def draw(self, win):
        win.blit(self.laser_img, (self.x, self.y))

    def move(self, vel_y):
        self.y += vel_y

    def off_screen(self):
        return self.y > HEIGHT

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    def __init__(self, x, y, health, ship_img, laser_img, laser_damage):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = ship_img
        self.laser_img = laser_img
        self.damage = laser_damage
        self.mask = pygame.mask.from_surface(ship_img)
        self.centre_w = self.ship_img.get_width() // 2 - self.laser_img.get_width() // 2

    def draw(self, win):
        win.blit(self.ship_img, (self.x, self.y))

    def move(self, vel_x, vel_y):
        self.x = vel_x
        self.y = vel_y

    def shoot(self, off_y, _lis, off_x=0):
        x = self.centre_w + self.x + off_x
        _laser = Laser(x, off_y, self.laser_img, self.damage)
        _lis.append(_laser)

    def ship_collision(self, ship_obj):
        return collide(self, ship_obj)


class Goon(Ship):
    def __init__(self, x, y, health, ship_img, laser_img, laser_damage):
        super().__init__(x, y, health, ship_img, laser_img, laser_damage)
        self.moves = cycle(generate_move(self.x, GOON_STEPS, FPS, OPTIMIZATION))


class Villain(Ship):
    def __init__(self, x, y, health, ship_img, laser_img, laser_damage):
        super().__init__(x, y, health, ship_img, laser_img, laser_damage)
        self.max_health = health
        self.img_x = ship_img.get_width()
        self.img_y = ship_img.get_height()

    def draw(self, win):
        super().draw(win)
        self.health_bar(win)

    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.img_y, self.img_x, 10))
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y + self.img_y, self.img_x * (self.health / self.max_health), 10))
        pygame.draw.rect(window, (0, 0, 0), (self.x, self.y + self.img_y, self.img_x, 10), width=2)


class Player(Ship):
    def __init__(self, x, y, health, ship_img, laser_img, laser_damage):
        super().__init__(x, y, health, ship_img, laser_img, laser_damage)
        self.max_health = health
        self.img_x = ship_img.get_width()
        self.img_y = ship_img.get_height()
        self.cool_counter = 300
        self.shoot_limit = COOL_DOWN

    def cool_down_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (10, 300, 10, 300))
        pygame.draw.rect(window, (0, 0, 255), (10, 300, 10, self.cool_counter))
        pygame.draw.rect(window, (0, 0, 0), (10, 300, 10, 300), width=2)

    def ship_collision(self, obj):
        return collide(self, obj)

    def draw(self, win):
        super().draw(win)
        self.health_bar(win)
        self.cool_down_bar(win)

    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.img_y + 10, self.img_x, 10))
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x, self.y + self.img_y + 10, self.img_x * (self.health / self.max_health), 10))
        pygame.draw.rect(window, (0, 0, 0), (self.x, self.y + self.img_y + 10, self.img_x, 10), width=2)


# MAIN GAME MENU........................................................................................................
IN_GAME = True
CLOCK = pygame.time.Clock()


def main_menu():
    """
    Game menu for choosing Player ship.
    :return: Ship image.
    """
    count = 0
    clicked = False
    px1 = 255
    px2 = 255
    px3 = 255
    px4 = 255
    mixer.music.load(os.path.join('assets', 'Sounds', 'Intro.mp3'))
    mixer.music.play(-1)
    while True:
        CLOCK.tick(FPS)
        WINDOW.blit(BACKGROUND, (0, 0))
        draw_text(WINDOW, 'AVENGE', 100, 'bankgothic', 25, 45, (0, 0, 0), count, -1, True)
        draw_text(WINDOW, 'AVENGE', 100, 'bankgothic', 20, 40, (255, 255, 255), count, -1, True)
        draw_text(WINDOW, 'A SPACE INVADERS GAME', 50, 'bankgothic', 25, 125, (0, 0, 0), count, -1, True)
        draw_text(WINDOW, 'A SPACE INVADERS GAME', 50, 'bankgothic', 20, 120, (255, 255, 255), count, -1, True)
        draw_text(WINDOW, 'CHOOSE YOUR SHIP', 30, 'comicsans', 460, 282, (0, 0, 0), count, -1, True)
        draw_text(WINDOW, 'CHOOSE YOUR SHIP', 30, 'comicsans', 458, 280, (255, 255, 255), count, -1, True)

        draw_text(WINDOW, 'Classic', 35, 'bankgothic', 490, 315, (255, 255, 0), count, -1, True)
        draw_text(WINDOW, 'Modern', 35, 'bankgothic', 490, 375, (255, 255, 0), count, -1, True)
        draw_text(WINDOW, 'Futuristic', 35, 'bankgothic', 465, 435, (255, 255, 0), count, -1, True)
        draw_text(WINDOW, 'Bat-wing', 35, 'bankgothic', 485, 495, (255, 255, 0), count, -1, True)

        mx, my = pygame.mouse.get_pos()
        button_1 = draw_button(WINDOW, (255, 255, px1), (400, 310, 350, 50))
        button_2 = draw_button(WINDOW, (255, 255, px2), (400, 370, 350, 50))
        button_3 = draw_button(WINDOW, (255, 255, px3), (400, 430, 350, 50))
        button_4 = draw_button(WINDOW, (255, 255, px4), (400, 490, 350, 50))
        px1 = 255
        px2 = 255
        px3 = 255
        px4 = 255
        if button_1.collidepoint((mx, my)):
            px1 = 0
            if clicked:
                return HERO_1
        if button_2.collidepoint((mx, my)):
            px2 = 0
            if clicked:
                return HERO_2
        if button_3.collidepoint((mx, my)):
            px3 = 0
            if clicked:
                return HERO_3
        if button_4.collidepoint((mx, my)):
            px4 = 0
            if clicked:
                return HERO_4

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                clicked = pygame.mouse.get_pressed(num_buttons=3)[0]
            if event.type == QUIT:
                return sys.exit()

        pygame.display.update()


def paused():
    """
    Pauses the game until ESC key is pressed.
    :return: None
    """
    while True:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return None
            elif event.type == QUIT:
                sys.exit()
        draw_text(WINDOW, 'PAUSED', 50, 'bankgothic', 455, 505, (0, 0, 0), 0, -1, True)
        draw_text(WINDOW, 'PAUSED', 50, 'bankgothic', 450, 500, (255, 255, 255), 0, -1, True)
        pygame.display.update()


def the_end():
    """
    The End screen of game.
    :return: None
    """
    mixer.music.load(os.path.join('assets', 'Sounds', 'Victory.mp3'))
    mixer.music.play(-1)
    while True:
        CLOCK.tick(FPS)
        WINDOW.blit(BACKGROUND, (0, 0))
        draw_text(WINDOW, 'VICTORY', 100, 'bankgothic', 310, 310, (0, 0, 0), 0, -1, True)
        draw_text(WINDOW, 'VICTORY', 100, 'bankgothic', 300, 300, (255, 255, 255), 0, -1, True)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    sys.exit()
            elif event.type == QUIT:
                sys.exit()
        pygame.display.update()


# CHOOSING SHIP MENU....................................................................................................
HERO = main_menu()
HERO_IMG_X, HERO_IMG_Y = HERO.get_width(), HERO.get_height()
player = Player(WIDTH // 2 - HERO_IMG_X // 2, HEIGHT - HERO_IMG_Y, HERO_HEALTH, HERO, LASER_HERO, HERO_DAMAGE)


# ......................................................................................................................


def level_maker(stage, villain_obj_list, vx_off, v_img_height, vx_moves, v_shoot_sound, frequency, lvl_sound):
    """
    This function is use to create levels.
    :param stage: 2-D list of 1s and 0s representing Goons positions.
    :param villain_obj_list: List of Villain Object.
    :param vx_off: Shooting x offset.
    :param v_img_height: Shooting y offset
    :param vx_moves: cycle iterator of x coordinates.
    :param v_shoot_sound: Laser shooting sound.
    :param frequency: Villain shooting frequency per FPS frames.
    :param lvl_sound: Level music.
    :return: None
    """
    global IN_GAME
    IN_GAME = True
    goons = _goon_plot(stage, 10, 0)
    villains = villain_obj_list
    goon_shoot_counter = 0
    villain_shoot_counter = 0
    _win_counter = 0
    cool_down = False
    lost = False
    l_down, f_down, r_down, b_down = False, False, False, False
    mixer.music.load(os.path.join('assets', 'Sounds', lvl_sound))
    mixer.music.play(-1)
    if player.health > HERO_HEALTH:
        player.health = HERO_HEALTH
    while IN_GAME:
        CLOCK.tick(FPS)
        WINDOW.blit(BACKGROUND, (0, 0))
        # Removing goons and villains as per health and collision.......................................................
        for goon in goons:
            if goon.health <= 0:
                goons.remove(goon)
                EXPLODE_SOUND.play()
                continue
            elif player.ship_collision(goon):
                goons.remove(goon)
                player.health -= goon.damage
                EXPLODE_SOUND.play()
                continue
            goon.draw(WINDOW)
            goon.move(next(goon.moves), goon.y + DOWN_SPEED)

        for villain in villains:
            if villain.health <= 0:
                villains.remove(villain)
                EXPLODE_SOUND.play()
                continue
            elif player.ship_collision(villain):
                player.health = 0
            villain.draw(WINDOW)
            villain.move(next(vx_moves), villain.y + DOWN_SPEED)

        if player.health <= 0 or any([goon.y > HEIGHT-50 for goon in goons]) or any([villain.y > HEIGHT-50 for villain
                                                                                     in villains]):
            mixer.music.stop()
            if not lost:
                EXPLODE_SOUND.play()
            lost = True
            player.x, player.y = -100, -100
            draw_text(WINDOW, 'YOU LOST', 100, 'bankgothic', 255, 405, (0, 0, 0), 0, -1, True)
            draw_text(WINDOW, 'YOU LOST', 100, 'bankgothic', 250, 400, (255, 255, 255), 0, -1, True)
        else:
            player.draw(WINDOW)
        # Removing Lasers as per collision and off screen...............................................................
        for laser in ENEMY_LASERS:
            if laser.collision(player):
                ENEMY_LASERS.remove(laser)
                player.health -= laser.damage
            elif laser.off_screen():
                ENEMY_LASERS.remove(laser)
                continue
            laser.draw(WINDOW)
            laser.move(LASER_VEL)

        for laser in HERO_LASERS:
            if laser.off_screen():
                HERO_LASERS.remove(laser)
                continue
            for goon in goons:
                if laser.collision(goon):
                    HERO_LASERS.remove(laser)
                    goon.health -= player.damage
            for villain in villains:
                if laser.collision(villain):
                    villain.health -= player.damage
                    HERO_LASERS.remove(laser)
            laser.draw(WINDOW)
            laser.move(-LASER_VEL)
        # Automating shooting of goons and villains.....................................................................
        if len(goons) == 0:
            goon_shoot_counter = 0
        else:
            goon_shoot_counter = auto_shoot(goon_shoot_counter, FPS // DIFFICULTY, random.choice(goons), [0],
                                            SHOOT_OFFSET,
                                            ENEMY_LASERS, GOON_SHOOT_SOUND)

        if len(villains) == 0:
            villain_shoot_counter = 0
        else:
            villain_shoot_counter = auto_shoot(villain_shoot_counter, FPS//frequency, random.choice(villains), vx_off,
                                               v_img_height, ENEMY_LASERS, v_shoot_sound)
        # Catching events from users....................................................................................
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN and not lost:
                if event.key == K_ESCAPE:
                    paused()
                elif event.key == K_w:
                    f_down = True
                elif event.key == K_a:
                    l_down = True
                elif event.key == K_d:
                    r_down = True
                elif event.key == K_s:
                    b_down = True
                elif event.key == K_SPACE:
                    if not cool_down:
                        player.shoot(player.y, HERO_LASERS)
                        player.cool_counter -= 60
                        HERO_SHOOT_SOUND.play()
            elif event.type == KEYUP:
                if event.key == K_w:
                    f_down = False
                elif event.key == K_a:
                    l_down = False
                elif event.key == K_d:
                    r_down = False
                elif event.key == K_s:
                    b_down = False
        move_player(player, l_down, f_down, r_down, b_down)
        # Playing Burn out sound........................................................................................
        if player.cool_counter <= 0:
            cool_down = True
            BURNOUT.play()
            player.cool_counter += 1
        elif player.cool_counter == 300:
            cool_down = False
        else:
            player.cool_counter += 1
        # Playing Winning sound if all enemies are destroyed............................................................
        if len(goons) == 0 and len(villains) == 0:
            if _win_counter == 0:
                mixer.music.stop()
                WIN.play()
            if _win_counter >= 5 * FPS:
                IN_GAME = False
            _win_counter += 1

        goon_shoot_counter += 1
        villain_shoot_counter += 1
        pygame.display.update()

    return None
# ......................................................................................................................
