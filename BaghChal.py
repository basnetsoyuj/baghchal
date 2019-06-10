'''
fen -> Similar to Forsyth–Edwards Notation in chess

'''
import numpy as np
import pickle

with open("data/points_link.pickle",'rb') as f:
    connected_points_dict=pickle.load(f)

class Board:
    def __init__(self, fen="B3B/5/5/5/B3B G 0"):
        self.fen = fen

    def show_board(self):
        rows = self.fen.split(" ")[0].split("/")
        print("--------------------------")
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
            print("--------------------------")


class Piece:
    def __init__(self, position):
        self.position = position

    def connected_points(self):
        return connected_points_dict[self.position]