'''
fen -> Similar to Forsyth–Edwards Notation in chess

'''
import numpy as np


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
        if self.position[0] == 1:
            y = np.array([0, 0, 0, 1])
        elif self.position[0] == 5:
            y = np.array([0, -1, 0, 0])
        else:
            y = np.array([0, -1, 0, +1])
        if self.position[1] == 1:
            x = np.array([1, 0, 0, 0])
        elif self.position[1] == 5:
            x = np.array([0, 0, -1, 0])
        else:
            x = np.array([1, 0, -1, 0])
        points = connect(
            np.array(self.position[0])+x, np.array(self.position[0])+y)-{self.position}
        return points

def connect(x,y):
    return {(x[i],y[i]) for i in range(len(x))}
p=Piece((1,2))
print(p.connected_points())