import math
import random
import pygame

import config


class IntermediatePoint:
    def __init__(self, pos, radius, team=0, is_master=False):
        self.rect = pygame.Rect(pos[0] - 16, pos[1] - 16, 32, 32)
        self.pos = pos
        self.radius = radius
        self.team = team
        self.health = 100
        self.is_master = is_master
        self.connection_pos = None
        self.attack_pos = None
        self.attack_team = 0
        self.active = False

    def update(self):
        if self.team != 0:
            self.health += 1
        self.connection_pos = None
        self.attack_pos = None

    def draw_arrow(self, screen, colour, start, end):
        pygame.draw.line(screen, colour, start, end, 8)
        rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
        center = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        pygame.draw.polygon(screen, colour, (
        (center[0] + 20 * math.sin(math.radians(rotation)), center[1] + 20 * math.cos(math.radians(rotation))),
        (center[0] + 20 * math.sin(math.radians(rotation - 120)), center[1] + 20 * math.cos(math.radians(rotation - 120))),
        (center[0] + 20 * math.sin(math.radians(rotation + 120)), center[1] + 20 * math.cos(math.radians(rotation + 120)))))

    def drawConnections(self, screen, font):
        if self.connection_pos != None:
            pygame.draw.line(screen, config.PLAYERS_COLORS[self.team], self.pos, self.connection_pos, 10)

        if self.attack_pos != None:
            self.draw_arrow(screen, config.PLAYERS_COLORS[self.attack_team], self.pos, self.attack_pos)

    def draw(self, screen, font):
        color = config.PLAYERS_COLORS[self.team]

        alpha_color = [color[0], color[1], color[2], 50]
        pygame.draw.circle(screen, alpha_color, self.pos, self.radius, 1)

        if self.active:
            pygame.draw.circle(screen, color, self.pos, self.radius, 1)
            pygame.draw.circle(screen, color, self.pos, 20, 0)

        if self.is_master:
            screen.blit(config.colored_players[self.team], (self.pos[0] - 16, self.pos[1] - 16))
        else:
            screen.blit(config.colored_nodes[self.team], (self.pos[0] - 16, self.pos[1] - 16))

        text = font.render(str(self.health), True, (255, 255, 255))
        screen.blit(text, (self.pos[0] - 10, self.pos[1] + 10))

    def getNeighborsIndices(self, all_neighbors):
        res = []
        for i in range(len(all_neighbors)):
            if self.pos[0] == all_neighbors[i].pos[0] and self.pos[1] == all_neighbors[i].pos[1]:
                continue
            if (self.pos[0] - all_neighbors[i].pos[0]) ** 2 + (self.pos[1] - all_neighbors[i].pos[1]) ** 2 < self.radius ** 2:
                res.append(i)
        return res

    def getTeamNeighborsIndices(self, all_neighbors):
        res = []
        for i in range(len(all_neighbors)):
            if self.pos[0] == all_neighbors[i].pos[0] and self.pos[1] == all_neighbors[i].pos[1]:
                continue
            if all_neighbors[i].team == self.team:
                if (self.pos[0] - all_neighbors[i].pos[0]) ** 2 + (self.pos[1] - all_neighbors[i].pos[1]) ** 2 < self.radius ** 2:
                    res.append(i)
        return res

    def connect(self, connection_pos):
        self.connection_pos = connection_pos

    def attack(self, attack_pos, attack_team):
        self.attack_pos = attack_pos
        self.attack_team = attack_team

    def markActive(self):
        self.active = True

    def unmarkActive(self):
        self.active = False