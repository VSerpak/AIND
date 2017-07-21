
# coding: utf-8

# In[1]:

"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


# In[2]:

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


# In[3]:

def winner_loser_determin(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")


# In[4]:

def null_score(game, player):
    """This heuristic presumes no knowledge for non-terminal states, and
    returns the same uninformative value for all other states.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state.
    """
    winner_loser_determin(game, player)

    return 0.


# In[5]:

def open_move_score(game, player):
    """The basic evaluation function described in lecture that outputs a score
    equal to the number of moves open for your computer player on the board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    winner_loser_determin(game, player)

    return float(len(game.get_legal_moves(player)))


# In[6]:

def improved_score(game, player):
    """The "Improved" evaluation function discussed in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    winner_loser_determin(game, player)

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)


# In[7]:

def aggressive_heuristic(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    The "aggressive" evaluation function discussed in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players with minimized opponent moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    winner_loser_determin(game, player)

    my_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return my_moves - 1.5 * opponent_moves


# In[8]:

def moves_determin(game, player):
    """Determine the legal moves for the both players with respect 
    to current position of the player.
    
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
        tuple([(int, int),...],[(int, int),...])
            Board coordinates corresponding to 
            a legal moves for both players moves
    """
    my_moves, opp_moves = [], []
    
    if game.active_player == player:
        my_moves = game.get_legal_moves(player)
    else:
        opp_moves = game.get_legal_moves(game.get_opponent(player))
    
    moves = (my_moves, opp_moves)
    
    return moves


# In[9]:

def weighted_score(game, player, moves):
    """Calculate the weght of each cell (player's position), basing
    on the number of legal next moves for this position.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).
        
    moves : tuple of board coordinates corresponding to 
            a legal moves for both players moves

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    h, w = game.height, game.width
    score = 1.
    
    for move in moves:
        if move in [(0, 0), (0, w-1), (h-1, 0), (h-1, w-1)]:
            score *= 2
        elif move in [(0, 1), (0, w-2), (1, 0), (1, w-1), (h-2, 0), (h-2, w-1), (h-1, 1), (h-1, w-2)]:
            score *= 3
        elif ((move[0] == 0 or move[0] == h-1) and move[1] >= 2 and 
              move[1] <= w-3) or ((move[1] == 0 or move[1] == w-1) and 
                                  move[0] >= 2 and move[0] <= h-3):
            score *= 4
        elif move in [(1, 1), (1, w-2), (h-2, 1), (h-2, w-2)]:
            score *= 4
        elif ((move[0] == 1 or move[0] == h-2) and 
              move[1] >= 2 and move[1] <= w-3) or ((move[1] == 1 or move[1] == w-2) and 
                                                   move[0] >= 2 and move[0] <= h-3):
            score *= 6
        else:
            score *= 8
    return score


# In[10]:

def weighted_open_move_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    The "weighted" open move evaluation function that outputs a weighted
    score equal to the number of moves open for your computer player on the board
    multiplyed on the heuristic constant chosen empirically as 1.5.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """    
    winner_loser_determin(game, player)
    moves = moves_determin(game, player)[0]
    
    return weighted_score(game, player, moves)


# In[11]:

def weighted_improved_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    The "weighted" "Improved" open move evaluation function that outputs a weighted
    score equal to difference in the number of weighted moves available to the
    two players.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """    
    winner_loser_determin(game, player)
    moves = moves_determin(game, player)
    
    my_score = weighted_score(game, player, moves[0])
    opp_score = weighted_score(game, player, moves[1])    
    
    return float(my_score - opp_score)


# In[12]:

def diff_my_moves_opp_moves_one_ply_lookahead(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    The difference in the number of available moves between the current
    player and its opponent one ply ahead in the future is used as the
    score of the current game state.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : objects
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """
    winner_loser_determin(game, player)

    h, w = game.height, game.width
    my_score, opp_score = 0, 0
    
    my_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    
    for move in my_moves:
        my_score += len(game.get_legal_moves(player))

    for move in opp_moves:
        opp_score += len(game.get_legal_moves(game.get_opponent(player)))

    return float(my_score - opp_score)


# In[13]:

def aggressive_diff_moves_one_ply_lookahead(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    The difference in the number of available moves between the current
    player and its opponent one ply ahead in the future is used as the
    score of the current game state. Player’s scores should be maximized
    by heuristic costant empirically chosen as 1.5.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : objects
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """
    winner_loser_determin(game, player)

    h, w = game.height, game.width
    my_score, opp_score = 0, 0
    
    my_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    
    for move in my_moves:
        my_score += len(game.get_legal_moves(player))

    for move in opp_moves:
        opp_score += len(game.get_legal_moves(game.get_opponent(player)))

    return float(1.5*my_score - opp_score)


# In[14]:

def aggr_weighted_improved_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    The "weighted" "Improved" open move evaluation function that outputs a weighted
    score equal to difference in the number of weighted moves available to the
    two players. Player’s scores should be maximized by heuristic costant empirically 
    chosen as 1.5.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """    
    winner_loser_determin(game, player)
    moves = moves_determin(game, player)
    
    my_score = weighted_score(game, player, moves[0])
    opp_score = weighted_score(game, player, moves[1])    
    
    return float(1.5*my_score - opp_score)


# In[15]:

def aggress_diff_weight_moves_one_ply_lookahead(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    The difference in the number of available moves between the current
    player and its opponent one ply ahead in the future is used as the
    score of the current game state. Player’s scores should be maximized
    by heuristic costant empirically chosen as 1.5.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : objects
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """
    winner_loser_determin(game, player)

    h, w = game.height, game.width
    my_score, opp_score = 0, 0
    
    my_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    
    for move in my_moves:
        my_score += weighted_score(game, player, my_moves)

    for move in opp_moves:
        opp_score += weighted_score(game, player, opp_moves)

    return float(1.5*my_score - opp_score)


# In[16]:

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

    return aggress_diff_weight_moves_one_ply_lookahead(game, player)


# In[17]:

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

    return aggressive_diff_moves_one_ply_lookahead(game, player)


# In[18]:

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

    return aggressive_heuristic(game, player)


# In[19]:

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
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


# In[20]:

import math

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

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        # raise NotImplementedError
        return self.best_move(game,depth)[0]
            
    def active_player(self, game):
        return game.active_player == self
    
    def evaluation(self,game):
        active_player = self.active_player(game)
        if active_player:
            value = float('-inf')
            function = max
        else:
            value = float('inf')
            function = min
        return value, function

    def best_move(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if depth == 0:
            return (game.get_player_location(self), self.score(game, self))

        best_move = (-1, -1) 
        legal_moves = game.get_legal_moves()
        next_move, function, value = None, None, None
        
        value = self.evaluation(game)[0]
        function = self.evaluation(game)[1]
        
        for move in legal_moves:
            next_move = game.forecast_move(move)
            score = self.best_move(next_move, depth - 1)[1]
            if function(value, score) == score:
                best_move = move
                value = score

        return best_move, value


# In[21]:

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.
        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************
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
        move = (-1, -1)
        for i in range(1, 100):
            try:
                move = self.alphabeta(game, i)
            except SearchTimeout:
                break
        return move

    def active_player(self, game):
        return game.active_player == self
    
    def evaluation(self,game):
        active_player = self.active_player(game)
        if active_player:
            value = float('-inf')
            function = max
            is_max = True
        else:
            value = float('inf')
            function = min
            is_max = False
        return value, function, is_max

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.
        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md
        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.
            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
               
        return self.best_move_a_b(game, depth)[0]        

    def best_move_a_b(self, game, depth, 
                      alpha=float("-inf"), beta=float("inf")):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if depth == 0:
            return (game.get_player_location(self), self.score(game, self))

        best_move = (-1, -1) 
        legal_moves = game.get_legal_moves()
        next_move, function, value = None, None, None
        
        is_max = True

        value = self.evaluation(game)[0]
        function = self.evaluation(game)[1]
        is_max = self.evaluation(game)[2]

        for move in legal_moves:
            next_move = game.forecast_move(move)
            score = self.best_move_a_b(next_move, depth - 1, alpha, beta)[1]
            if function(value, score) == score:
                best_move = move
                value = score
            if is_max:
                if value >= beta:
                    return best_move, value
                else:
                    alpha = max(value, alpha)
            else:
                if value <= alpha:
                    return best_move, value
                else:
                    beta = min(value, beta)

        return best_move, value


# In[ ]:



