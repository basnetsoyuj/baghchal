'''
FEN -> Similar to Forsyth–Edwards Notation in chess
        {"B3B/5/5/5/B3B"(similar to chess,"B" - Bagh, "G" - Goat)}
        {"G" or "B" represents who has next move}
        {number of moves by goat}
PGN -> Portable Game Notation like in chess
        Move to move tracking notation
        <Move number>. G<old_position><new_position> (...B<old_position><new_position>)
        Example : 1.G0033 B1122 2.G0044
        [ Note:00 for unplaced piece ]
'''
import pickle
import re

with open("data/points_link.pickle", 'rb') as f:
    connected_points_dict = pickle.load(f)

with open("data/bagh_moves.pickle", 'rb') as f:
    bagh_moves_dict = pickle.load(f)


def fen_to_board(fen, board):
    b = [[], [], [], [], []]
    rows = fen.split(" ")[0].split("/")
    for x in range(5):
        counter = 1
        for y in rows[x]:
            if y == "B":
                b[x].append(Bagh(board, (x + 1, counter)))
                counter += 1
            elif y == "G":
                b[x].append(Bagh(board, (x + 1, counter)))
                counter += 1
            else:
                for _ in range(int(y)):
                    b[x].append(0)
                    counter += 1
    return b


def board_to_fen(board):  # Next move and move number not included
    string = ""
    for x in range(5):
        counter = 0
        for y in range(5):
            if board[x][y]:
                counter = 0
                string += board[x][y].__str__()
            else:
                counter += 1
                if y == 4 or board[x][y + 1] != 0:
                    string += str(counter)
        string += "/"
    return string[:-1]


def pgn_converter(pgn, board):
    '''
    return_items takes 0,1 or 2 as value for fen,board,both fen and board respectively
    '''

    moves = re.findall(r'[1-9]+\.\s*([G][1-5]{2,4})\s*([B][x]?[1-5]{4})?', pgn)
    no_of_goat_moves = len(moves)
    next_turn = "B" if moves[-1][-1] == "" else "G"
    Bagh(board, (1, 1))
    Bagh(board, (5, 5))
    Bagh(board, (1, 5))
    Bagh(board, (5, 1))
    no_of_goat_moves_current = 0
    for move in moves:
        no_of_goat_moves_current += 1
        for piece in move:
            if piece == "":
                break
            elif piece[1] == "x":
                x1, y1, x2, y2 = int(piece[2]), int(piece[3]), \
                                 int(piece[4]), int(piece[5])
                if board[x1, y1].__class__ != Bagh: raise Exception(f"Invalid PGN. Piece at ({x1},{y1}) is not Bagh.")
                if not ((x2, y2) in board[x1, y1].valid_bagh_moves()): Exception(
                    f"Invalid PGN. Illegal Capture move by Bagh at {x1}{y1}")
                board.update
            else:
                x1, y1, x2, y2 = int(
                    piece[1]), int(piece[2]), int(piece[3]), \
                                 int(piece[4])

    return f"{board_to_fen(board)} {next_turn} {no_of_goat_moves}"


class Board:

    def __init__(self, description=""):
        self.board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
        self.next_turn = "G"
        self.no_of_moves_made = 0
        self.no_of_goat_moves = 0
        self.no_of_bagh_moves = 0
        self.goats_placed = 0
        self. goats_captured = 0


        if description == "":
            self.fen = "B3B/5/5/5/B3B G 0"
            self.pgn = ""
            self.board = fen_to_board(self.fen, self)

        elif description[0] == "1":
            self.pgn = description
            self.fen = pgn_converter(self.pgn, self)
        else:
            self.fen = fen
            self.pgn = ""
            self.board = fen_to_board(fen, self)

    def __getitem__(self, index):
        return self.board[index[0] - 1][index[1] - 1]

    def __setitem__(self, index, value):
        self.board[index[0] - 1][index[1] - 1] = value
        self.fen = board_to_fen(self.board)

    def no_of_moves_made(self):
        return self.no_of_goat_moves + self.no_of_bagh_moves

    def show_board(self):
        print("-" * 26)
        for row in self.board:
            for x in row:
                if x:
                    print(f"| {x.__str__()} ", end=" ")
                else:
                    print("|   ", end=" ")
            print("|")
            print("-" * 26)

    def validate_placement(self, move):
        x1, y1 = int(move[1]), int(move[2])
        validate_points(x1, y1)
        if not self.goats_placed() < 20: raise Exception(f"More than 20 goats cannot be placed")
        if self[x1, y1]: raise Exception("The coordinate is already occupied.")
        return True

    def validate(self, move):
        move = move.strip()
        if len(move) not in {3, 5, 6}: raise Exception("Error ! Could not recognise the move.")
        if move[0] != self.next_turn: raise Exception(f"Illegal Move : {move}.It is other side's turn.")
        if move[:2] == "Bx": return validate_capture(self, move)
        if len(move) == 3:
            if move[0] == "B": Exception(f"Further Bagh cannot be placed.")
            return validate_placement(self, move)
        if move[:2] == "Gx": raise Exception("Goats cannot capture.")
        x1, y1, x2, y2 = move[2:]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        validate_points(x1, y1, x2, y2)
        validate_pp(x1, y1, move[0])
        if not ((x2, y2) in self.board[x1, y1].valid_bagh_moves()): raise Exception(
            f"Error . {move} is not a valid move.")
        return True

    def validate_capture(self, move):
        x1, y1, x2, y2 = int(move[2]), int(move[3]), int(move[4]), int(move[5])
        validate_points(x1, y1, x2, y2)
        validate_pp(x1, y1, move[0])
        if not ((x2, y2) in self.board[x1, y1].valid_bagh_moves()): raise Exception(
            f"Error . {move} is not a valid move.")
        return True

    def validate_points(self, x1, y1, x2=1, y2=1):
        if not (0 < x1 < 6 and 0 < y1 < 6 and 1 < x2 < 6 and 1 < y2 < 6): raise Exception(
            "Invalid PGN. Coordinates not in range.")

    def validate_pp(self, x1, y1, p):
        if self[x1, y1].__str__() != p: raise Exception(f"Piece at ({x1},{y1}) is other than specified.")

    def move(self, move):
        if len(move) == 3:
            Goat(self, (int(move[1]), int(move[2])))
            self.no_of_goat_moves += 1
            self.goats_placed+=1
        else:
            if len(move) == 5:
                x1, y1, x2, y2 = int(move[1]), int(move[2]), int(move[3]), int(move[4])
            elif len(move) == 6:
                x1, y1, x2, y2 = int(move[2]), int(move[3]), int(move[4]), int(move[5])
                self[(x1+x2)//2,(y1+y2)//2]=0
                self.goats_captured+=1
            self[x1,y1]=0
        if move[0] == "G":
            Goat(board, (x2, y2)
            self.no_of_goat_moves += 1
        elif move[1] == "B":
            Bagh(board, (x2, y2)
            self.no_of_bagh_moves += 1
        self.next_turn="G" if self.next_turn=="B" else "B"


class Piece:

    def __init__(self, board, position=0):
        if position:
            if not (1, 1) <= position <= (5, 5):
                raise Exception(f"Invalid Coordinate for {self.__repr__()} - {position}")
            if board[position[0], position[1]]:
                raise Exception(
                    f"Cannot place {self.__repr__()} at coordinate {position} occupied by {board[position[0],position[1]].__repr__()}")
        self.position = position
        self.board = board
        self.board[position[0], position[1]] = self

    def connected_points(self):
        if self.position:
            return connected_points_dict[self.position]
        else:
            return 0

    def valid_moves(self):
        return {x for x in self.connected_points()
                if not self.board[x[0], x[1]]}

    def update_position(self, new_position):
        self.board[new_position[0], new_position]


class Bagh(Piece):

    def __init__(self, board, position):
        if position == 0:
            raise Exception("Position of Bagh must be defined")
        super(Bagh, self).__init__(board, position)

    def __str__(self):
        return "B"

    def __repr__(self):
        return "Bagh"

    def special_connected_points(self):
        return bagh_moves_dict[self.position]

    def valid_bagh_moves(self):
        return {x for x in self.special_connected_points()
                if (not self.board[x[0], x[1]]) and self.board[
                    (x[0] + self.position[0]) // 2, (x[1] + self.position[1]) // 2].__class__ == Goat}

    def valid_moves(self):
        return super(Bagh, self).valid_moves().union(self.valid_bagh_moves())


class Goat(Piece):

    def __str__(self):
        return "G"

    def __repr__(self):
        return "Goat"


board = Board()
board.show_board()
print(board[1, 1].valid_moves())