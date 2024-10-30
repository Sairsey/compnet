import time

import pygame
import sys
import random
from background import Background
from source import SourcePoint
from intermediate import IntermediatePoint
from random_player import RandomPlayer
from greedy_player import GreedyPlayer
from aggresive_player import AggresivePlayer
from controlled_player import ControlledPlayer

class Game:
    WIDTH = 1280
    HEIGHT = 720
    SAFE_LEFT = 20
    SAFE_RIGHT = WIDTH - 20
    SAFE_TOP = 20
    SAFE_BOTTOM = HEIGHT - 20
    ALLOWED_DIST = 20
    MIN_RADIUS = 100
    MAX_RADIUS = 400
    ADDITIONAL_POINTS = 50

    PLAYERS = [
        ControlledPlayer(1),
        RandomPlayer(2),
        AggresivePlayer(3),
        GreedyPlayer(4),
    ]

    takenPoints = []
    def generatePosition(self):
        isGood = False
        point = ()
        while not isGood:
            point = random.randrange(self.SAFE_LEFT, self.SAFE_RIGHT), random.randrange(self.SAFE_TOP, self.SAFE_BOTTOM)
            isGood = True
            for p in self.takenPoints:
                if (p[0] - point[0]) ** 2 + (p[1] - point[1]) ** 2 < self.ALLOWED_DIST ** 2:
                    isGood = False
                    break
        self.takenPoints.append(point)
        return point

    def setPosition(self, point):
        self.takenPoints.append(point)
        return point

    def connectPoints(self, start_point):
        path = []
        queue = [start_point]
        shortest_paths = [[start_point]]
        current = 0
        # Simple BFS
        while current < len(queue):
            current_point_pos = self.intermediate_points[queue[current]].pos
            current_point_radius = self.intermediate_points[queue[current]].radius
            target_point_pos = self.source_point.pos
            # if we can go straight to target -> do it
            if (current_point_pos[0] - target_point_pos[0]) ** 2 + (current_point_pos[1] - target_point_pos[1]) ** 2 <= current_point_radius ** 2:
                path = shortest_paths[current]
                break
            # if we cannot -> retrieve neighbor points
            neighbors = self.intermediate_points[queue[current]].getNeighborsIndices(self.intermediate_points)
            for neighbor in neighbors:
                if neighbor in queue:
                    continue
                queue.append(neighbor)
                shortest_paths.append(shortest_paths[current] + [neighbor])
            current += 1

        return path

    def connectTeamPoints(self, start_point):
        path = []
        queue = [start_point]
        shortest_paths = [[start_point]]
        current = 0
        # Simple BFS
        while current < len(queue):
            current_point_pos = self.intermediate_points[queue[current]].pos
            current_point_radius = self.intermediate_points[queue[current]].radius
            target_point_pos = self.source_point.pos
            # if we can go straight to target -> do it
            if (current_point_pos[0] - target_point_pos[0]) ** 2 + (current_point_pos[1] - target_point_pos[1]) ** 2 <= current_point_radius ** 2:
                path = shortest_paths[current]
                break
            # if we cannot -> retrieve neighbor points
            neighbors = self.intermediate_points[queue[current]].getTeamNeighborsIndices(self.intermediate_points)
            for neighbor in neighbors:
                if neighbor in queue:
                    continue
                queue.append(neighbor)
                shortest_paths.append(shortest_paths[current] + [neighbor])
            current += 1

        return path

    def attack(self, idx1, idx2):
        if self.intermediate_points[idx2].is_master:
            return False
        pos1 = self.intermediate_points[idx1].pos
        pos2 = self.intermediate_points[idx2].pos
        if (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 > self.intermediate_points[idx1].radius ** 2:
            return False
        attack_force = max(self.intermediate_points[idx1].health - 1, 0)
        if self.intermediate_points[idx2].team != self.intermediate_points[idx1].team:
            real_attack = min(attack_force, self.intermediate_points[idx2].health)
            self.intermediate_points[idx2].health -= real_attack
            self.intermediate_points[idx1].health -= real_attack
            if self.intermediate_points[idx2].health == 0:
                self.intermediate_points[idx2].team = self.intermediate_points[idx1].team

        attack_force = max(self.intermediate_points[idx1].health - 1, 0)
        if self.intermediate_points[idx2].team == self.intermediate_points[idx1].team:
            self.intermediate_points[idx2].health += attack_force
            self.intermediate_points[idx1].health -= attack_force
        return True

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen_alpha = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.font_big = pygame.font.SysFont('couriernew', 40)
        self.font_med = pygame.font.SysFont('couriernew', 24)
        self.font_small = pygame.font.SysFont('couriernew', 12)
        self.clock = pygame.time.Clock()
        self.pause = False
        self.playerUpdateTime = time.time()

        self.background = Background()
        # the source point, each team want to download from
        self.source_point = SourcePoint(self.setPosition((self.WIDTH / 2, self.HEIGHT / 2)))

        self.intermediate_points = []
        # add destination point for each team
        self.intermediate_points.append(
            IntermediatePoint(
                self.setPosition((self.SAFE_RIGHT, self.SAFE_BOTTOM)),
                self.MAX_RADIUS,
                1,
                True))

        self.intermediate_points.append(
            IntermediatePoint(
                self.setPosition((self.SAFE_LEFT, self.SAFE_BOTTOM)),
                self.MAX_RADIUS,
                2,
                True))

        self.intermediate_points.append(
            IntermediatePoint(
                self.setPosition((self.SAFE_LEFT, self.SAFE_TOP)),
                self.MAX_RADIUS,
                3,
                True))

        self.intermediate_points.append(
            IntermediatePoint(
                self.setPosition((self.SAFE_RIGHT, self.SAFE_TOP)),
                self.MAX_RADIUS,
                4,
                True))

        # add points, until we connect source and dest
        while len(self.connectPoints(0)) == 0:
            self.intermediate_points.append(
                IntermediatePoint(self.generatePosition(), random.randrange(self.MIN_RADIUS, self.MAX_RADIUS)))

        while len(self.connectPoints(1)) == 0:
            self.intermediate_points.append(
                IntermediatePoint(self.generatePosition(), random.randrange(self.MIN_RADIUS, self.MAX_RADIUS)))

        while len(self.connectPoints(2)) == 0:
            self.intermediate_points.append(
                IntermediatePoint(self.generatePosition(), random.randrange(self.MIN_RADIUS, self.MAX_RADIUS)))

        while len(self.connectPoints(3)) == 0:
            self.intermediate_points.append(
                IntermediatePoint(self.generatePosition(), random.randrange(self.MIN_RADIUS, self.MAX_RADIUS)))

        # generate additional points
        for i in range(self.ADDITIONAL_POINTS):
            self.intermediate_points.append(IntermediatePoint(self.generatePosition(), random.randrange(self.MIN_RADIUS, self.MAX_RADIUS)))

        self.whoWon = None

    def update(self):
        if self.pause:
            return
        self.background.update()

        # check if someone Won
        if self.whoWon == None:
            for i in range(len(self.PLAYERS)):
                if self.PLAYERS[i].isWon():
                    self.whoWon = i

        if self.whoWon != None:
            return

        # update health
        self.source_point.update()
        for i in range(len(self.intermediate_points)):
            self.intermediate_points[i].unmarkActive()
            self.intermediate_points[i].update()

        # update input
        for i in range(len(self.PLAYERS)):
            if self.PLAYERS[i].update(self.intermediate_points):
                self.intermediate_points[self.PLAYERS[i].fromIdx].markActive()
            if self.PLAYERS[i].fast:
                decision = self.PLAYERS[i].decide(self.intermediate_points)
                if decision != None:
                    self.PLAYERS[i].decision = decision
                    self.attack(decision[0], decision[1])
                    self.intermediate_points[decision[0]].attack(self.intermediate_points[decision[1]].pos, i + 1)


        # update Players decisions
        if time.time() - self.playerUpdateTime > 1:
            for i in range(len(self.PLAYERS)):
                decision = self.PLAYERS[i].decide(self.intermediate_points)
                if decision != None:
                    self.PLAYERS[i].decision = decision
                    self.attack(decision[0], decision[1])
                    self.intermediate_points[decision[0]].attack(self.intermediate_points[decision[1]].pos, i + 1)
            self.playerUpdateTime = time.time()
        else: # keep attack on screen
            for i in range(len(self.PLAYERS)):
                if self.PLAYERS[i].decision != None:
                    self.intermediate_points[self.PLAYERS[i].decision[0]].attack(self.intermediate_points[self.PLAYERS[i].decision[1]].pos, i + 1)

        # check for each player -> if it is connected to source
        for i in range(len(self.PLAYERS)):
            # draw path
            path = self.connectTeamPoints(i)
            if len(path) > 0:
                for j in range(len(path) - 1):
                    self.intermediate_points[path[j]].connect(self.intermediate_points[path[j + 1]].pos)
                self.intermediate_points[path[-1]].connect(self.source_point.pos)
                # send 1 message
                self.PLAYERS[i].sendAndReceiveMsg()

    def draw(self):
        self.background.draw(self.screen)
        self.screen_alpha.fill((0, 0, 0, 0))

        for i in range(len(self.intermediate_points)):
            self.intermediate_points[i].drawConnections(self.screen_alpha, self.font_small)

        self.source_point.draw(self.screen_alpha)

        for i in range(len(self.intermediate_points)):
            self.intermediate_points[i].draw(self.screen_alpha, self.font_small)

        # for each player also draw their progress
        for i in range(len(self.PLAYERS)):
            text = self.font_small.render(str(self.PLAYERS[i].progress()) + "%", True, (255, 255, 255))
            self.screen_alpha.blit(text, (self.intermediate_points[i].pos[0] - 10, self.intermediate_points[i].pos[1] - 20))

        self.screen.blit(self.screen_alpha, (0, 0))

        if self.pause:
            self.screen.fill((0, 0, 0, 0), (640 - 70, 360 - 25, 170, 50))
            text = self.font_big.render("Paused", True, (255, 255, 255))
            self.screen.blit(text, (640 - 60, 360 - 25))

        if self.whoWon != None:
            self.screen.fill((0, 0, 0, 0), (640 - 150, 360 - 25, 310, 50))
            text = self.font_big.render("Player " + str(self.whoWon) + " won!", True, (255, 255, 255))
            self.screen.blit(text, (640 - 150, 360 - 25) )


    def run(self):
        while True:
            # process input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause
            # update
            self.update()
            # draw
            self.draw()
            # flip screen
            pygame.display.flip()
            # 30 fps
            self.clock.tick(30)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = Game()
    game.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
