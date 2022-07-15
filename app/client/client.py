import sys
from tkinter import E

import pygame

from app import *

from app.client.sprites import *

from app.client.midia import midia_loader
from app.client.screens import start_screen, settings_screen, await_screen, game_over_screen
from app.client.network import Network

vec = pg.math.Vector2

class Game():
    def __init__(self):
        # Creating screem
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=4)
        self.map = -1
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.timer = pygame.time.Clock()
        self.font = pygame.font.match_font(TEXT_FONT)
        midia_loader.load_files(self)
        self.network = Network(SERVER_IP, SERVER_PORT)
        self.state = INITIAL_STATE

    def new_game(self):
        # intanciating sprites
        self.all_sprites = pygame.sprite.Group()
        p_data = self.network.my_player_data
        enemy_data = self.network.enemy_player_data
        self.my_player = Player(self, p_data, True)
        self.enemy_player = Player(self, enemy_data, False)
        self.alliebullets = pygame.sprite.Group()
        self.enemybullets = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        wall_creator(self, self.map)
        self.all_sprites.add(self.my_player)
        self.all_sprites.add(self.enemy_player)
        self.moscou_song.play(-1)

    def run(self):
        # game loop
        while self.state != END_STATE:
            self.dt = self.timer.tick(FPS) / 1000.0
            self.events()
            update_sprites(self)
            draw_sprites(self)
            


    def events(self):
        # defines games events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = END_STATE

    def reset(self):
        print(f"PLayer PID {self.my_player.pid} LIFE {self.my_player.life} && PID {self.enemy_player.pid} LIFE {self.enemy_player.life}")
        #clear bullets and players sprits
        for bullet in self.alliebullets:
            bullet.kill()
        for bullet in self.enemybullets:
            bullet.kill()
        self.enemy_player.kill()
        self.my_player.kill()
        if(self.my_player.life == 0 or self.enemy_player.life == 0):
            game.state = END_STATE

        #get next start position
        self.my_player.start_position = (self.my_player.start_position + 1) % 2

        #update player position data
        self.my_player.pos = vec(POSITIONS[self.my_player.start_position])
        #self.enemy_player.pos = vec(POSITIONS[enemmy_start_position])

        #add player data to screen
        self.all_sprites.add(self.my_player)
        self.all_sprites.add(self.enemy_player)
        
        if self.my_player.life == 0 or self.enemy_player.life == 0:
            self.moscou_song.stop()
            self.state = END_STATE

    def show_info(self):
        my_hp_obj = pygame.font.SysFont(self.font, 50, True)
        my_hp_text = my_hp_obj.render(f"MY LIVES: {self.my_player.life}", 1, INFO_COLORS[game.map - 1])
        
        enemy_hp_obj = pygame.font.SysFont(self.font, 50, True)
        enemy_hp_text = enemy_hp_obj.render(f"ENEMY LIVES: {self.enemy_player.life}", 1, INFO_COLORS[game.map - 1])
        
        self.screen.blit(my_hp_text, (450,10))
        self.screen.blit(enemy_hp_text, (450,70))
        
if __name__ == "__main__":
    test_mode = "False"
    file, server_ip, server_port, test_mode = sys.argv

    SERVER_IP = server_ip
    SERVER_PORT = int(server_port)

    waiting = True
    while waiting:
        game = Game()

        if(test_mode != "True"):
            start_screen.show(game)

        #check if user closed the scree
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                waiting = False
                game.state = END_STATE
                continue

        game.state = CONNECT_TO_SERVER_STATE
        my_player = game.network.connect()

        if(my_player.pid == 0):
            game.map = settings_screen.show(game)

            game.network.send_selected_map(game.map)
            game.network.send_pid_is_ready()

            game.state = AWAIT_PLAYERS_STATE
            game.network.start_receive(game)

            await_screen.show(game)

        if(my_player.pid == 1):
            game.state = GET_MAP_STATE
            game.network.start_receive(game)
            await_screen.show(game)

        game.new_game()
        game.run()
        game_over_screen.show(game)