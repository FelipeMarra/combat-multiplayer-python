import pygame
from constants import *
import os
# TODO import sprits

class Game:
    def __init__(self):
        #Creating screem
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.timer = pygame.time.Clock()
        self.is_running = True
        self.font = pygame.font.match_font(TEXT_FONT)
        self.load_files()

    def new_game(self):
        #intanciating sprits
        self.all_sprits = pygame.sprite.Group()
        self.run()

    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.timer.tick(FPS)
            self.events()
            self.update_sprits()
            self.draw_sprits()

    def events(self):
        #defines games events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.is_running = False

    def update_sprits(self):
        self.all_sprits.update()

    def draw_sprits(self):
        #cleaning screen
        self.screen.fill(BLACK)
        #drawing sprits
        self.all_sprits.draw(self.screen)
        pygame.display.flip()

    #load audio and images
    def load_files(self):
        images_directory = os.path.join(os.getcwd(), "midia/images")
        self.audios_directory = os.path.join(os.getcwd(), "midia/audios")
        self.test_tank_sheet = os.path.join(images_directory, TEST_TANK_SHEET)
        self.test_map = os.path.join(images_directory, TEST_MAP_SHEET)
        #get and scale logo
        self.start_logo = os.path.join(images_directory, START_LOGO)
        self.start_logo = pygame.image.load(self.start_logo).convert()
        self.start_logo = pygame.transform.scale(self.start_logo, (720, 360))
        #tanks start screen
        self.tank_wallpaper1 = os.path.join(images_directory, TANK_WALLPAPER)
        self.tank_wallpaper1 = pygame.image.load(self.tank_wallpaper1).convert_alpha()
        self.tank_wallpaper1 = pygame.transform.scale(self.tank_wallpaper1, (500, 360))
        self.tank_wallpaper1 = pygame.transform.flip(self.tank_wallpaper1, False, False)
        self.tank_wallpaper1 = pygame.transform.rotate(self.tank_wallpaper1, 340)

        self.tank_wallpaper2 = os.path.join(images_directory, TANK_WALLPAPER)
        self.tank_wallpaper2 = pygame.image.load(self.tank_wallpaper2).convert_alpha()
        self.tank_wallpaper2 = pygame.transform.scale(self.tank_wallpaper2, (500, 360))
        self.tank_wallpaper2 = pygame.transform.flip(self.tank_wallpaper2, True, False)
        self.tank_wallpaper2 = pygame.transform.rotate(self.tank_wallpaper2, 20)

        #audios
        self.start_song = pygame.mixer.Sound(os.path.join(self.audios_directory, AOT_OPENING))
        self.start_song.set_volume(0.1)
        self.moscou_song = pygame.mixer.Sound(os.path.join(self.audios_directory, MOSCOU_DEFENDER))
        self.moscou_song.set_volume(0.1)
        self.beep_sound = pygame.mixer.Sound(os.path.join(self.audios_directory, BEEP_SOUND))

    #displays a text on the screen
    def show_text(self, text, font_size, color, x, y):
        font = pygame.font.Font(self.font, font_size)
        text = font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text, text_rect)

    def show_start_screen(self):

        #self.start_song.play()
        font_fade = pygame.USEREVENT + 1
        show_text = True
        pygame.time.set_timer(font_fade, 900)

        waiting = True
        while waiting:
            self.timer.tick(120)

            #show texts
            for event in pygame.event.get():
                #await command
                if event.type == pygame.QUIT:
                    waiting = False
                    self.is_running = False

                if event.type == pygame.KEYUP:
                    self.beep_sound.play()
                    self.start_song.stop()
                    waiting = False

                #blinking text
                if event.type == font_fade:
                    show_text = not show_text

                self.screen.fill(BLACK)

                #show logo
                start_logo_rect = self.start_logo.get_rect()
                start_logo_rect.midtop = (WIDTH/2, 20)
                self.screen.blit(self.start_logo, start_logo_rect)

                #show tanks
                wallpaper1_tank_rect = self.tank_wallpaper1.get_rect()
                wallpaper1_tank_rect.midtop = (200, 250)
                self.screen.blit(self.tank_wallpaper1, wallpaper1_tank_rect)

                wallpaper2_tank_rect = self.tank_wallpaper2.get_rect()
                wallpaper2_tank_rect.midtop = (WIDTH-200, HIGHT-470)
                self.screen.blit(self.tank_wallpaper2, wallpaper2_tank_rect)

                if show_text:
                    self.show_text('PRESS ANY KEY TO CONNECT', 32, YELLOW, WIDTH/2, HIGHT/2 + 50)

                self.show_text('Developed by Marra & Galli (w/o Muriarte)', 19, WHITE, WIDTH/2, HIGHT-20)
                pygame.display.flip()



    def show_game_over_screen(self):
        pass

if __name__ == "__main__":
    game = Game()
    game.show_start_screen()

    while game.is_running:
        game.new_game()
        game.show_game_over_screen()