import pygame
import constants as consts
# TODO import sprits

class Game:
    def __init__(self):
        #Creating screem
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((consts.WIDTH, consts.HIGHT))
        pygame.display.set_caption(consts.GAME_TITLE)
        self.timer = pygame.time.Clock()
        self.is_running = True

    def new_game(self):
        #intanciating sprits
        self.all_sprits = pygame.sprite.Group()
        self.run()

    def run(self):
        #game loop
        print("RUN")
        self.playing = True
        while self.playing:
            self.timer.tick(consts.FPS)
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
        print("DRAW")
        #cleaning screen
        self.screen.fill(consts.BLACK)
        #drawing sprits
        self.all_sprits.draw(self.screen)
        pygame.display.flip()

    def show_start_screen(self):
        pass

    def show_game_over_screen(self):
        pass

if __name__ == "main":
    game = Game()
    game.show_start_screen()

    while game.is_running:
        game.new_game()
        game.show_game_over_screen()