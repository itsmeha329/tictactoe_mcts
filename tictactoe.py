import math
import random
from copy import deepcopy

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, move):
        if self.board[move] == ' ':
            self.board[move] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def is_winner(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(self.board[i] == player for i in condition) for condition in win_conditions)

    def is_game_over(self):
        return self.is_winner('X') or self.is_winner('O') or len(self.available_moves()) == 0

    def get_result(self, player):
        if self.is_winner(player):
            return 1
        elif self.is_winner('O' if player == 'X' else 'X'):
            return -1
        else:
            return 0

    def print_board(self):
        for i in range(0, 9, 3):
            print(' | '.join(self.board[i:i+3]))
            if i < 6:
                print('---------')

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.score = 0

class MCTS:
    def __init__(self, state, player):
        self.root = Node(state)
        self.player = player

    def select(self, node):
        while not node.state.is_game_over():
            if len(node.children) < len(node.state.available_moves()):
                return self.expand(node)
            else:
                node = self.get_best_child(node)
        return node

    def expand(self, node):
        tried_moves = [child.move for child in node.children]
        untried_moves = [move for move in node.state.available_moves() if move not in tried_moves]
        move = random.choice(untried_moves)
        new_state = deepcopy(node.state)
        new_state.make_move(move)
        child = Node(new_state, parent=node, move=move)
        node.children.append(child)
        return child

    def simulate(self, state):
        while not state.is_game_over():
            move = random.choice(state.available_moves())
            state.make_move(move)
        return state.get_result(self.player)

    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.score += result
            node = node.parent

    def get_best_child(self, node, c_param=1.4):
        best_score = float('-inf')
        best_children = []
        for child in node.children:
            exploit = child.score / child.visits
            explore = math.sqrt(math.log(node.visits) / child.visits)
            score = exploit + c_param * explore
            if score > best_score:
                best_score = score
                best_children = [child]
            elif score == best_score:
                best_children.append(child)
        return random.choice(best_children)

    def get_best_move(self, simulations_number):
        for _ in range(simulations_number):
            node = self.select(self.root)
            result = self.simulate(deepcopy(node.state))
            self.backpropagate(node, result)
        return self.get_best_child(self.root, c_param=0).move

def play_game():
    game = TicTacToe()
    while not game.is_game_over():
        game.print_board()
        if game.current_player == 'X':
            while True:
                try:
                    move = int(input("Enter your move (0-8): "))
                    if move in game.available_moves():
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number between 0 and 8.")
        else:
            mcts = MCTS(game, 'O')
            move = mcts.get_best_move(1000)
        game.make_move(move)
    
    game.print_board()
    if game.is_winner('X'):
        print("You win!")
    elif game.is_winner('O'):
        print("AI wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_game()
