# Basic Minesweeper Game using the command line.
# author: nk
# date: 10th Sept, 2021

import random

BOX_CHAR = '☐'
neighbors = [[-1,-1],[0, -1],[1, -1],[-1,0],[1, 0],[-1,1],[0, 1],[1, 1]]

# random.seed(234)

class MineField:
    
    def __init__(self, size, mine_density):
        self.size = size
        self.mine_field = [[ 'X' if random.randint(0,10) > (10 - mine_density) else '.' for i in range(size)] for j in range(size)]
        self.probability_map = [[0 for i in range(size)] for j in range(size)]
        self.touched_tiles = [[0 for i in range(size)] for j in range(size)]
        self.mineHit = False
        
        for i in range(self.size):
            for j in range(self.size):
                if self.mine_field[i][j] != 'X':
                    # print("empty")
                    neighborCount = 0
                    for n in range(len(neighbors)):
                        y = i + neighbors[n][1]
                        x = j + neighbors[n][0]
                        # print(f'x:{x},y:{y}')
                        if y >= 0 and y < self.size and x >= 0 and x < self.size:
                            if self.mine_field[y][x] == 'X':
                                neighborCount += 1
                    self.probability_map[i][j] = neighborCount
                    # print(f'{i},{j} has {neighborCount} neighbor{'s' if neighborCount == 1 else ''}.')
    
    '''
    Prints the current state of the minefield to the console.
    '''
    def printMinefield(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.touched_tiles[i][j]:
                    if self.mine_field[i][j] != 'X':
                        if self.probability_map[i][j] == 0:
                            print('.', end = " ")
                        else:
                            print(self.probability_map[i][j], end = " ")
                    else:
                        if self.mineHit:
                            print('X', end = " ")
                        else:
                            print(BOX_CHAR, end = " ")
                else:
                    if self.mineHit and self.mine_field[i][j] == 'X':
                        print('X', end = " ")
                    elif self.mine_field[i][j] == 'M':
                        print('+', end = " ")
                    else:
                        print(BOX_CHAR, end = " ")
            print()
    
    '''
    Tells us if a cell contains a mine or not.
    '''
    def checkTile(self, x, y):
        return True if self.mine_field[y][x] == 'X' else False
    
    '''
    Recursively digs all neighboring cells with 0 probability until first non-zero neighbors.
    '''
    def digNearby(self, x, y):
        if not self.touched_tiles[y][x]:
            self.touched_tiles[y][x] = 1
        
        for n in range(len(neighbors)):
            x1 = x + neighbors[n][1]
            y1 = y + neighbors[n][0]
            if x1 >= 0 and x1 < self.size and y1 >= 0 and y1 < self.size:
                if not self.touched_tiles[y1][x1]:
                    if self.probability_map[y1][x1] == 0:
                        self.digNearby(x1, y1)
                    else:
                        self.touched_tiles[y1][x1] = 1
    
    def touchTile(self, x, y):
        self.touched_tiles[y][x] = 1
        if self.probability_map[y][x] == 0:
            # recursive function to dig all neighbors until non-zeros are reached.
            self.digNearby(x, y)
    
    def markTile(self, x, y):
        self.mine_field[y][x] = 'M'
    
    def printProbabilityMap(self):
        for row in self.probability_map:
            for cell in row:
                print(cell, end = " ")
            print()
    

if __name__ == '__main__':
    
    fieldSize = 16
    m = MineField(fieldSize, 2) # density from 0 ~ 10
    m.printMinefield()
    
    user_command = ""
    
    while user_command != "Q":
        print("Commands:")
        print("Q -> quit, T -> touch tile, M -> mark bomb")
        user_command = input("Enter command: ")
        
        if user_command == "T" or user_command == "M":
            x = int(input("X = "))
            y = int(input("Y = "))
            if x < 0 or x > fieldSize - 1:
                print(f'X coordinate out of bounds. Enter a coordinate between 0 and {fieldSize-1}')
                continue
            if y < 0 or y > fieldSize - 1:
                print(f'Y coordinate out of bounds. Enter a coordinate between 0 and {fieldSize-1}')
                continue
            
            if user_command == "T":
                m.touchTile(x, y)
            
                if m.checkTile(x, y):
                    user_command = "Q"
                    m.mineHit = True
                    print("You hit a mine!")
                    
            elif user_command == "M":
                m.markTile(x, y)
                
            print("-"*32)
            m.printMinefield()
            print("-"*32)
            
    print("-- GAME OVER --")