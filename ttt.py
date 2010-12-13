'''
Tic-Tac-Toe

rkchak

'''

import operator, sys, random, time


E = EMPTY = ' '
X = 'x'
O = 'o'

class TictactoeBoard(object):
    board = [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    center = 1,1
    winning_positions_list = [ [(0,0),(0,1),(0,2)],
                               [(1,0),(1,1),(1,2)],
                               [(2,0),(2,1),(2,2)],
                               [(0,0),(1,0),(2,0)],
                               [(0,1),(1,1),(2,1)],
                               [(0,2),(1,2),(2,2)],
                               [(0,0),(1,1),(2,2)],
                               [(0,2),(1,1),(2,0)] ]
    opponent = { X: O, O: X}
    def __init__(self, computer, human):
        self.computer = computer
        self.human = human
        
    def value(self, pos):
        row, col = pos
        return self.board[row][col]
    
    def get_winner(self):
        for winning_positions in self.winning_positions_list:
            if self.value(winning_positions[0]) == self.value(winning_positions[1]) == self.value(winning_positions[2]):
                return self.value(winning_positions[0])
        return None

    def get_human_input(self):
        input = raw_input("position - ")
        row = int(input[0])-1
        col = int(input[1])-1
        move = row, col
        if move not in self.possible_moves():
            print 'Invalid position'
            return None
        return row, col
    
    def play_human(self):
        got_valid_input = True
        while got_valid_input:
            retval = self.get_human_input()
            if retval:
                got_valid_input = False
                move = retval
        self.play(move, self.human)
        self.display()
        self.is_game_over()
        return True
        
    def play(self, move, ch):
        row, col = move
        if self.board[row][col] == E:
            self.board[row][col] = ch
            return True
        return False
        
    def undo_play(self, move):
        row, col = move
        self.board[row][col] = E
        
    def play_computer(self):
        moves = [(move, self.deduce_next_move(move, self.computer)) for move in self.possible_moves()]
        random.shuffle(moves)
        moves.sort(key = lambda (move, get_winner): get_winner)
        move = moves[-1][0]
        print 'Computer move:', (int(move[0])+1, int(move[1])+1)
        self.play(move, self.computer)
        self.display()
        self.is_game_over()
    def deduce_next_move(self, move, player):
        try:
            self.play(move, player)
            if not self.possible_moves():
                winner = self.get_winner()
                if winner == player:
                    return +1
                if not winner:
                    return 0
                return -1
            outcomes = [self.deduce_next_move(next_move, self.opponent[player]) for next_move in self.possible_moves()]
            if player == self.computer:
                return min(outcomes)
            else:
                return max(outcomes)
        finally:
            self.undo_play(move)
    
    def possible_moves(self):
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == EMPTY:
                    moves.append((row, col))
        return moves
    
    def is_game_over(self):
        return not self.possible_moves() or self.get_winner()


    def display(self):
        self.display_positions_board()
        print 'Playing board:'
        print '', self.board[0][0], '|', self.board[0][1], '|', self.board[0][2]
        print "---+---+---"
        print '', self.board[1][0], '|', self.board[1][1], '|', self.board[1][2]
        print "---+---+---"
        print '', self.board[2][0], '|', self.board[2][1], '|', self.board[2][2]
        print

    def display_positions_board(self):
        positions_board = [[11, 12, 13],
                           [21, 22, 23],
                           [31, 32, 33]]
        print 'Positions board:'
        print positions_board[0][0], '|', positions_board[0][1], '|', positions_board[0][2]
        print "---+----+---"
        print positions_board[1][0], '|', positions_board[1][1], '|', positions_board[1][2]
        print "---+----+---"
        print positions_board[2][0], '|', positions_board[2][1], '|', positions_board[2][2]
        print
        

def status(tictactoe):
    winner = tictactoe.get_winner()
    if winner == tictactoe.human:
        print "Game over. You won!"
        sys.exit(0)
    elif winner == tictactoe.computer:
        print "Game over. The computer won."
        sys.exit(0)
    else:
        if not len(tictactoe.possible_moves()):
            print "Game over. Draw"
            sys.exit(0)

def main():
    human =  raw_input("You playing with? (x/o): ")
    if human in ['x', 'X']:
        human = X
        computer = O
    elif human in ['o', 'O']:
        human = O
        computer = X
    else:
        print "Invalid input."
        return
    first_turn =  raw_input("Do you wish to start the game? (y/n): ")
    if first_turn in ['n', 'N']:
        first_turn = 'computer'
    elif first_turn in ['y', 'Y']:
        first_turn = 'human'
    else:
        print "Invalid input."
        return
    # create the object
    tictactoe = TictactoeBoard(computer, human)
    if first_turn == 'human':
        tictactoe.display()
    turn_index = 1    
    while True:
        if first_turn == 'computer':
            tictactoe.play_computer()
            status(tictactoe)
            tictactoe.play_human()
            status(tictactoe)
        elif first_turn == 'human':
            tictactoe.play_human()
            status(tictactoe)
            tictactoe.play_computer()
            status(tictactoe)

if __name__ == '__main__':
    main()