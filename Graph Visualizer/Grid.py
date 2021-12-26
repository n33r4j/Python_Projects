# Grid Class

import pygame
from Colors import *


class Grid:
    def __init__(self, position, width, height, cell_size, line_color=(255,255,255), line_thickness=1):
        self.position = position
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.line_color = line_color
        self.line_thickness = line_thickness
        self.state_matrix = [[0 for i in range(width)] for j in range(height)]
        self.dist_matrix = [[0 for i in range(width)] for j in range(height)] # for storing distances from start
        # 0 -> empty(Black), -1 -> Wall(White), 1 -> Currently Active(Orange), 2 -> Explored(Dark Blue), 
        # 3 -> Found but to be visited(Yellow), 4 -> Start(Green), 5 -> Goal(Red), 6 -> Ideal Path(Light Blue)

    def setStateMatrix(self, state_matrix):
        self.state_matrix = state_matrix

    def setDistMatrix(self, dist_matrix):
        self.dist_matrix = dist_matrix

    def setCellState(self, row, column, state):
        self.state_matrix[row][column] = state

    def Draw(self, window):
        # Draw Vertical grid lines
        for i in range(self.width+1):
            X = self.position[0]+(i*self.cell_size)
            start_Y = self.position[1]
            end_Y = self.position[1]+(self.cell_size*self.height)
            pygame.draw.aaline(window, self.line_color, (X,start_Y), (X,end_Y), self.line_thickness)

        # Draw Horizontal grid lines
        for i in range(self.height+1):
            Y = self.position[1]+(i*self.cell_size)
            start_X = self.position[0]
            end_X = self.position[0]+(self.cell_size*self.height)
            pygame.draw.aaline(window, self.line_color, (start_X,Y), (end_X,Y), self.line_thickness)

        for i in range(self.height):
            for j in range(self.width):
                cell_color = (0,0,0)
                curr_cell = self.state_matrix[i][j]

                if  curr_cell == -1:
                    cell_color = L_GREY
                elif curr_cell == 1:
                    cell_color = ORANGE
                elif curr_cell == 2:
                    cell_color = D_BLUE
                elif curr_cell == 3:
                    cell_color = YELLOW
                elif curr_cell == 4:
                    cell_color = GREEN
                elif curr_cell == 5:
                    cell_color = RED
                elif curr_cell == 6:
                    cell_color = L_BLUE
                else:
                    pass
                
                # For filling cells with circles
                # X = self.position[0] + (j*self.cell_size)+(self.cell_size/2)
                # Y = self.position[1] + (i*self.cell_size)+(self.cell_size/2)
                # pygame.draw.circle(window, cell_color, (X,Y), (0.9*self.cell_size)/2)

                # For filling cells with rects
                X = self.position[0] + (j*self.cell_size)+2
                Y = self.position[1] + (i*self.cell_size)+2
                pygame.draw.rect(window, cell_color, pygame.Rect(X,Y,self.cell_size-3,self.cell_size-3))

    