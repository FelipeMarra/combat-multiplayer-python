import sys
import threading

import pygame

from app import *

from app.client.sprites import *

from app.client.midia import midia_loader
from app.client.screens import start_screen, game_over_screen
from app.client.network import Network

class Game(metaclass=SingletonMeta):
    def __init__(self):
        # Creating screem
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=4)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.timer = pygame.time.Clock()
        self.is_running = True
        self.font = pygame.font.match_font(TEXT_FONT)
        midia_loader.load_files(self)
        self.network = Network(server_ip, int(server_port))

    def new_game(self):
        # intanciating sprites
        self.all_sprites = pygame.sprite.Group()
        p_data = self.network.my_player_data
        enemy_data = self.network.start_enemy(ServerPkt(PLAYER, p_data))
        self.my_player = Player(self, p_data, True)
        self.enemy_player = Player(self, enemy_data, False)
        self.alliebullets = pygame.sprite.Group()
        self.enemybullets = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        wall_creator(self, map = 1)
        self.all_sprites.add(self.my_player)
        self.all_sprites.add(self.enemy_player)
        self.moscou_song.play(-1)

    def run(self):
        #sercer data receiving loop
        new_thread = threading.Thread(target=self.network.receive, args=(id(self),))
        new_thread.start()
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.timer.tick(FPS) / 1000.0
            self.events()
            update_sprites(self)
            draw_sprites(self)


    def events(self):
        # defines games events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.is_running = False

if __name__ == "__main__":
    file, server_ip, server_port, test_mode = sys.argv
    game = Game()
    if(test_mode != "True"):
        start_screen.show()
    #TODO game.show_await_screen()
    my_player = game.network.connect()
    if(my_player.pid == 0):
        game.network.await_match()
    while game.is_running:
        game.new_game()
        game.run()
        game_over_screen.show()
