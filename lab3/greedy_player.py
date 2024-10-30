import random
import SRP


class GreedyPlayer:
    def __init__(self, team):
        self.team = team
        self.SRP_reciever = SRP.SRPReceiver()
        self.SRP_sender = SRP.SRPSender()
        self.decision = None
        self.fast = False

    def isWon(self):
        return self.SRP_sender.isDone()

    def progress(self):
        if self.isWon():
            return 100
        else:
            return int(100 * self.SRP_sender.ans_count / (self.SRP_sender.max_number + 1))

    def decide(self, intermediate_points):
        possible_moves = []
        # get list of possible targets
        for i in range(len(intermediate_points)):
            if intermediate_points[i].team == self.team:
                neighbors = intermediate_points[i].getNeighborsIndices(intermediate_points)
                for neighbor in neighbors:
                    if intermediate_points[neighbor].team != self.team:
                        possible_moves.append((i, neighbor))

        return possible_moves[0]

    def sendAndReceiveMsg(self):
        # send one message to each other
        if self.SRP_sender.send_msg_queue.has_msg():
            self.SRP_reciever.recieve_msg_queue.send_message(self.SRP_sender.send_msg_queue.get_message())
        if self.SRP_reciever.send_msg_queue.has_msg():
            self.SRP_sender.recieve_msg_queue.send_message(self.SRP_reciever.send_msg_queue.get_message())

    def update(self, intermediate_points):
        # update receiver
        self.SRP_sender.update()
        self.SRP_reciever.update()
        return False
