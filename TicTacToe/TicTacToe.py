
# coding: utf-8

# In[1]:

from collections import namedtuple
GameState = namedtuple("GameState",('to_move, utility, board, moves'))


# In[2]:

class TicTacToe():
    def __init__(self, h=3, k=3, v=3):
        self.h = h
        self.k = k
        self.v = v
        
        moves = [(x,y) for x in range(1, h+1)
                for y in range(1, v+1)]
        
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)
        
    def display(self, state):
        board = state.board
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print(board.get((x,y),'.'), end=' ')
            print()


# In[3]:

ttt = TicTacToe()


# In[4]:

ini_state = ttt.initial
ini_state


# In[5]:

ttt.display(ini_state)


# In[6]:

ini_state.to_move


# In[7]:

def random_player(game, state):
    return random.choice(game.actions(state))


# In[8]:

import random
random_player(ttt, ini_state)


# In[9]:

class TicTacToe():
    def __init__(self, h=3, k=3, v=3):
        self.h = h
        self.k = k
        self.v = v
        
        moves = [(x,y) for x in range(1, h+1)
                for y in range(1, v+1)]
        
        self.board = {k:"." for k in moves}
        
        self.initial = GameState(to_move='X', utility=0, board=self.board, moves=moves)
        print(self.initial)
        
    def display(self, state):
        board = state.board
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print(board.get((x,y),'.'), end=' ')
            print()
            
    def actions(self, state):
        return state.moves
    
    def result(self, state, moves, move):
        if move not in state.moves:
            return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                            board=state.board, moves=state.moves,
                            utility=self.compute_utility(state.board, move, state.to_move))
        board = state.board.copy()
        self.board[move] = state.to_move
        moves.remove(move)
        
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                            board=state.board, moves=state.moves,
                            utility=self.compute_utility(state.board, move, state.to_move))
    
    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 1)) or
                self.k_in_row(board, move, player, (1, -1))):
            
            return +1 if player == 'X' else -1
        else:
            return 0
        
    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k
    
    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0



# In[10]:

ttt = TicTacToe()


# In[11]:

ini_state = ttt.initial


# In[12]:

ttt.display(ini_state)


# In[13]:

random_player(ttt, ini_state)


# In[14]:

random_player(ttt, ini_state)


# In[15]:

move = random_player(ttt, ini_state)
move


# In[16]:

ini_state.moves


# In[17]:

ini_state = ttt.result(ini_state, ini_state.moves, move)


# In[18]:

ini_state


# In[19]:

ttt.board


# In[20]:

ttt.display(ini_state)


# In[21]:

class TicTacToe():
    def __init__(self, h=3, k=3, v=3):
        self.h = h
        self.k = k
        self.v = v
        
        moves = [(x,y) for x in range(1, h+1)
                for y in range(1, v+1)]
        
        self.board = {k:"." for k in moves}
        
        self.initial = GameState(to_move='X', utility=0, board=self.board, moves=moves)
        print(self.initial)
        
    def display(self, state):
        board = state.board
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print(board.get((x,y),'.'), end=' ')
            print()
            
    def actions(self, state):
        return state.moves
    
    def disp_result(self, state, move):
        if move not in state.moves:
            return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                            board=state.board, moves=state.moves,
                            utility=self.compute_utility(state.board, move, state.to_move))
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                            board=state.board, moves=state.moves,
                            utility=self.compute_utility(board, move, state.to_move))
    
    def result(self, state, moves, move):
        if move not in state.moves:
            return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                            board=state.board, moves=state.moves,
                            utility=self.compute_utility(state.board, move, state.to_move))
        board = state.board.copy()
        self.board[move] = state.to_move
        moves.remove(move)
        
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                            board=state.board, moves=state.moves,
                            utility=self.compute_utility(state.board, move, state.to_move))
    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 1)) or
                self.k_in_row(board, move, player, (1, -1))):
            
            return +1 if player == 'X' else -1
        else:
            return 0
        
    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k
    
    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move


# In[22]:

ttt = TicTacToe()
ini_state = ttt.initial


# In[23]:

ttt.display(ini_state)


# In[24]:

move = random_player(ttt, ini_state)
move


# In[25]:

ini_state = ttt.result(ini_state, ini_state.moves, move)


# In[26]:

ttt.display(ini_state)


# <img src='Images/pceudo_code_minimax_alg.png' width=70%>

# In[27]:

infinity = float('inf')
def alphabeta_player(game, state):
    return alphabeta_full_search(state, game)


# In[28]:

move = alphabeta_player(ttt, ini_state)
move


# In[29]:

def alphabeta_full_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.disp_result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.disp_result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.disp_result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


# In[30]:

move = alphabeta_player(ttt, ini_state)
move


# In[31]:

state = ttt.result(ini_state, ini_state.moves, move)
ttt.display(state)


# In[32]:

state


# In[33]:

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


# In[34]:

class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                             utility=self.compute_utility(state.board, move, state.to_move),
                             board=state.board, moves=state.moves)  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k


# In[35]:

ttt = TicTacToe()
state = ttt.initial
ttt.display(state)


# <img src='Images/fig.5.5.png' width=70%>
# <img src='Images/pceudo_code_a_b_search_alg.png' width=70%>

# In[36]:

def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


# In[37]:

def alphabeta_player(game, state):
    return alphabeta_search(state, game)


# In[38]:

ttt.play_game(random_player, alphabeta_player)


# In[39]:

class ConnectFour(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)

    def actions(self, state):
        return [(x, y) for (x, y) in state.moves
                if y == 1 or (x, y - 1) in state.board]


# In[42]:

ttt_four = ConnectFour()


# In[43]:

state = ttt_four.initial
ttt_four.display(state)


# In[45]:

ttt_four.play_game(random_player, alphabeta_player)


# In[46]:

ttt_four.play_game(alphabeta_player, alphabeta_player)


# In[48]:

ttt_four.play_game(random_player, alphabeta_player)


# In[ ]:



