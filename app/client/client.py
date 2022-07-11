import sys
import threading

import pygame

from app import *

from app.client.sprites import *

from app.client.midia import midia_loader
from app.client.screens import start_screen, settings_screen, await_screen, game_over_screen
from app.client.network import Network

vec = pg.math.Vector2

class Game(metaclass=SingletonMeta):
    def __init__(self):
        # Creating screem
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=4)
        self.map = -1
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.timer = pygame.time.Clock()
        self.is_running = True
        self.font = pygame.font.match_font(TEXT_FONT)
        midia_loader.load_files(self)
        self.network = Network(SERVER_IP, SERVER_PORT)

    def new_game(self):
        # intanciating sprites
        self.all_sprites = pygame.sprite.Group()
        p_data = self.network.my_player_data
        enemy_data = self.network.start_enemy(p_data)
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

    def reset(self):
        print("Entrou no reset!")
        #clear bullets and players sprits
        for bullet in self.alliebullets:
            bullet.kill()
        for bullet in self.enemybullets:
            bullet.kill()
        self.enemy_player.kill()
        self.my_player.kill()

        #get next start position
        #enemmy_start_position = self.my_player.start_position 
        #print(f"NEW ENEMMY POS {enemmy_start_position}")
        self.my_player.start_position = (self.my_player.start_position + 1) % 2
        print(f"NEW MY P POS {self.my_player.start_position}")

        #update player position data
        self.my_player.pos = vec(POSITIONS[self.my_player.start_position])
        #self.enemy_player.pos = vec(POSITIONS[enemmy_start_position])

        #add player data to screen
        self.all_sprites.add(self.my_player)
        self.all_sprites.add(self.enemy_player)

if __name__ == "__main__":
    test_mode = "False"
    file, server_ip, server_port, test_mode = sys.argv
    
    SERVER_IP = server_ip
    SERVER_PORT = int(server_port)

    game = Game()

    if(test_mode != "True"):
        start_screen.show(game)

    my_player = game.network.connect()

    if(my_player.pid == 0):
        game.map = settings_screen.show(game)
        game.network.send_selected_map(game.map)
        await_screen.show(game)

    if(my_player.pid == 1):
        await_screen.show(game)

    while game.is_running:
        game.new_game()
        game.run()
        #TODO game_over_screen.show(game)
