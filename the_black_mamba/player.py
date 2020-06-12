
import time
from collections import Counter
import copy
from the_black_mamba.minimax import Minimax


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
        for xy in self._WHITE_SQUARES:
            self.state[xy] = +1
        for xy in self._BLACK_SQUARES:
            self.state[xy] = -1

        self.data_set = self.state_to_json_converter()
        self.counter = 0

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """

        if self.my_colour == "white":
            actions = [("MOVE",1,(1,1),(0,1)),("MOVE",1,(4,1),(3,1)), ("MOVE",1,(6,1),(7,1))]

        elif self.my_colour == "black":
            actions = [("MOVE", 1, (6, 6), (7,6)), ("MOVE", 1, (3, 6), (4, 6)), ("MOVE", 1, (0, 6), (1, 6))]

        if self.counter < len(actions):
            data_copy = copy.deepcopy(self.data_set)
            self.counter = self.counter + 1

            result = self.move_on_json_check(data_copy,actions[self.counter - 1][1], actions[self.counter - 1][2][0],
                                 actions[self.counter - 1][2][1], actions[self.counter - 1][3][0],
                                 actions[self.counter - 1][3][1], self.my_colour)

            if result["white"][0][0] != -1:
                return actions[self.counter - 1]
            else:
                self.counter = len(actions)

        if self.counter >= len(actions):
            if self.score["white"] + self.score["black"] <= 3:
                ai_agent = Minimax(max_depth=6, player_color=self.my_colour, data_set=self.data_set,
                                   state=self.state, score=self.score)
            else:
                if (self.score["white"] + self.score["black"] < 8) and (self.score["white"] + self.score["black"] >= 4):
                    ai_agent = Minimax(max_depth=4, player_color=self.my_colour, data_set=self.data_set,
                                       state=self.state, score=self.score)
                else:
                    ai_agent = Minimax(max_depth=2, player_color=self.my_colour, data_set=self.data_set, state=self.state,
                                   score=self.score)
            action = Minimax.execute(ai_agent)
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

        if atype == "MOVE":
            amount, start_coordinates, end_coordinates = aargs

            start_x_coordinate = start_coordinates[0]
            start_y_coordinate = start_coordinates[1]
            end_x_coordinate = end_coordinates[0]
            end_y_coordinate = end_coordinates[1]
            self.data_set = self.state_to_json_converter()
            data_temp = copy.deepcopy(self.data_set)
            self.data_set = self.move_on_json(data_temp, amount, start_x_coordinate, start_y_coordinate,
                                              end_x_coordinate, end_y_coordinate, colour)
            self.state = self.json_to_state_converter()

        elif atype == "BOOM":
            coordinates = aargs
            x_coordinate = coordinates[0][0]
            y_coordinate = coordinates[0][1]
            self.data_set = self.state_to_json_converter()
            data_temp = copy.deepcopy(self.data_set)
            self.data_set = self.boom_on_json(data_temp, x_coordinate, y_coordinate)
            self.state = self.json_to_state_converter()

            score_white = 0
            score_black = 0

            for item in self.data_set["white"]:
                score_white = score_white + item[0]
            for item in self.data_set["black"]:
                score_black = score_black + item[0]

            self.score = {'white': score_white, 'black': score_black}

    def state_to_json_converter(self):

        data_temp = {'white': [], 'black': []}

        for x in range(8):
            for y in range(8):
                if self.state[(x, y)] != 0:
                    if self.state[(x, y)] > 0:
                        data_temp['white'].append([self.state[(x, y)], x, y])
                    else:
                        data_temp['black'].append([(-self.state[(x, y)]), x, y])

        return data_temp

    def json_to_state_converter(self):
        state_temp = Counter({xy: 0 for xy in self._ALL_SQUARES})

        for item in self.data_set['white']:
            state_temp[(item[1], item[2])] = item[0]

        for item in self.data_set['black']:
            state_temp[(item[1], item[2])] = -item[0]

        return state_temp

    def move_on_json(self, data, n, x_a, y_a, x_b, y_b, colour):

        if x_b > 7 or x_b < 0 or y_b > 7 or y_b < 0:
            #print('invalid move: Move out of board')
            null_board = {'white': [], 'black': []}
            null_board['white'].append([-1, -1, -1])
            null_board['black'].append([-1, -1, -1])
            return null_board

        current_position_count = 0
        current_position_color = ''
        target_position_count = 0
        target_position_color = ''

        for item in data['white']:
            if x_a == item[1] and y_a == item[2]:
                current_position_count = item[0]
                current_position_color = 'W'
            if x_b == item[1] and y_b == item[2]:
                target_position_count = item[0]
                target_position_color = 'W'

        for item in data['black']:
            if x_a == item[1] and y_a == item[2]:
                current_position_count = item[0]
                current_position_color = 'B'
            if x_b == item[1] and y_b == item[2]:
                target_position_count = item[0]
                target_position_color = 'B'

        # Check valid move: Move more piece than piece
        if current_position_count < n:
            # print('invalid move: Move more than allowed,N')
            null_board = {'white': [], 'black': []}
            null_board['white'].append([-1, -1, -1])
            null_board['black'].append([-1, -1, -1])
            return null_board
        # Check valid move: Move more than piece in stack
        if abs(x_a - x_b) > current_position_count:
            # print('invalid move: Move more than allowed,X')
            null_board = {'white': [], 'black': []}
            null_board['white'].append([-1, -1, -1])
            null_board['black'].append([-1, -1, -1])
            return null_board
        if abs(y_a - y_b) > current_position_count:
            # print('invalid move: Move more than allowed,Y')
            null_board = {'white': [], 'black': []}
            null_board['white'].append([-1, -1, -1])
            null_board['black'].append([-1, -1, -1])
            return null_board
        # Check valid move: Collision
        if current_position_color != target_position_color and target_position_color != '':
            # print('invalid move: Collision,Color')
            null_board = {'white': [], 'black': []}
            null_board['white'].append([-1, -1, -1])
            null_board['black'].append([-1, -1, -1])
            return null_board

        # temporary variable for json object to be returned
        data_temp = {'white': [], 'black': []}

        is_new_position_occupied = 0
        number_of_tokens_on_new_position = 0

        if colour == "white":
            for item in data['white']:
                if item[1] == x_b and item[2] == y_b:
                    number_of_tokens_on_new_position = item[0]
                    is_new_position_occupied = 1

            for item in data['white']:
                if item[1] == x_a and item[2] == y_a:
                    if (item[0] - n) > 0:
                        data_temp['white'].append([(item[0] - n), x_a, y_a])
                else:
                    if item[1] != x_b or item[2] != y_b:
                        data_temp['white'].append([item[0], item[1], item[2]])

            if is_new_position_occupied == 1:
                data_temp['white'].append([(number_of_tokens_on_new_position + n), x_b, y_b])
            else:
                data_temp['white'].append([n, x_b, y_b])

            self.state[tuple([x_a, y_a])] -= n
            self.state[tuple([x_b, y_b])] += n
            data_temp['black'] = data['black']

        elif colour == "black":
            for item in data['black']:
                if item[1] == x_b and item[2] == y_b:
                    number_of_tokens_on_new_position = item[0]
                    is_new_position_occupied = 1

            for item in data['black']:
                if item[1] == x_a and item[2] == y_a:
                    if (item[0] - n) > 0:
                        data_temp['black'].append([(item[0] - n), x_a, y_a])
                else:
                    if item[1] != x_b or item[2] != y_b:
                        data_temp['black'].append([item[0], item[1], item[2]])

            if is_new_position_occupied == 1:
                data_temp['black'].append([(number_of_tokens_on_new_position + n), x_b, y_b])
            else:
                data_temp['black'].append([n, x_b, y_b])

            self.state[tuple([x_a, y_a])] += n
            self.state[tuple([x_b, y_b])] -= n
            data_temp['white'] = data['white']

        return data_temp

    def move_on_json_check(self, data, n, x_a, y_a, x_b, y_b, colour):

        if x_b > 7 or x_b < 0 or y_b > 7 or y_b < 0:
            #print('invalid move: Move out of board')
            null_board = {'white': [], 'black': []}
            null_board['white'].append([-1, -1, -1])
            null_board['black'].append([-1, -1, -1])
            return null_board

        current_position_count = 0
        current_position_color = ''
        target_position_count = 0
        target_position_color = ''

        for item in data['white']:
            if x_a == item[1] and y_a == item[2]:
                current_position_count = item[0]
                current_position_color = 'W'
            if x_b == item[1] and y_b == item[2]:
                target_position_count = item[0]
                target_position_color = 'W'

        for item in data['black']:
            if x_a == item[1] and y_a == item[2]:
                current_position_count = item[0]
                current_position_color = 'B'
            if x_b == item[1] and y_b == item[2]:
                target_position_count = item[0]
                target_position_color = 'B'

        # Check valid move: Move more piece than piece
        if current_position_count < n:
            # print('invalid move: Move more than allowed,N')
            null_board = {'white': [], 'black': []}
            null_board['white'].append([-1, -1, -1])
            null_board['black'].append([-1, -1, -1])
            return null_board
        # Check valid move: Move more than piece in stack
        if abs(x_a - x_b) > current_position_count:
            # print('invalid move: Move more than allowed,X')
            null_board = {'white': [], 'black': []}
            null_board['white'].append([-1, -1, -1])
            null_board['black'].append([-1, -1, -1])
            return null_board
        if abs(y_a - y_b) > current_position_count:
            # print('invalid move: Move more than allowed,Y')
            null_board = {'white': [], 'black': []}
            null_board['white'].append([-1, -1, -1])
            null_board['black'].append([-1, -1, -1])
            return null_board
        # Check valid move: Collision
        if current_position_color != target_position_color and target_position_color != '':
            # print('invalid move: Collision,Color')
            null_board = {'white': [], 'black': []}
            null_board['white'].append([-1, -1, -1])
            null_board['black'].append([-1, -1, -1])
            return null_board

        # temporary variable for json object to be returned
        data_temp = {'white': [], 'black': []}

        is_new_position_occupied = 0
        number_of_tokens_on_new_position = 0

        if colour == "white":
            for item in data['white']:
                if item[1] == x_b and item[2] == y_b:
                    number_of_tokens_on_new_position = item[0]
                    is_new_position_occupied = 1

            for item in data['white']:
                if item[1] == x_a and item[2] == y_a:
                    if (item[0] - n) > 0:
                        data_temp['white'].append([(item[0] - n), x_a, y_a])
                else:
                    if item[1] != x_b or item[2] != y_b:
                        data_temp['white'].append([item[0], item[1], item[2]])

            if is_new_position_occupied == 1:
                data_temp['white'].append([(number_of_tokens_on_new_position + n), x_b, y_b])
            else:
                data_temp['white'].append([n, x_b, y_b])

            data_temp['black'] = data['black']

        elif colour == "black":
            for item in data['black']:
                if item[1] == x_b and item[2] == y_b:
                    number_of_tokens_on_new_position = item[0]
                    is_new_position_occupied = 1

            for item in data['black']:
                if item[1] == x_a and item[2] == y_a:
                    if (item[0] - n) > 0:
                        data_temp['black'].append([(item[0] - n), x_a, y_a])
                else:
                    if item[1] != x_b or item[2] != y_b:
                        data_temp['black'].append([item[0], item[1], item[2]])

            if is_new_position_occupied == 1:
                data_temp['black'].append([(number_of_tokens_on_new_position + n), x_b, y_b])
            else:
                data_temp['black'].append([n, x_b, y_b])

            data_temp['white'] = data['white']

        return data_temp

    def boom_on_json(self, data, x_a, y_a):

        data_temp = {'white': [], 'black': []}
        null_data = {}

        if x_a > 7 or x_a < 0 or y_a > 7 or y_a < 0:
            return null_data

        for item in data['white']:
            if item[1] != x_a or item[2] != y_a:
                data_temp['white'].append([item[0], item[1], item[2]])

        for item in data['black']:
            if item[1] != x_a or item[2] != y_a:
                data_temp['black'].append([item[0], item[1], item[2]])

        if x_a - 1 >= 0 and y_a - 1 >= 0:
            for item in data_temp['white']:
                if item[1] == (x_a - 1) and item[2] == (y_a - 1):
                    data_temp = self.boom_on_json(data_temp, (x_a - 1), (y_a - 1))

            for item in data_temp['black']:
                if item[1] == (x_a - 1) and item[2] == (y_a - 1):
                    data_temp = self.boom_on_json(data_temp,  (x_a - 1), (y_a - 1))

        if y_a - 1 >= 0:
            for item in data_temp['white']:
                if item[1] == x_a and item[2] == (y_a - 1):
                    data_temp = self.boom_on_json(data_temp, x_a, (y_a - 1))

            for item in data_temp['black']:
                if item[1] == x_a and item[2] == (y_a - 1):
                    data_temp = self.boom_on_json(data_temp, x_a, (y_a - 1))

        if x_a + 1 <= 7 and y_a - 1 >= 0:
            for item in data_temp['white']:
                if item[1] == (x_a + 1) and item[2] == (y_a - 1):
                    data_temp = self.boom_on_json(data_temp, (x_a + 1), (y_a - 1))

            for item in data_temp['black']:
                if item[1] == (x_a + 1) and item[2] == (y_a - 1):
                    data_temp = self.boom_on_json(data_temp, (x_a + 1), (y_a - 1))

        if x_a - 1 >= 0:
            for item in data_temp['white']:
                if item[1] == (x_a - 1) and item[2] == y_a:
                    data_temp = self.boom_on_json(data_temp, (x_a - 1), y_a)

            for item in data_temp['black']:
                if item[1] == (x_a - 1) and item[2] == y_a:
                    data_temp = self.boom_on_json(data_temp, (x_a - 1), y_a)

        if x_a + 1 <= 7:
            for item in data_temp['white']:
                if item[1] == (x_a + 1) and item[2] == y_a:
                    data_temp = self.boom_on_json(data_temp, (x_a + 1), y_a)

            for item in data_temp['black']:
                if item[1] == (x_a + 1) and item[2] == y_a:
                    data_temp = self.boom_on_json(data_temp, (x_a + 1), y_a)

        if x_a - 1 >= 0 and y_a + 1 <= 7:
            for item in data_temp['white']:
                if item[1] == (x_a - 1) and item[2] == (y_a + 1):
                    data_temp = self.boom_on_json(data_temp, (x_a - 1), (y_a + 1))

            for item in data_temp['black']:
                if item[1] == (x_a - 1) and item[2] == (y_a + 1):
                    data_temp = self.boom_on_json(data_temp, (x_a - 1), (y_a + 1))

        if y_a + 1 <= 7:
            for item in data_temp['white']:
                if item[1] == x_a and item[2] == (y_a + 1):
                    data_temp = self.boom_on_json(data_temp, x_a, (y_a + 1))

            for item in data_temp['black']:
                if item[1] == x_a and item[2] == (y_a + 1):
                    data_temp = self.boom_on_json(data_temp, x_a, (y_a + 1))

        if x_a + 1 <= 7 and y_a + 1 <= 7:
            for item in data_temp['white']:
                if item[1] == (x_a + 1) and item[2] == (y_a + 1):
                    data_temp = self.boom_on_json(data_temp, (x_a + 1), (y_a + 1))

            for item in data_temp['black']:
                if item[1] == (x_a + 1) and item[2] == (y_a + 1):
                    data_temp = self.boom_on_json(data_temp, (x_a + 1), (y_a + 1))

        return data_temp
