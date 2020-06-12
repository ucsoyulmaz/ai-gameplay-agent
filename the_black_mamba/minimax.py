from random import shuffle
import copy
from collections import Counter

max_value_global = float("-inf")

class Minimax:

    # *********************************************************************************************************************
    # *********************************************************************************************************************
    def __init__(self, max_depth, player_color, data_set, state, score):

        # global max_value for alpha beta pruning --> this is the benchmark point
        global max_value_global
        max_value_global = float("-inf")

        # the variables which we need inside self
        self.max_depth = max_depth
        self.player_color = player_color
        self._ALL_SQUARES = {(x, y) for x in range(8) for y in range(8)}
        self.state = state
        self.data_set = data_set
        self.score = score

    # *********************************************************************************************************************
    # *********************************************************************************************************************


    # *********************************************************************************************************************
    # *********************************************************************************************************************
    # this function is responsible for making decision among all the possible move actions
    def minimax_decision(self, state, data, max_depth, score, turn_color):



        global max_value_global
        action_utilities = []       # this array is responsible for storing the final utility values of each action
        data_copy = copy.deepcopy(data)

        # Getting all the possible actions that the player can apply
        if turn_color == "white":
            opponent_color = "black"

        elif turn_color == "black":
            opponent_color = "white"

        max_location = self.find_max_location(data_copy, opponent_color)
        data_copy = copy.deepcopy(data)
        all_possible_actions = self.find_all_possible_actions(data_copy, turn_color, max_location["x_location"], max_location["y_location"])

        # if you want to play aggressively, make it 1. For passive play, make it 0.
        is_offensive = 1

        if is_offensive == 1:
            all_possible_actions.sort(key=self.take_distance_as_sorting_parameter)

        elif is_offensive == 0:
            shuffle(all_possible_actions)       # Shuffling the array to be fair

        state_copy = copy.deepcopy(state)
        max_depth_copy = copy.deepcopy(max_depth)
        score_copy = copy.deepcopy(score)
        data_copy = copy.deepcopy(data)
        turn_color_copy = copy.deepcopy(turn_color)

        # FOR EACH ITEM IN THE ALL_POSSIBLE_ACTIONS ARRAY
        for item in all_possible_actions:

            # Imitating each action and getting the final state, data and scores
            state_new, data_new, score_new = self.imitate_action(state_copy, data_copy, score_copy, item["action_sentence"], turn_color)

            #--------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------
            # Checking whether this particular action of the player decreases his score or not
            is_bad_action = 0
            if turn_color_copy == "white":
                if (score_new["white"] - score_new["black"]) < (score_copy["white"] - score_copy["black"]):
                    if score_new["white"] > 0 and score_new["black"] == 0:
                        is_bad_action = 0
                    else:
                        is_bad_action = 1

            elif turn_color_copy == "black":
                if (score_new["black"] - score_new["white"]) < (score_copy["black"] - score_copy["white"]):
                    if score_new["black"] > 0 and score_new["white"] == 0:
                        is_bad_action = 0
                    else:
                        is_bad_action = 1
            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------


            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------
            # if the action does not cause any score lose, take it in consideration.
            if is_bad_action == 0:

                # If there is a winner action, do not continue --> just return it
                if self.player_color == "white":
                    if score_new["black"] == 0 and score_new["white"] > 0:
                        return float('inf'), item["action_sentence"]

                elif self.player_color == "black":
                    if score_new["white"] == 0 and score_new["black"] > 0:
                        return float('inf'), item["action_sentence"]


                # Changing the color for the next turn
                new_turn_color = turn_color_copy  # just some value here

                if turn_color_copy == "white":
                    new_turn_color = "black"

                elif turn_color_copy == "black":
                    new_turn_color = "white"

                # Calling minimax_exc function which returns a utility value and scores of both players
                utility_value, score_own, score_opponent = self.minimax_exec(state_new, data_new, max_depth_copy - 1, score_new, new_turn_color)

                # Add the required fields into action_utilies array
                action_utilities.append({"action": item["action_sentence"], "utility": utility_value, "score_own": score_own, "score_opponent": score_opponent})

                # Alpha - beta pruning here
                if max_value_global > utility_value:
                    return float('-inf'), item["action_sentence"]

            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------


        if len(action_utilities) == 0:
            return float('-inf'), "NONE"


        # --------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------
        # For the case that we reach to the max_depth and we need to return the min value
        if max_depth_copy == 1:
            min_utility = action_utilities[0]["utility"]
            min_action = action_utilities[0]["action"]

            for item in action_utilities:
                if min_utility > item["utility"]:
                    min_utility = item["utility"]
                    min_action = item["action"]

            return min_utility, min_action

        # For the case that we haven't reached to the max_depth and we need to return the max value
        else:
            max_utility = action_utilities[0]["utility"]
            max_action = action_utilities[0]["action"]
            max_action_lowest_opponent_score = action_utilities[0]["score_opponent"]
            max_value_global = copy.deepcopy(max_utility)

            for item in action_utilities:
                if max_utility <= item["utility"]:
                    if max_utility == item["utility"]:
                        if item["action"][0] == "MOVE" and max_action[0] == "MOVE":
                            if max_action[2] == item["action"][2] and max_action[3] == item["action"][3]:
                                if max_action[1] < item["action"][1]:
                                    max_action = item["action"]
                        else:
                            if max_action_lowest_opponent_score > item["score_opponent"]:
                                score_difference = 0
                                if turn_color_copy == "white":
                                    score_difference = item["score_own"] - item["score_opponent"]

                                elif turn_color_copy == "black":
                                    score_difference = item["score_own"] - item["score_opponent"]

                                if score_difference >= 0:
                                    max_utility = item["utility"]
                                    max_action = item["action"]
                                    max_action_lowest_opponent_score = item["score_opponent"]

                    else:
                        max_utility = item["utility"]
                        max_action = item["action"]
                        max_action_lowest_opponent_score = item["score_opponent"]

                    if max_value_global < max_utility:
                        max_value_global = max_utility

            return max_utility, max_action
        # --------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------

    # *********************************************************************************************************************
    # *********************************************************************************************************************

    # *********************************************************************************************************************
    # *********************************************************************************************************************

    def minimax_exec(self, state, data, max_depth, score, turn_color):

        if max_depth == 0:
            if turn_color == "white":
                utility = score["white"] - score["black"]
                return utility, score["white"], score["black"]
            elif turn_color == "black":
                utility = score["black"] - score["white"]
                return utility, score["black"], score["white"]

        if turn_color == "white":
            if score["black"] == 0 and score["white"] > 0:
                utility = score["white"] - score["black"]
                return utility, score["white"], score["black"]

        elif turn_color == "black":
            if score["white"] == 0 and score["black"] > 0:
                utility = score["black"] - score["white"]
                return utility, score["black"], score["white"]

        data_copy = copy.deepcopy(data)
        state_copy = copy.deepcopy(state)
        max_depth_copy = copy.deepcopy(max_depth)
        score_copy = copy.deepcopy(score)
        turn_color_copy = copy.deepcopy(turn_color)

        if turn_color == "white":
            utility, action = self.minimax_decision(state_copy, data_copy, max_depth_copy, score_copy, turn_color_copy)
            return utility, score_copy["white"], score_copy["black"]

        elif turn_color == "black":
            utility, action = self.minimax_decision(state_copy, data_copy, max_depth_copy, score_copy, turn_color_copy)
            return utility, score_copy["white"], score_copy["white"]

    # *********************************************************************************************************************
    # *********************************************************************************************************************


    # *********************************************************************************************************************
    # *********************************************************************************************************************


    def execute(self):
        state_copy = copy.deepcopy(self.state)
        data_copy = copy.deepcopy(self.data_set)
        max_depth_copy = copy.deepcopy(self.max_depth)
        score_copy = copy.deepcopy(self.score)
        player_color_copy = self.player_color
        utility, action = self.minimax_decision(state_copy, data_copy, max_depth_copy, score_copy, player_color_copy)

        print("Final Utility: ", utility, "--- action: ", action)
        return action

    # *********************************************************************************************************************
    # *********************************************************************************************************************

    # *********************************************************************************************************************
    # *********************************************************************************************************************
    def imitate_action(self, state, data, score, action, turn_color):

        atype, *aargs = action

        if atype == "MOVE":
            amount, start_coordinates, end_coordinates = aargs
            start_x_coordinate = start_coordinates[0]
            start_y_coordinate = start_coordinates[1]
            end_x_coordinate = end_coordinates[0]
            end_y_coordinate = end_coordinates[1]
            data_temp = copy.deepcopy(data)
            data = self.move_on_json(data_temp, amount, start_x_coordinate, start_y_coordinate,
                                              end_x_coordinate, end_y_coordinate, turn_color)
            state = self.json_to_state_converter(data)

        elif atype == "BOOM":
            coordinates = aargs
            x_coordinate = coordinates[0][0]
            y_coordinate = coordinates[0][1]
            data_temp = copy.deepcopy(data)
            data = self.boom_on_json(data_temp, x_coordinate, y_coordinate)
            state = self.json_to_state_converter(data)

            score_white = 0
            score_black = 0

            for item in data["white"]:
                score_white = score_white + item[0]
            for item in data["black"]:
                score_black = score_black + item[0]

            score = {'white': score_white, 'black': score_black}

        return state, data, score

    # *********************************************************************************************************************
    # *********************************************************************************************************************

    # *********************************************************************************************************************
    # *********************************************************************************************************************
    def find_all_possible_actions(self, data, turn_color, x_central, y_central):
        all_possible_moves = []

        array_to_lookup = []
        if turn_color == "white":
            array_to_lookup = data["white"]
        elif turn_color == "black":
            array_to_lookup = data["black"]

        for item in array_to_lookup:
            for index in range(item[0]):

                amount = index + 1

                for spaces in range(item[0]):
                    number_of_spaces = spaces + 1

                    data_copy = copy.deepcopy(data)
                    action_check = self.move_on_json(data_copy, amount, item[1], item[2], item[1],
                                                     item[2] - number_of_spaces, turn_color)
                    if action_check['white'][0][0] != -1:
                        action_sentence = ("MOVE", amount, (item[1], item[2]), (item[1], item[2] - number_of_spaces))
                        all_possible_moves.append({"action_sentence": action_sentence,
                                                   "distance": abs(item[1] - x_central) + abs(
                                                       item[2] - number_of_spaces - y_central)})

                    data_copy = copy.deepcopy(data)
                    action_check = self.move_on_json(data_copy, amount, item[1], item[2], item[1] + number_of_spaces,
                                                     item[2], turn_color)
                    if action_check['white'][0][0] != -1:
                        action_sentence = ("MOVE", amount, (item[1], item[2]), (item[1] + number_of_spaces, item[2]))
                        all_possible_moves.append({"action_sentence": action_sentence,
                                                   "distance": abs(item[1] + number_of_spaces - x_central) + abs(
                                                       item[2] - y_central)})

                    data_copy = copy.deepcopy(data)
                    action_check = self.move_on_json(data_copy, amount, item[1], item[2], item[1],
                                                     item[2] + number_of_spaces, turn_color)
                    if action_check['white'][0][0] != -1:
                        action_sentence = ("MOVE", amount, (item[1], item[2]), (item[1], item[2] + number_of_spaces))
                        all_possible_moves.append({"action_sentence": action_sentence,
                                                   "distance": abs(item[1] - x_central) + abs(
                                                       item[2] + number_of_spaces - y_central)})

                    data_copy = copy.deepcopy(data)
                    action_check = self.move_on_json(data_copy, amount, item[1], item[2], item[1] - number_of_spaces,
                                                     item[2], turn_color)
                    if action_check['white'][0][0] != -1:
                        action_sentence = ("MOVE", amount, (item[1], item[2]), (item[1] - number_of_spaces, item[2]))
                        all_possible_moves.append({"action_sentence": action_sentence,
                                                   "distance": abs(item[1] - number_of_spaces - x_central) + abs(
                                                       item[2] - y_central)})

            action_sentence = ("BOOM", (item[1], item[2]))
            all_possible_moves.append({"action_sentence": action_sentence, "distance": 0})

        return all_possible_moves

    # *********************************************************************************************************************
    # *********************************************************************************************************************


    # *********************************************************************************************************************
    # *********************************************************************************************************************
    def json_to_state_converter(self, data_temp):
        state_temp = Counter({xy: 0 for xy in self._ALL_SQUARES})

        for item in data_temp['white']:
            state_temp[(item[1], item[2])] = item[0]

        for item in data_temp['black']:
            state_temp[(item[1], item[2])] = -item[0]

        return state_temp
    # *********************************************************************************************************************
    # *********************************************************************************************************************

    # *********************************************************************************************************************
    # *********************************************************************************************************************
    def move_on_json(self, data, n, x_a, y_a, x_b, y_b, colour):

        if x_b > 7 or x_b < 0 or y_b > 7 or y_b < 0:
            # print('invalid move: Move out of board')
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

    # *********************************************************************************************************************
    # *********************************************************************************************************************


    # *********************************************************************************************************************
    # *********************************************************************************************************************
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
                    data_temp = self.boom_on_json(data_temp, (x_a - 1), (y_a - 1))

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

    # *********************************************************************************************************************
    # *********************************************************************************************************************

    # *********************************************************************************************************************
    # *********************************************************************************************************************
    def find_max_location(self, data_node, opponent_color):

        max_values = {opponent_color: 0, 'x_location': -1, 'y_location': -1, 'data_set_after_boom': {}}

        for item in data_node[opponent_color]:

            # ----------------------------------------------------------------------------------------------
            count = {opponent_color: 0, 'x_location': item[1] - 1, 'y_location': item[2] - 1}
            new_json = self.boom_on_json(data_node, item[1] - 1, item[2] - 1)

            if len(new_json) != 0:
                if len(data_node[opponent_color]) > len(new_json[opponent_color]):
                    for item_data_node in data_node[opponent_color]:
                        is_this_item_missing = 1
                        for item_new_json in new_json[opponent_color]:
                            if item_data_node == item_new_json:
                                is_this_item_missing = 0
                        if is_this_item_missing == 1:
                            count[opponent_color] = count[opponent_color] + item_data_node[0]

                if max_values[opponent_color] < count[opponent_color]:
                    max_values[opponent_color] = count[opponent_color]
                    max_values['x_location'] = count['x_location']
                    max_values['y_location'] = count['y_location']
                    max_values['data_set_after_boom'] = new_json

            # ----------------------------------------------------------------------------------------------

            count = {opponent_color: 0, 'x_location': item[1], 'y_location': item[2] - 1}
            new_json = self.boom_on_json(data_node, item[1], item[2] - 1)

            if len(new_json) != 0:
                if len(data_node[opponent_color]) > len(new_json[opponent_color]):
                    for item_data_node in data_node[opponent_color]:
                        is_this_item_missing = 1
                        for item_new_json in new_json[opponent_color]:
                            if item_data_node == item_new_json:
                                is_this_item_missing = 0
                        if is_this_item_missing == 1:
                            count[opponent_color] = count[opponent_color] + item_data_node[0]

                if max_values[opponent_color] < count[opponent_color]:
                    max_values[opponent_color] = count[opponent_color]
                    max_values['x_location'] = count['x_location']
                    max_values['y_location'] = count['y_location']
                    max_values['data_set_after_boom'] = new_json

            # ----------------------------------------------------------------------------------------------

            count = {opponent_color: 0, 'x_location': item[1] + 1, 'y_location': item[2] - 1}
            new_json = self.boom_on_json(data_node, item[1] + 1, item[2] - 1)

            if len(new_json) != 0:
                if len(data_node[opponent_color]) > len(new_json[opponent_color]):
                    for item_data_node in data_node[opponent_color]:
                        is_this_item_missing = 1
                        for item_new_json in new_json[opponent_color]:
                            if item_data_node == item_new_json:
                                is_this_item_missing = 0
                        if is_this_item_missing == 1:
                            count[opponent_color] = count[opponent_color] + item_data_node[0]

                if max_values[opponent_color] < count[opponent_color]:
                    max_values[opponent_color] = count[opponent_color]
                    max_values['x_location'] = count['x_location']
                    max_values['y_location'] = count['y_location']
                    max_values['data_set_after_boom'] = new_json

            # ----------------------------------------------------------------------------------------------

            count = {opponent_color: 0, 'x_location': item[1] - 1, 'y_location': item[2]}
            new_json = self.boom_on_json(data_node, item[1] - 1, item[2])

            if len(new_json) != 0:
                if len(data_node[opponent_color]) > len(new_json[opponent_color]):
                    for item_data_node in data_node[opponent_color]:
                        is_this_item_missing = 1
                        for item_new_json in new_json[opponent_color]:
                            if item_data_node == item_new_json:
                                is_this_item_missing = 0
                        if is_this_item_missing == 1:
                            count[opponent_color] = count[opponent_color] + item_data_node[0]

                if max_values[opponent_color] < count[opponent_color]:
                    max_values[opponent_color] = count[opponent_color]
                    max_values['x_location'] = count['x_location']
                    max_values['y_location'] = count['y_location']
                    max_values['data_set_after_boom'] = new_json

            # ----------------------------------------------------------------------------------------------

            count = {opponent_color: 0, 'x_location': item[1] + 1, 'y_location': item[2]}
            new_json = self.boom_on_json(data_node, item[1] + 1, item[2])

            if len(new_json) != 0:
                if len(data_node[opponent_color]) > len(new_json[opponent_color]):
                    for item_data_node in data_node[opponent_color]:
                        is_this_item_missing = 1
                        for item_new_json in new_json[opponent_color]:
                            if item_data_node == item_new_json:
                                is_this_item_missing = 0
                        if is_this_item_missing == 1:
                            count[opponent_color] = count[opponent_color] + item_data_node[0]

                if max_values[opponent_color] < count[opponent_color]:
                    max_values[opponent_color] = count[opponent_color]
                    max_values['x_location'] = count['x_location']
                    max_values['y_location'] = count['y_location']
                    max_values['data_set_after_boom'] = new_json

            # ----------------------------------------------------------------------------------------------

            count = {opponent_color: 0, 'x_location': item[1] - 1, 'y_location': item[2] + 1}
            new_json = self.boom_on_json(data_node, item[1] - 1, item[2] + 1)

            if len(new_json) != 0:
                if len(data_node[opponent_color]) > len(new_json[opponent_color]):
                    for item_data_node in data_node[opponent_color]:
                        is_this_item_missing = 1
                        for item_new_json in new_json[opponent_color]:
                            if item_data_node == item_new_json:
                                is_this_item_missing = 0
                        if is_this_item_missing == 1:
                            count[opponent_color] = count[opponent_color] + item_data_node[0]

                if max_values[opponent_color] < count[opponent_color]:
                    max_values[opponent_color] = count[opponent_color]
                    max_values['x_location'] = count['x_location']
                    max_values['y_location'] = count['y_location']
                    max_values['data_set_after_boom'] = new_json

            # ----------------------------------------------------------------------------------------------

            count = {opponent_color: 0, 'x_location': item[1], 'y_location': item[2] + 1}
            new_json = self.boom_on_json(data_node, item[1], item[2] + 1)

            if len(new_json) != 0:
                if len(data_node[opponent_color]) > len(new_json[opponent_color]):
                    for item_data_node in data_node[opponent_color]:
                        is_this_item_missing = 1
                        for item_new_json in new_json[opponent_color]:
                            if item_data_node == item_new_json:
                                is_this_item_missing = 0
                        if is_this_item_missing == 1:
                            count[opponent_color] = count[opponent_color] + item_data_node[0]

                if max_values[opponent_color] < count[opponent_color]:
                    max_values[opponent_color] = count[opponent_color]
                    max_values['x_location'] = count['x_location']
                    max_values['y_location'] = count['y_location']
                    max_values['data_set_after_boom'] = new_json

            # ----------------------------------------------------------------------------------------------

            count = {opponent_color: 0, 'x_location': item[1] + 1, 'y_location': item[2] + 1}
            new_json = self.boom_on_json(data_node, item[1] + 1, item[2] + 1)

            if len(new_json) != 0:
                if len(data_node[opponent_color]) > len(new_json[opponent_color]):
                    for item_data_node in data_node[opponent_color]:
                        is_this_item_missing = 1
                        for item_new_json in new_json[opponent_color]:
                            if item_data_node == item_new_json:
                                is_this_item_missing = 0
                        if is_this_item_missing == 1:
                            count[opponent_color] = count[opponent_color] + item_data_node[0]

                if max_values[opponent_color] < count[opponent_color]:
                    max_values[opponent_color] = count[opponent_color]
                    max_values['x_location'] = count['x_location']
                    max_values['y_location'] = count['y_location']
                    max_values['data_set_after_boom'] = new_json

            # ----------------------------------------------------------------------------------------------

        return max_values

    # *********************************************************************************************************************
    # *********************************************************************************************************************

    # *********************************************************************************************************************
    # *********************************************************************************************************************
    # take second element for sort
    def take_distance_as_sorting_parameter(self, elem):
        return elem['distance']
    # *********************************************************************************************************************
    # *********************************************************************************************************************