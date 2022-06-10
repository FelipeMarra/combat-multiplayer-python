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

    #displays a text on the screen
    def show_text(self, text, font_size, color, x, y):
        font = pygame.font.Font(self.font, font_size)
        text = font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text, text_rect)

    def show_start_screen(self):

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
                    waiting = False

                #blinking text
                if event.type == font_fade:
                    show_text = not show_text

                self.screen.fill(BLACK)

                #show logo
                start_logo_rect = self.start_logo.get_rect()
                start_logo_rect.midtop = (WIDTH/2, 20)
                self.screen.blit(self.start_logo, start_logo_rect)

                if show_text:
                    self.show_text('PRESS ANY KEY TO START', 32, YELLOW, WIDTH/2, HIGHT/2 + 50)

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