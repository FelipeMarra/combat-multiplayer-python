import os

import pygame

from app import *

# load audio and images
def load_files(game):
    images_directory = os.path.join(os.getcwd(), "app/client/midia/images")
    game.audios_directory = os.path.join(os.getcwd(), "app/client/midia/audios")
    game.animation_directory = os.path.join(os.getcwd(), f"{images_directory}/boom")
    game.test_tank_sheet = os.path.join(images_directory, TEST_TANK_SHEET)
    game.test_map = os.path.join(images_directory, TEST_MAP_SHEET)
    # get and scale logo
    game.start_logo = os.path.join(images_directory, START_LOGO)
    game.start_logo = pygame.image.load(game.start_logo).convert_alpha()
    game.start_logo = pygame.transform.scale(game.start_logo, (720, 360))
    # background
    game.start_background = os.path.join(images_directory, START_BACKGROUND)
    game.start_background = pygame.image.load(game.start_background).convert()
    game.start_background = pygame.transform.scale(game.start_background, (WIDTH, HEIGHT))
    #map
    game.map_background = os.path.join(images_directory, MAPBACKGROUND)
    game.map_background = pygame.image.load(game.map_background).convert_alpha()
    game.map_background = pygame.transform.smoothscale(game.map_background, (WIDTH, HEIGHT))

    #pointer
    game.pointerImg = os.path.join(images_directory, POINTER)
    game.pointerImg = pygame.image.load(game.pointerImg).convert_alpha()
    game.pointerImg = pygame.transform.scale(game.pointerImg, (50, 50))

    # tanks start screen
    game.tank_wallpaper1 = os.path.join(images_directory, TANK_WALLPAPER)
    game.tank_wallpaper1 = pygame.image.load(game.tank_wallpaper1).convert_alpha()
    game.tank_wallpaper1 = pygame.transform.scale(game.tank_wallpaper1, (500, 360))
    game.tank_wallpaper1 = pygame.transform.flip(game.tank_wallpaper1, False, False)
    game.tank_wallpaper1 = pygame.transform.rotate(game.tank_wallpaper1, 340)

    game.tank_wallpaper2 = os.path.join(images_directory, TANK_WALLPAPER)
    game.tank_wallpaper2 = pygame.image.load(game.tank_wallpaper2).convert_alpha()
    game.tank_wallpaper2 = pygame.transform.scale(game.tank_wallpaper2, (500, 360))
    game.tank_wallpaper2 = pygame.transform.flip(game.tank_wallpaper2, True, False)
    game.tank_wallpaper2 = pygame.transform.rotate(game.tank_wallpaper2, 20)

    # audios
    game.start_song = pygame.mixer.Sound(os.path.join(game.audios_directory, AOT_OPENING))
    game.start_song.set_volume(0.1)
    game.moscou_song = pygame.mixer.Sound(os.path.join(game.audios_directory, MOSCOU_DEFENDER))
    game.moscou_song.set_volume(0.1)
    game.beep_sound = pygame.mixer.Sound(os.path.join(game.audios_directory, BEEP_SOUND))
    game.explosion_sound = pygame.mixer.Sound(os.path.join(game.audios_directory, EXPLOSION_SOUND))
    game.explosion_sound.set_volume(0.3)

    # player
    game.player_image = pygame.image.load(os.path.join(images_directory, TANK_BLUE)).convert_alpha()
    game.player_image = pygame.transform.scale(game.player_image, (50, 50))
    game.player_image = pygame.transform.rotate(game.player_image, 90)

    # enemy
    game.enemy_image = pygame.image.load(os.path.join(images_directory, TANK_RED)).convert_alpha()
    game.enemy_image = pygame.transform.scale(game.enemy_image, (50, 50))
    game.enemy_image = pygame.transform.rotate(game.enemy_image, 90)

    # bullet
    game.blue_bullet = pygame.image.load(os.path.join(images_directory, BLUEBULLET)).convert_alpha()
    game.blue_bullet = pygame.transform.scale(game.blue_bullet, BULLET_SIZE)
    game.red_bullet = pygame.image.load(os.path.join(images_directory, REDBULLET)).convert_alpha()
    game.red_bullet = pygame.transform.scale(game.red_bullet, BULLET_SIZE)
    game.bullet_song = pg.mixer.Sound(os.path.join(game.audios_directory, BULLET_SOUND))
    game.bullet_song.set_volume(0.5)