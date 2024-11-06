import pygame
import json
from random_player import RandomPlayer
from greedy_player import GreedyPlayer
from aggressive_player import AggresivePlayer
from controlled_player import ControlledPlayer


# Loading config with variables
json_data = {}
with open("config.json", "rt") as f:
    json_data = json.load(f)

PLAYERS_COLORS = json_data["players_colors"]
SCREEN_WIDTH = json_data["screen_width"]
SCREEN_HEIGHT = json_data["screen_height"]
SCREEN_SAFE_LEFT = json_data["screen_offset_left"]
SCREEN_SAFE_RIGHT = SCREEN_WIDTH - json_data["screen_offset_right"]
SCREEN_SAFE_TOP = json_data["screen_offset_top"]
SCREEN_SAFE_BOTTOM = SCREEN_HEIGHT - json_data["screen_offset_bottom"]
MIN_NODES_DIST = json_data["node_min_dist_between"]
MIN_NODE_RADIUS = json_data["node_min_radius"]
MAX_NODE_RADIUS = max(json_data["node_max_radius"],json_data["node_min_radius"] + 1)
NODE_PLACEMENT_METHOD = json_data["node_placement_method"]
NODE_RANDOM_PLACEMENT_ADDITIONAL_POINTS = json_data["node_placement_random_additional_points"]
PLAYERS_BEHAVIOUR = json_data["players_behaviour"]
PLAYERS_POSITIONS = json_data["players_positions"]
PLAYERS = []


# load images
background = pygame.image.load(json_data["background_img"])
node = pygame.image.load(json_data["node_img"])
goal = pygame.image.load(json_data["goal_img"])
player = pygame.image.load(json_data["player_img"])

# generate colored images
colored_players = [
    player.copy(),
    player.copy(),
    player.copy(),
    player.copy(),
    player.copy()
]

colored_nodes = [
    node.copy(),
    node.copy(),
    node.copy(),
    node.copy(),
    node.copy()
]

for i in range(len(PLAYERS_COLORS)):
    colored_players[i].fill(PLAYERS_COLORS[i], special_flags=pygame.BLEND_RGBA_MIN)
    colored_nodes[i].fill(PLAYERS_COLORS[i], special_flags=pygame.BLEND_RGBA_MIN)

# generate players
for i in range(len(PLAYERS_BEHAVIOUR)):
    if PLAYERS_BEHAVIOUR[i] == "random":
        PLAYERS.append(RandomPlayer(i + 1))
    elif PLAYERS_BEHAVIOUR[i] == "aggressive":
        PLAYERS.append(AggresivePlayer(i + 1))
    elif PLAYERS_BEHAVIOUR[i] == "greedy":
        PLAYERS.append(GreedyPlayer(i + 1))
    elif PLAYERS_BEHAVIOUR[i] == "controlled":
        PLAYERS.append(ControlledPlayer(i + 1))
    else:
        PLAYERS.append(RandomPlayer(i + 1))
