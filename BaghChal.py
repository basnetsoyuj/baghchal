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


def fen_to_board(fen, board):
    board = [[], [], [], [], []]
    rows = self.fen.split(" ")[0].split("/")
    for x in range(5):
        for y in range(5):
            if rows[x][y] == "B":
                board[x][y] = Bagh(board, (x+1, y+1))
            elif rows[x][y] == "G":
                board[x][y] = Goat(board, (x+1, y+1))
            else:
                board[x][y]


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


def pgn_converter(pgn, board, return_items=0):
    '''
    return_items takes 0,1 or 2 as value for fen,board,both fen and board respectively
    '''

    moves = re.findall(r"[1-9]+\.\s*([G][0-9]{4})\s*([B][0-9]{4})?", pgn)
    no_of_goat_moves = len(moves)
    next_turn = "B" if moves[-1][-1] == "" else "G"
    board = [[Bagh(board, (1, 1)), 0, 0, 0, Bagh(board, (1, 5))],
             [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
             [Bagh(board, (5, 1)), 0, 0, 0, Bagh(board, (5, 5))]]
    no_of_goat_moves_current = 0
    for move in moves:
        no_of_goat_moves_current += 1
        for piece in move:
            if piece == "":
                continue
            x1, y1, x2, y2 = int(
                piece[1]) - 1, int(piece[2]) - 1, int(piece[3]) - 1,\
                int(piece[4]) - 1
            if piece[0] == "B" or no_of_goat_moves_current > 20:
                if board[x1][y1] == 0 or board[x2][y2] != 0:
                    raise Exception("Invalid PGN - Move not possible")
                else:
                    board[x1][y1] = 0
            else:
                if board[x2][y2] != 0:
                    raise Exception("Invalid PGN - Move not possible")
                board[x2][y2] =piece[0]
    if return_items == 0:
        return f"{board_to_fen(board)} {next_turn} {no_of_goat_moves}"
    elif return_items == 1:
        return board
    else:
        return f"{board_to_fen(board)} {next_turn} {no_of_goat_moves}", board


class Board:

    def __init__(self, description=""):
        if description == "":
            self.fen = "B3B/5/5/5/B3B G 0"
            self.pgn = ""
        elif description[0] == "1":
            self.pgn = description
            self.fen, self.board = pgn_converter(self.pgn, self, 2)
        else:
            self.fen = fen
            self.pgn = ""

    def __getitem__(self, index):
        return self.board[index[0]][index[1]]

    def __setitem__(self, index, value):
        self.board[index[0]][index[1]] = value

    def next_turn(self):
        return self.fen.split(" ")[1]

    def no_of_goat_moves(self):
        return int(self.fen.split(" ")[2])

    def no_of_bagh_moves(self):
        return self.no_of_goat_moves() \
            if self.next_turn() == "G" else self.no_of_goat_moves() - 1

    def no_of_moves_made(self):
        return self.no_of_goat_moves() + self.no_of_bagh_moves()

    def goats_placed(self):
        return self.no_of_goat_moves() if self.no_of_goat_moves() < 20 else 20

    def goats_captured(self):
        return self.goats_placed() - self.fen.split(" ")[0].count("G")

    def show_board(self):
        rows = self.fen.split(" ")[0].split("/")
        print("-" * 26)
        for row in rows:
            for x in row:
                if x == "B":
                    print("| B ", end=" ")
                elif x == "G":
                    print("| G ", end=" ")
                else:
                    for _ in range(int(x)):
                        print("|   ", end=" ")
            print("|")
            print("-" * 26)


class Piece:

    def __init__(self, board, position=0):
        self.position = position
        self.board = board

    def connected_points(self):
        if self.position:
            return connected_points_dict[self.position]
        else:
            return 0

    def valid_moves(self):
        return {x for x in self.connected_points()
                if not self.board[x[0], x[1]]}

    def update_position(new_position):
        self.position = new_position


class Bagh(Piece):

    def __str__(self):
        return "B"

    def __repr__(self):
        return "B"

    def special_connected_points(self):
        pass


class Goat(Piece):

    def __str__(self):
        return "G"

    def __repr__(self):
        return "B"


board = Board("1.G0033 B1122 2.G0044")
g = Goat(board, (1, 2))
print(board.board)
