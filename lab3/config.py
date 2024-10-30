import pygame

TEAMS_COLORS = [
    [127, 127, 127, 50],
    [0, 0, 255, 255],
    [255, 255, 0, 255],
    [255, 0, 255, 255],
    [0, 255, 255, 255]]

background = pygame.image.load("bin/background.bmp")
sword = pygame.image.load("bin/sword.png")
computer = pygame.image.load("bin/computer.png")
goal = pygame.image.load("bin/goal.png")
player = pygame.image.load("bin/player.png")

colored_players = [
    player.copy(),
    player.copy(),
    player.copy(),
    player.copy(),
    player.copy()
]

colored_computers = [
    computer.copy(),
    computer.copy(),
    computer.copy(),
    computer.copy(),
    computer.copy()
]

colored_swords = [
    sword.copy(),
    sword.copy(),
    sword.copy(),
    sword.copy(),
    sword.copy()
]

for i in range(len(TEAMS_COLORS)):
    colored_players[i].fill(TEAMS_COLORS[i], special_flags=pygame.BLEND_RGBA_MIN)
    colored_computers[i].fill(TEAMS_COLORS[i], special_flags=pygame.BLEND_RGBA_MIN)
    colored_swords[i].fill(TEAMS_COLORS[i], special_flags=pygame.BLEND_RGBA_MIN)

