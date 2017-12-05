"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    This should be the best heuristic function for your project submission.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # get current move count
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    center = game.width/2

    own_position = game.get_player_location(player)
    opp_position = game.get_player_location(game.get_opponent(player))

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    own_dist_x = abs(center - own_position[0])
    own_dist_y = abs(center - own_position[1])

    opp_dist_x = abs(center - opp_position[0])
    opp_dist_y = abs(center - opp_position[1])

    return float(10 * (own_moves - opp_moves) +
                 (own_dist_x + own_dist_y) - (opp_dist_x + opp_dist_y))



def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    score = .0
    total_spaces = game.width * game.height
    remaining_spaces = len(game.get_blank_spaces())
    coefficient = float(total_spaces - remaining_spaces) / float(total_spaces)

    my_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    for move in my_moves:
        isNearWall = 1 if (move[0] == 0 or move[0] == game.width - 1 or
            move[1] == 0 or move[1] == game.height - 1) else 0
        score += 1 - coefficient * isNearWall

    for move in opponent_moves:
        isNearWall = 1 if (move[0] == 0 or move[0] == game.width - 1 or
            move[1] == 0 or move[1] == game.height - 1) else 0
        score -= 1 - coefficient * isNearWall

    return score

def proximity(location1, location2):
    '''
     Function return extra score as function of proximity between two positions.
    Parameters
    ----------
    location1, location2: tuple
        two tuples of integers (i,j) correspond two different positions on the board

    Returns
    ----------
    float
       extra score as function of proximity between two positions.    
    '''
    return abs(location1[0]-location2[0])+abs(location1[1]-location2[1])


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    score = .0
    total_spaces = game.width * game.height
    remaining_spaces = len(game.get_blank_spaces())
    coefficient = float(total_spaces - remaining_spaces) / float(total_spaces)

    my_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))

    for move in my_moves:
        isNearWall = 1 if (move[0] == 0 or move[0] == game.width - 1 or
            move[1] == 0 or move[1] == game.height - 1) else 0
        score += 1 - coefficient * isNearWall

    for move in opponent_moves:
        isNearWall = 1 if (move[0] == 0 or move[0] == game.width - 1 or
            move[1] == 0 or move[1] == game.height - 1) else 0
        score -= 1 - coefficient * isNearWall

    return score


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.
    ********************  DO NOT MODIFY THIS CLASS  ********************
    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)
    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.
    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score_2, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************
        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def terminate_game(self, game):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        return not bool(game.get_legal_moves())

    def max_value(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth >= self.search_depth:
            return self.score(game, self)
        depth += 1
        if self.terminate_game(game):
            return -1
        value = float("-inf")
        for move in game.get_legal_moves():
            value = max(value, self.min_value(game.forecast_move(move), depth))
        return value

    def min_value(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth >= self.search_depth:
            return self.score(game, self)
        depth += 1
        if self.terminate_game(game):
           return 1
        value = float("inf")
        for move in game.get_legal_moves():
            value = min(value, self.max_value(game.forecast_move(move), depth))
        return value

    def minimax(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        depth = 1
        best_score = float("-inf")
        best_move = game.get_legal_moves()[0]
        for move in game.get_legal_moves():
            value = self.min_value(game.forecast_move(move), depth)
            if value > best_score:
                best_score = value
                best_move = move
        return best_move

class AlphaBetaPlayer(IsolationPlayer):
    def get_move(self, game, time_left):
        self.time_left = time_left
        # TODO: finish this function!
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        while True:
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                best_move = self.alphabeta(game, self.search_depth)
                self.search_depth += 1
                depth = 1
            except SearchTimeout:
                # pass  # Handle any actions required after timeout as needed
                break
        # Return the best move from the last completed search iteration
        return best_move

    def min_value(self, game, depth, alpha, beta):
        # find min result
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()
        depth -= 1
        if ((not moves) or (depth == 0)):
            return self.score(game, self)
        # find minimum value = set to largest value
        for move in moves:
            value = self.max_value(game.forecast_move(move), depth, alpha, beta)
            if value <= alpha:
                return value
            if value < beta:
                beta = value
        return beta

    def max_value(self, game, depth, alpha, beta):
        # find max result
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()
        depth -= 1
        if ((not moves) or (depth == 0)):
            return self.score(game, self)
       # largest value = set to smallest value
        for move in moves:
            value = self.min_value(game.forecast_move(move), depth, alpha, beta)
            if value >= beta:
                return value
            if value > alpha:
                alpha = value
        return alpha
        
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # TODO: finish this function!
        # bestScore = float("-inf")
        bestMove = None
        if depth <= 0:
            return bestMove
        
        # for each legal move - move by AI
        for move in game.get_legal_moves():
            # get min score - move by opponent
            value = self.min_value(game.forecast_move(move), depth, alpha, beta)
            if value > alpha:
                alpha = value
                bestMove = move
        return bestMove
        
