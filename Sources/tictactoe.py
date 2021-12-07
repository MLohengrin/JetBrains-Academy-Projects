# Tic-Tac-Toe with AI

import random


class TicTacToe:
    STATES = ('X', 'O', 'DRAW', 'UNFINISHED')
    PLAYERS = ('user', 'easy', 'medium', 'hard')

    def __init__(self) -> None:
        self.active = True
        self.state = self.STATES[3]
        self.matrix = list()
        self.new_game()
        self.player1 = None
        self.player2 = None
        self.main()

    def __str__(self) -> str:
        repr = '---------\n'
        for r in range(3):
            repr += '| ' + ' '.join(self.matrix[r]) + ' |\n'
        repr += '---------'
        return repr

    def new_game(self):
        self.matrix.clear()
        self.active = True
        self.state = self.STATES[3]
        self.player1 = None
        self.player2 = None
        for _ in range(3):
            self.matrix.append([' ', ' ', ' '])

    def generate_matrix(self, param):
        for row in range(3):
            for col in range(3):
                self.matrix[row][col] = param[row * 3 + col] if param[row * 3 + col] != '_' else ' '

    def check_move(self, move_str):
        move = move_str.split()
        if len(move) != 2 or (not (move[0].isnumeric() or move[1].isnumeric())):
            print('You should enter numbers!')
        else:
            x, y = int(move[1]) - 1, int(move[0]) - 1
            if x < 0 or x > 2 or y < 0 or y > 2:
                print('Coordinates should be from 1 to 3!')
            else:
                if not self.isfree(x, y, self.matrix):
                    print('This cell is occupied! Choose another one!')
                else:
                    self.matrix[y][x] = self.next_symb(self.matrix)
                    return True

    def isfree(self, x, y, board):
        return board[y][x] == ' '

    def next_symb(self, board):
        xtot, otot = 0, 0
        for rows in board:
            for symb in rows:
                if symb == 'X':
                    xtot += 1
                elif symb == 'O':
                    otot += 1
        return 'X' if xtot <= otot else 'O'

    def user_move(self):
        while True:
            move = input('Enter the coordinates: ')
            if self.check_move(move):
                break

    def check_state(self):
        if self.check_win('X', self.matrix):
            self.state = self.STATES[0]
            self.active = False
        elif self.check_win('O', self.matrix):
            self.state = self.STATES[1]
            self.active = False
        elif self.full(self.matrix):
            self.state = self.STATES[2]
            self.active = False
        else:
            self.state = self.STATES[3]

    def full(self, board):
        for row in board:
            for sym in row:
                if sym == ' ':
                    return False
        return True

    def check_win(self, sym, board):
        first_col = sym == board[0][0] == board[1][0] == board[2][0]
        second_col = sym == board[0][1] == board[1][1] == board[2][1]
        third_col = sym == board[0][2] == board[1][2] == board[2][2]
        first_row = sym == board[0][0] == board[0][1] == board[0][2]
        second_row = sym == board[1][0] == board[1][1] == board[1][2]
        third_row = sym == board[2][0] == board[2][1] == board[2][2]
        main_diag = sym == board[0][0] == board[1][1] == board[2][2]
        side_diag = sym == board[0][2] == board[1][1] == board[2][0]
        if any([first_col, second_col, third_col, first_row, second_row, third_row, main_diag, side_diag]):
            return True
        return False

    def print_state(self):
        if self.state == self.STATES[0]:
            print('X wins')
        if self.state == self.STATES[1]:
            print('O wins')
        if self.state == self.STATES[2]:
            print('Draw')
        if self.state == self.STATES[3]:
            print('Game not finished')

    def computer_move(self, player):
        print(f'Making move level "{player}"')
        if player == 'easy':
            self.easy_move()
        elif player == 'medium':
            self.medium_move(player)
        elif player == 'hard':
            self.hard_move(player)

    def easy_move(self):
        while True:
            x, y = random.randint(0, 2), random.randint(0, 2)
            if self.isfree(x, y, self.matrix):
                self.matrix[y][x] = self.next_symb(self.matrix)
                break

    def medium_move(self, player):
        winning_move = self.winning_move(player)
        saving_move = self.saving_move(player)
        if winning_move:
            self.matrix[winning_move[0]][winning_move[1]] = self.next_symb(self.matrix)
        elif saving_move:
            self.matrix[saving_move[0]][saving_move[1]] = self.next_symb(self.matrix)
        else:
            self.easy_move()

    def winning_move(self, player):
        last_one = self.last_one(self.next_symb(self.matrix))
        return last_one

    def saving_move(self, player):
        last_one = self.last_one('X' if 'X' != self.next_symb(self.matrix) else 'O')
        return last_one

    def last_one(self, sym):
        # 00
        if self.matrix[0][0] == ' ':
            if sym == self.matrix[0][1] == self.matrix[0][2] or \
                    sym == self.matrix[1][1] == self.matrix[2][2] or \
                    sym == self.matrix[1][0] == self.matrix[2][0]:
                return 0, 0
        # 01
        if self.matrix[0][1] == ' ':
            if sym == self.matrix[0][0] == self.matrix[0][2] or \
                    sym == self.matrix[1][1] == self.matrix[2][1]:
                return 0, 1
        # 02
        if self.matrix[0][2] == ' ':
            if sym == self.matrix[0][0] == self.matrix[0][1] or \
                    sym == self.matrix[1][1] == self.matrix[0][2] or \
                    sym == self.matrix[1][2] == self.matrix[2][2]:
                return 0, 2
                # 10
        if self.matrix[1][0] == ' ':
            if sym == self.matrix[0][0] == self.matrix[2][0] or \
                    sym == self.matrix[1][1] == self.matrix[1][2]:
                return 1, 0
        # 11
        if self.matrix[1][1] == ' ':
            if sym == self.matrix[0][0] == self.matrix[2][2] or \
                    sym == self.matrix[0][2] == self.matrix[2][0] or \
                    sym == self.matrix[0][1] == self.matrix[2][1] or \
                    sym == self.matrix[1][0] == self.matrix[1][2]:
                return 1, 1
        # 12
        if self.matrix[1][2] == ' ':
            if sym == self.matrix[0][2] == self.matrix[2][2] or \
                    sym == self.matrix[1][0] == self.matrix[1][1]:
                return 1, 2
        # 20
        if self.matrix[2][0] == ' ':
            if sym == self.matrix[0][0] == self.matrix[1][0] or \
                    sym == self.matrix[1][1] == self.matrix[0][2] or \
                    sym == self.matrix[2][1] == self.matrix[2][2]:
                return 2, 0
        # 21
        if self.matrix[2][1] == ' ':
            if sym == self.matrix[0][1] == self.matrix[1][1] or \
                    sym == self.matrix[2][0] == self.matrix[2][2]:
                return 2, 1
        # 22
        if self.matrix[2][2] == ' ':
            if sym == self.matrix[0][2] == self.matrix[1][2] or \
                    sym == self.matrix[0][0] == self.matrix[1][1] or \
                    sym == self.matrix[2][0] == self.matrix[2][1]:
                return 2, 2
        return False

    def hard_move(self, player):
        result = self.minimax([x for x in self.matrix], self.next_symb(self.matrix), self.next_symb(self.matrix))
        y, x = result['index'] // 3, result['index'] % 3
        self.matrix[y][x] = self.next_symb(self.matrix)

    def minimax(self, matrix, ai_player, actual_player):
        availabe_spots = self.find_free(matrix)
        if self.check_win(ai_player, matrix):
            return {'score': 10}
        elif self.check_win('X' if ai_player == 'O' else 'O', matrix):
            return {'score': -10}
        elif self.full(matrix):
            return {'score': 0}
        moves = []
        for i in range(len(availabe_spots)):
            move = dict()
            move['index'] = availabe_spots[i]
            matrix[availabe_spots[i] // 3][availabe_spots[i] % 3] = actual_player
            result = self.minimax([x for x in matrix], ai_player, 'X' if actual_player == 'O' else 'O')
            move['score'] = result['score']
            matrix[availabe_spots[i] // 3][availabe_spots[i] % 3] = ' '
            moves.append(move)
        bestMove = 0
        if actual_player == ai_player:
            bestScore = -10000
            for i in range(len(moves)):
                if moves[i]['score'] > bestScore:
                    bestScore = moves[i]['score']
                    bestMove = i
        else:
            bestScore = 10000
            for i in range(len(moves)):
                if moves[i]['score'] < bestScore:
                    bestScore = moves[i]['score']
                    bestMove = i
        return moves[bestMove]

    def find_free(self, matrix):
        spots = []
        for n in range(9):
            if self.isfree(n % 3, n // 3, matrix):
                spots.append(n)
        return spots

    def input_settings(self):
        while True:
            choice = input("Input command: ").split()
            if choice[0] == 'exit':
                exit()
            if len(choice) != 3 or \
                    choice[0] != 'start' or \
                    choice[1] not in self.PLAYERS or \
                    choice[2] not in self.PLAYERS:
                print('Bad parameters')
                continue
            else:
                self.player1 = choice[1]
                self.player2 = choice[2]
                break

    def main(self):
        # self.generate_matrix(input())
        while True:
            self.new_game()
            self.input_settings()
            print(self)
            while self.active:
                self.user_move() if self.player1 == 'user' else self.computer_move(self.player1)
                print(self)
                self.check_state()
                # self.print_state()
                if self.active:
                    self.user_move() if self.player2 == 'user' else self.computer_move(self.player2)
                    print(self)
                    self.check_state()
                    if not self.active:
                        self.print_state()
                else:
                    self.print_state()


TicTacToe()
