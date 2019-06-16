'''
FEN -> Similar to Forsyth–Edwards Notation in chess
        {"B3B/5/5/5/B3B"(similar to chess,"B" - Bagh, "G" - Goat)}
        {"G" or "B" represents who has next move}
        {number of moves by goat}
PGN -> Portable Game Notation like in chess
        Move to move tracking notation
        <Move number>. G(<old_position>)<new_position> (...B<old_position><new_position>)
        Example : 1.G33 B1122 2.G44
        [ Note: G<new_position> for unplaced piece ]
'''
import pickle
import re

with open("data/points_link.pickle", 'rb') as f:
    connected_points_dict = pickle.load(f)

with open("data/bagh_moves.pickle", 'rb') as f:
    bagh_moves_dict = pickle.load(f)


class Board:

    def __init__(self, description=""):
        self.board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
        self.next_turn = "G"
        self.no_of_goat_moves = 0
        self.no_of_bagh_moves = 0
        self.goats_placed = 0
        self.goats_captured = 0
        self.goat_points = set()
        self.bagh_points = set()

        if description == "":
            self.fen = "B3B/5/5/5/B3B G 0"
            self.pgn = ""
            self.fen_to_board(self.fen)

        else:
            self.pgn = description.strip()
            self.pgn_converter(self.pgn)

    def __getitem__(self, index):
        return self.board[index[0] - 1][index[1] - 1]

    def __setitem__(self, index, value):
        self.board[index[0] - 1][index[1] - 1] = value

    def no_of_moves_made(self):
        return self.no_of_goat_moves + self.no_of_bagh_moves

    def possible_moves(self):
        if self.is_game_over(): return 0
        move_list = set()
        if self.next_turn == "G" and self.no_of_goat_moves < 20:
            return {f'G{x1}{y1}' for x1 in range(1, 6) for y1 in range(1, 6) if
                    (x1, y1) not in self.bagh_points.union(self.goat_points)}
        elif self.next_turn == "G" and self.no_of_goat_moves >= 20:
            for x1, y1 in self.goat_points:
                move_list.update({f'G{x1}{y1}{x2}{y2}' for x2, y2 in self[x1, y1].valid_moves()})
            return move_list
        else:
            for x1, y1 in self.bagh_points:
                move_list.update({f'B{x1}{y1}{x2}{y2}' for x2, y2 in self[x1, y1].valid_non_special_moves()})
                move_list.update({f'Bx{x1}{y1}{x2}{y2}' for x2, y2 in self[x1, y1].valid_bagh_moves()})
            return move_list

    def pgn_converter(self, pgn):
        move_list = re.findall(
            r'[0-9]+\.\s*([G][1-5]{2,4})\s*([B][x]?[1-5]{4})?', pgn)
        print(move_list)
        # no_of_goat_moves = len(moves)
        # next_turn = "B" if moves[-1][-1] == "" else "G"
        Bagh(self, (1, 1))
        Bagh(self, (5, 5))
        Bagh(self, (1, 5))
        Bagh(self, (5, 1))
        for moves in move_list:
            for move in moves:
                if move == "":
                    break
                self.move(move)

    def fen_to_board(self, fen):
        rows = fen.split(" ")[0].split("/")
        for x in range(5):
            counter = 1
            for y in rows[x]:
                if y == "B":
                    Bagh(self, (x + 1, counter))
                    counter += 1
                elif y == "G":
                    Bagh(self, (x + 1, counter))
                    counter += 1
                else:
                    for _ in range(int(y)):
                        counter += 1

    @property
    def baghs_trapped(self):
        counter = 0
        for bagh in self.bagh_points:
            if not self[bagh[0], bagh[1]].valid_moves():
                counter += 1
        return counter

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
        self.validate_points(x1, y1)
        if not self.goats_placed < 20:
            raise Exception(f"More than 20 goats cannot be placed")
        if self[x1, y1]:
            raise Exception("The coordinate is already occupied.")
        return True

    def validate(self, move):
        if self.is_game_over(): raise Exception("The game is already over.")
        move = move.strip()
        if len(move) not in {3, 5, 6}:
            raise Exception("Error ! Could not recognise the move.")
        if move[0] != self.next_turn:
            raise Exception(f"Illegal Move : {move}.It is other side's turn.")
        if move[:2] == "Bx":
            return self.validate_capture(move)
        if len(move) == 3:
            if self.goats_placed >= 20:
                raise Exception(f"Futher piece cannot be placed.")
            if move[0] == "B":
                raise Exception(f"Further Bagh cannot be placed.")
            return self.validate_placement(move)
        if move[0] == "G" and len(move) == 5 and self.no_of_goat_moves < 20:
            raise Exception("All the goats must be placed first.")
        if move[:2] == "Gx":
            raise Exception("Goats cannot capture.")
        x1, y1, x2, y2 = int(move[1]), int(move[2]), int(move[3]), int(move[4])
        self.validate_points(x1, y1, x2, y2)
        self.validate_pp(x1, y1, move[0])
        if not ((x2, y2) in self[x1, y1].valid_moves()):
            raise Exception(
                f"Error . {move} is not a valid move.")
        return True

    def validate_capture(self, move):
        x1, y1, x2, y2 = int(move[2]), int(move[3]), int(move[4]), int(move[5])
        self.validate_points(x1, y1, x2, y2)
        self.validate_pp(x1, y1, move[0])
        if not ((x2, y2) in self[x1, y1].valid_bagh_moves()):
            raise Exception(
                f"Error. {move} is not a valid move.")
        return True

    def validate_points(self, x1, y1, x2=1, y2=1):
        if not (0 < x1 < 6 and 0 < y1 < 6 and 0 < x2 < 6 and 0 < y2 < 6):
            raise Exception(
                "Invalid PGN. Coordinates not in range.")

    def validate_pp(self, x1, y1, p):
        if not self[x1, y1]:
            raise Exception(f"({x1},{y1}) is not occupied.")
        if self[x1, y1].__str__() != p:
            raise Exception(f"Piece at ({x1},{y1}) is other than specified.")

    def safe_move(self, move):
        if self.is_game_over(): raise Exception("The game is already over.")
        if len(move) == 3:
            Goat(self, (int(move[1]), int(move[2])))
            self.no_of_goat_moves += 1
            self.goats_placed += 1
        else:
            if len(move) == 5:
                x1, y1, x2, y2 = int(move[1]), int(
                    move[2]), int(move[3]), int(move[4])
            elif len(move) == 6:
                x1, y1, x2, y2 = int(move[2]), int(
                    move[3]), int(move[4]), int(move[5])
                x3, y3 = (x1 + x2) // 2, (y1 + y2) // 2
                self[x3, y3] = 0
                self.goat_points.remove((x3, y3))
                self.goats_captured += 1
            self[x1, y1] = 0
            if move[0] == "G":
                self.goat_points.remove((x1, y1))
                Goat(self, (x2, y2))
                self.no_of_goat_moves += 1
            elif move[0] == "B":
                self.bagh_points.remove((x1, y1))
                Bagh(self, (x2, y2))
                self.no_of_bagh_moves += 1

        pgn_update=""
        if self.next_turn=="G":pgn_update+=f"{self.no_of_goat_moves}. "
        pgn_update+=move
        self.pgn+=" "+pgn_update
        self.next_turn = "G" if self.next_turn == "B" else "B"
        self.fen = self.board_to_fen()

    def board_to_fen(self):
        string = ""
        for x in range(1, 6):
            counter = 0
            for y in range(1, 6):
                if self[x, y]:
                    counter = 0
                    string += self[x, y].__str__()
                else:
                    counter += 1
                    if y == 5 or self[x, y + 1] != 0:
                        string += str(counter)
            string += "/"
        return f"{string[:-1]} {self.next_turn} {self.no_of_goat_moves}"

    def move(self, move):
        if self.validate(move):
            self.safe_move(move)
            print(move)
            self.show_board()

    def is_game_over(self):
        if self.goats_captured >= 5: return "B"
        if self.baghs_trapped == 4: return "G"
        return 0


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


class Bagh(Piece):

    def __init__(self, board, position):
        super(Bagh, self).__init__(board, position)
        self.board.bagh_points.add(position)

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

    def valid_non_special_moves(self):
        return super(Bagh, self).valid_moves()


class Goat(Piece):

    def __init__(self, board, position):
        super(Goat, self).__init__(board, position)
        self.board.goat_points.add(position)

    def __str__(self):
        return "G"

    def __repr__(self):
        return "Goat"


#b = Board("1. G33 B1525 2. G14 B2524 3. G43 Bx2442 4. G21 B5554 5. G23 B5455 6. G33 B5554 7. G31 B5455 8. G25 B5554 9. G55 B5444 10. G12 B4241 11. G35 B4445 12. G54 B1122 13. G11 B2232 14. G34 B3242 15. G32 Bx4224 16. G33 B2413 17. G52 Bx5153 18. G51 B5344 19. G52 Bx4424 20. G34")
#b.show_board()

