#Screen dimentions
WIDTH = 1280
HEIGHT = 720

#positions
PLAYER_POSITION_0 = (100, HEIGHT/2)
PLAYER_POSITION_1 = (WIDTH-100, HEIGHT/2)
POSITIONS = [PLAYER_POSITION_0, PLAYER_POSITION_1]

#game title
GAME_TITLE = "Combat Multiplayer"

#FPS
FPS = 30

#COLORS
BLACK = (0, 0, 0)
YELLOW = (244, 233, 51)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

PILLS = [RED, BLUE]
COLORS = [RED, BLACK]
INFO_COLORS = [BLACK, WHITE]

#Images
TEST_TANK_SHEET = "tank_01_grey.png"
TEST_MAP_SHEET = "tank_01_grey.png"
START_LOGO = "atari_combat_logo.png"
TANK_WALLPAPER = "tankwallpaper.png"
START_BACKGROUND = "background.jpg"
POINTER = "pointer_image.png"
CHOICEMAP = "mapchoice.png"
WAITING_IMAGE = "waiting_image.jpg"

#Audios
AOT_OPENING = 'aotopening.wav'
MOSCOU_DEFENDER = 'moscoudefender.wav'
BEEP_SOUND = 'beep.wav'
MORPHEUS_AUDIO = "morpheus.wav"


#TEXT
TEXT_FONT = "arial"

#Player Settings
N_PLAYERS = 2
TANK_BLUE = "tank_blue.png"
TANK_RED = "tank_red.png"
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.2
COLLISION_TOLLERANCE = 25

#Bullet Settings
BLUEBULLET = "bluebullet.png"
REDBULLET = "redbullet.png"
BULLET_SOUND = "cannon_fire.wav"
BULLET_SPEED = 20
BULLET_LIFETIME = 6000
BULLET_RATE = 1000
LATERAL = "hitting_lateral"
UPDOWN = "hitting_updown"
BULLET_COLLISION_TOLLERANCE = 13
BULLET_SIZE = (20, 20)

#Explosion
EXPLOSION_SOUND = 'explosion.wav'
EXPLOSION_SPEED = 4

#server/network settings
BUFFER_SIZE = 1024
SERVER_IP = -1
SERVER_PORT = -1

#server/network commands
#get asks the server an information
GET_READY_PLAYERS = "GET READY_PLAYERS"
GET_GAME_MAP = "GET GAME_MAP"
#post sets a information on the server or client
POST_GAME_MAP = "POST GAME_MAP"
POST_PID_IS_READY = "POST PID_IS_READY"
POST_GAME_RESET = "POST GAME_RESET"

#states
INITIAL_STATE = 0
CONNECT_TO_SERVER_STATE = 1
GET_MAP_STATE = 2
AWAIT_PLAYERS_STATE = 3
TRADE_UPDATES_STATE = 4
END_STATE = 5