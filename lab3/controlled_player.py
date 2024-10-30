import random

import pygame.mouse

import SRP


class ControlledPlayer:
    def __init__(self, team):
        self.team = team
        self.SRP_reciever = SRP.SRPReceiver()
        self.SRP_sender = SRP.SRPSender()
        self.fromIdx = -1
        self.toIdx = -1
        self.decision = None
        self.fast = True
        self.prev_state = False

    def isWon(self):
        return self.SRP_sender.isDone()

    def progress(self):
        if self.isWon():
            return 100
        else:
            return int(100 * self.SRP_sender.ans_count / (self.SRP_sender.max_number + 1))

    def update(self, intermediate_points):
        # update receiver
        self.SRP_sender.update()
        self.SRP_reciever.update()
        cur_state = pygame.mouse.get_pressed()[0]
        if self.prev_state == False and cur_state == True:
            pos = pygame.mouse.get_pos()
            clicked_points = [s for s in range(len(intermediate_points)) if intermediate_points[s].rect.collidepoint(pos)]
            if len(clicked_points) > 0:
                if self.fromIdx == -1 and intermediate_points[clicked_points[0]].team == self.team:
                    self.fromIdx = clicked_points[0]
                elif self.toIdx == -1 and clicked_points[0] != self.fromIdx:
                    self.toIdx = clicked_points[0]
        self.prev_state = cur_state
        return True


    def decide(self, intermediate_points):

        res = None
        if self.fromIdx != -1 and self.toIdx != -1:
            res = (self.fromIdx, self.toIdx)
            self.fromIdx = -1
            self.toIdx = -1

        return res

    def sendAndReceiveMsg(self):
        # send one message to each other
        if self.SRP_sender.send_msg_queue.has_msg():
            self.SRP_reciever.recieve_msg_queue.send_message(self.SRP_sender.send_msg_queue.get_message())
        if self.SRP_reciever.send_msg_queue.has_msg():
            self.SRP_sender.recieve_msg_queue.send_message(self.SRP_reciever.send_msg_queue.get_message())