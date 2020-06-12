
import time
from collections import Counter
from copy import copy
from another_player.Minimax import Minimax


class ExamplePlayer:


    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (White or Black). The value will be one of the 
        strings "white" or "black" correspondingly.
        """
        # TODO: Set up state representation and your my_color.
        # Initiate the state
        if colour == "white":
            self.my_colour = "white"
        else:
            self.my_colour = "black"
        # Initiate the state
        self._ALL_SQUARES = {(x, y) for x in range(8) for y in range(8)}

        self._BLACK_SQUARES = [(0, 7), (1, 7), (3, 7), (4, 7), (6, 7), (7, 7), (0, 6), (1, 6), (3, 6), (4, 6), (6, 6),
                               (7, 6)]
        self._WHITE_SQUARES = [(0, 1), (1, 1), (3, 1), (4, 1), (6, 1), (7, 1), (0, 0), (1, 0), (3, 0), (4, 0), (6, 0),
                               (7, 0)]

        self.score = {'white': 12, 'black': 12}
        self.state = Counter({xy: 0 for xy in self._ALL_SQUARES})
        # White is positive number , Black is negative number
        for xy in self._WHITE_SQUARES:
            self.state[xy] = +1
        for xy in self._BLACK_SQUARES:
            self.state[xy] = -1


    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        # ("BOOM", (0, 0))
        # ("MOVE", n,(Xa, Ya),(Xb,Yb))
        # action = ("MOVE", 1,(0, 0),(0,1))
        # action = ("BOOM", (0, 0))
        action_type = input("Enter your action: MOVE OR BOOM: ")
        if action_type == "MOVE":
            amount = int(input("Amont to Move: "))
            from_square_X = int(input("From square X: "))
            from_square_Y = int(input("From square Y: "))
            to_square_X = int(input("Destination square X: "))
            to_square_Y = int(input("Destination square Y: "))
            action = ("MOVE", amount,(from_square_X,from_square_Y),(to_square_X,to_square_Y))
        elif action_type == "BOOM":
            boom_square_X = int(input("BOOM square X: "))
            boom_square_Y = int(input("BOOM square Y: "))
            action = ("BOOM", (boom_square_X, boom_square_Y))



        # self.ai_agent = Minimax(max_depth=1, player_color=self.my_colour)
        # action = self.ai_agent._available_actions(self,self.my_colour)[0]
        # action = self.ai_agent.choose_action(self)
        return action


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        # TODO: Update state representation in response to action.
        """
               Submit an action to the game for validation and application.
               If the action is not allowed, raise an InvalidActionException with
               a message describing allowed actions.
               Otherwise, apply the action to the game state.
               """

        atype, *aargs = action
        # ( action type, number of piece , current square  ,destination square)
        # ("MOVE", n,(Xa, Ya),(Xb,Yb))
        if atype == "MOVE":
            n, a, b = aargs
            n = -n if self.state[a] < 0 else n
            # move the piece
            self.state[a] -= n
            self.state[b] += n
        # ( atype,start_square)
        # ("BOOM", (0, 0))
        else:  # atype == "BOOM":
            start_square, = aargs
            to_boom = [start_square]
            for boom_square in to_boom:
                n = self.state[boom_square]
                self.score["white" if n > 0 else "black"] -= abs(n)
                self.state[boom_square] = 0
                for near_square in self._NEAR_SQUARES(boom_square):
                    if self.state[near_square] != 0:
                        to_boom.append(near_square)

        # Imitate BOOM action and return result of the boom as score

    def _NEAR_SQUARES(self, square):
        x, y = square
        return {(x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                (x - 1, y), (x + 1, y),
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)} & self._ALL_SQUARES

