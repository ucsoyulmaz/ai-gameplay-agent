from random import shuffle
import copy


class Minimax:
    # TODO: Optimise util_function
    # TODO: Optimise sorting Line 34

    def __init__(self, max_depth, player_color):

        self.max_depth = max_depth
        self.player_color = player_color
        self._ALL_SQUARES = {(x, y) for x in range(8) for y in range(8)}

    def choose_action(self, state):

        # Get Util score and selected action from current state
        eval_score, selected_action = self._minimax(0, state, True, float('-inf'), float('inf'))

        # Return selected action, list of possible action
        return selected_action

    # Return util function value and action
    def _minimax(self, current_depth, state, is_max_turn, alpha, beta):

        # Return score from util function if it hits max depth or the game is in terminal state
        if current_depth == self.max_depth or self.is_terminal(state):
            return self.util_function(state, self.player_color), ""

        # Get possible action
        available_action = self._available_actions(state, self.player_color)

        # There is no sort algorithm here, just random. If we figure out something we can do it
        shuffle(available_action)

        # Default value of best value is -inf if we want max and inf if we want min, so It get replace right away
        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = None

        # Do recursive for every branch node
        for action in available_action:
            new_state = self.imitate_action(state, action)

            # Recursive happen here, loop until max dept or termianl
            eval_child, action_child = self._minimax(current_depth + 1, new_state, not is_max_turn, alpha, beta)

            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_target = action
                # Alpha-beta prunning
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_target = action
                # Alpha-beta prunning
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        # Return util function value and action
        return best_value, action_target

    def imitate_action(self, state, action):
        atype, *aargs = action
        state_copy = copy.deepcopy(state)
        if atype == "MOVE":
            n, a, b = aargs
            n = -n if state_copy.state[a] < 0 else n
            # move the piece
            state_copy.state[a] -= n
            state_copy.state[b] += n
        else:  # atype == "BOOM":
            start_square, = aargs
            to_boom = [start_square]
            for boom_square in to_boom:
                n = state_copy.state[boom_square]
                state_copy.score["white" if n > 0 else "black"] -= abs(n)
                state_copy.state[boom_square] = 0
                for near_square in self._NEAR_SQUARES(boom_square):
                    if state_copy.state[near_square] != 0:
                        to_boom.append(near_square)
        return state_copy

    def _available_actions(self, state, colour):
        """
        A list of currently-available actions for a particular player
        (assists validation).
        """
        available_actions = []
        if colour == "white":
            stacks = +state.state
        else:
            stacks = -state.state
        for square in stacks.keys():
            available_actions.append(("BOOM", square))
        for square, n in stacks.items():
            for d in range(1, n + 1):
                for next_square in self._NEXT_SQUARES(square, d):
                    if next_square in stacks or state.state[next_square] == 0:
                        for m in range(1, n + 1):
                            move_action = ("MOVE", m, square, next_square)
                            available_actions.append(move_action)
        return available_actions

    def is_terminal(self, state):
        if state.score['black'] == 1 & state.score['white'] == 1:
            return True
        elif state.my_colour == "white":
            if state.score['black'] == 0:
                return True
        elif state.my_colour == "black":
            if state.score['white'] == 0:
                return True
        else:
            return False

    def _NEXT_SQUARES(self, square, d=1):
        x, y = square
        return {(x, y + d),
                (x - d, y), (x + d, y),
                (x, y - d)} & self._ALL_SQUARES

    def _NEAR_SQUARES(self, square):
        x, y = square
        return {(x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                (x - 1, y), (x + 1, y),
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)} & self._ALL_SQUARES

    def util_function(self, board, my_color):
        if my_color == "white":
            if board.score['black'] == 0:
                return 1200
            elif board.score['white'] == 0:
                return -1200
            else:
                return board.score['white'] + -0.9 * (12-board.score['black'])

        elif my_color == "black":
            if board.score['white'] == 0:
                return 1200
            elif board.score['black'] == 0:
                return -1200
            else:
                return board.score['black'] + -0.9 * (12-board.score['white'])
