# Grid Visualization for Path Finding Algorithms
#
# Grassfire and A* implemented
# Try PRM and RRT for non-grid based maps.
#
# Notes:
# - There's probably a better way to write the code for searching neighbouring cells. Maybe using a dict ?
# - The A* implementation isn't correct. The way that the optimal path is found needs to be done by keeping
#   track of the parent nodes instead of assigning numbers like the grassfire algorithm.
# - 

import pygame

from Grid import Grid
from Colors import *
from PriorityQueue import PriorityQueue
import random

WIDTH, HEIGHT = 1000, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Visualizer")

FPS_MAX = 60
SIM_RUN = True
SIM_PAUSED = False

# GRID_SIZE = 46
# GRID_WIDTH = 12
# GRID_HEIGHT = 12


map_WIDTH, map_HEIGHT = 33, 33
cell_SIZE = 20
map = [[0 for i in range(map_WIDTH)] for j in range(map_HEIGHT)]
dist_mat = [[0 for i in range(map_WIDTH)] for j in range(map_HEIGHT)]

# Create Walls
def addWall(axis, rank, start, end):
    if axis == 0:
        for i in range(start, min(end, map_WIDTH-1)):
            map[min(rank, map_HEIGHT-1)][i] = -1
    elif axis == 1:
        for i in range(start, min(end, map_HEIGHT-1)):
            map[i][min(rank, map_WIDTH-1)] = -1

# Create Random Walls, density ~ 0.0 - 1.0
def addRandomWalls(density):
    for i in range(map_HEIGHT):
        for j in range(map_WIDTH):
            num = random.random()
            if num < density:
                map[i][j] = -1

# addWall(0, 4, 0, 35)
# addWall(0, 8, 1, 36)
# addWall(0, 12, 0, 35)
# addWall(0, 16, 1, 36)
addWall(0, 25, 5, 24)
addWall(0, 30, 1, 26)
# addWall(0, 28, 0, 35)
# addWall(0, 32, 1, 36)
addWall(1, 20, 1, 30)
# addWall(1, 30, 27, 35)

addRandomWalls(0.0)

# Sets
def TracePath(goal, map, dist_mat):
    row = goal[0]
    col = goal[1]
    stepfound = False

    while dist_mat[row][col]:
        # print("stepping...", row, col)
        
        # UP
        if row-1 >= 0 and map[row-1][col] > 0 and dist_mat[row-1][col] < dist_mat[row][col]:
            row -= 1
            stepfound = True
        # UP-RIGHT
        elif row-1 >= 0 and col+1 <= map_WIDTH-1 and map[row-1][col+1] > 0 and dist_mat[row-1][col+1] < dist_mat[row][col]:
            row -= 1
            col += 1
            stepfound = True
        # RIGHT
        elif col+1 <= map_WIDTH-1 and map[row][col+1] > 0 and dist_mat[row][col+1] < dist_mat[row][col]:
            col += 1
            stepfound = True
        # DOWN-RIGHT
        elif row+1 <= map_HEIGHT-1 and col+1 <= map_WIDTH-1 and map[row+1][col+1] > 0 and dist_mat[row+1][col+1] < dist_mat[row][col]:
            row += 1
            col += 1
            stepfound = True
        # DOWN
        elif row+1 <= map_HEIGHT-1 and map[row+1][col] > 0 and dist_mat[row+1][col] < dist_mat[row][col]:
            row += 1
            stepfound = True
        # DOWN-LEFT
        elif row+1 <= map_HEIGHT-1 and col-1 >= 0 and map[row+1][col-1] > 0 and dist_mat[row+1][col-1] < dist_mat[row][col]:
            row += 1
            col -= 1
            stepfound = True
        # LEFT
        elif col-1 >= 0 and map[row][col-1] > 0 and dist_mat[row][col-1] < dist_mat[row][col]:
            col -= 1
            stepfound = True
        # UP-LEFT
        elif row-1 >= 0 and col-1 >= 0 and map[row-1][col-1] > 0 and dist_mat[row-1][col-1] < dist_mat[row][col]:
            row -= 1
            col -= 1
            stepfound = True
        
        if stepfound:
            stepfound = False
            if dist_mat[row][col]:
                map[row][col] = 6
                # print(dist_mat[row][col])
        else:
            print("No path found.")
            break
    
    return map


def Grassfire(start, goal, grid):
    toVisit = []
    toVisit.append(start)
    global map
    global dist_mat
    map[start[0]][start[1]] = 0
    map[goal[0]][goal[1]] = 5
    
    clock = pygame.time.Clock()
    global SIM_RUN
    timer = 0 # Set the timer in ms to control the update speed.
    timer_start = 0
    goal_found = False


    while SIM_RUN:
        clock.tick(FPS_MAX)
        # print("running")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIM_RUN = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

        if not SIM_PAUSED:
            currTime = pygame.time.get_ticks()
            # print(currTime)

            if currTime - timer_start > timer:
                # print("step",currTime)
                timer_start = currTime

                if toVisit and not goal_found:
                    # print(toVisit[0], goal)
                    if(toVisit[0] == goal):
                        # print("Goal found!")
                        print(f"Shortest path to goal is {dist_mat[toVisit[0][0]][toVisit[0][1]]} units.")
                        map[goal[0]][goal[1]] = 5
                        goal_found = True
                        grid.setStateMatrix(TracePath(goal, map, dist_mat))
                        draw_window(grid)
                        continue

                    row = toVisit[0][0]
                    col = toVisit[0][1]
                    if not toVisit[0] == start:
                        map[row][col] = 2
                    else:
                        map[row][col] = 4
                    # print(curr_num, row, col, toVisit)
                    # UP
                    if row > 0 and map[row-1][col] in [0,5]:
                        if dist_mat[row-1][col] == 0 or dist_mat[row][col]+1 < dist_mat[row-1][col]:
                            dist_mat[row-1][col] = dist_mat[row][col]+1
                        
                        if not map[row-1][col] == 5:
                            map[row-1][col] = 3
                        toVisit.append((row-1,col))
                    # UP-RIGHT
                    if row > 0 and col < map_WIDTH-1 and map[row-1][col+1] in [0,5]:
                        if dist_mat[row-1][col+1] == 0 or dist_mat[row][col]+1 < dist_mat[row-1][col+1]:
                            dist_mat[row-1][col+1] = dist_mat[row][col]+1
                        if not map[row-1][col+1] == 5:
                            map[row-1][col+1] = 3
                        toVisit.append((row-1,col+1))
                    # RIGHT
                    if col < map_WIDTH-1 and map[row][col+1] in [0,5]:
                        if dist_mat[row][col+1] == 0 or dist_mat[row][col]+1 < dist_mat[row][col+1]:
                            dist_mat[row][col+1] = dist_mat[row][col]+1
                        if not map[row][col+1] == 5:
                            map[row][col+1] = 3
                        toVisit.append((row,col+1))
                    # DOWN-RIGHT
                    if row < map_HEIGHT-1 and col < map_WIDTH-1 and map[row+1][col+1] in [0,5]:
                        if dist_mat[row+1][col+1] == 0 or dist_mat[row][col]+1 < dist_mat[row+1][col+1]:
                            dist_mat[row+1][col+1] = dist_mat[row][col]+1
                        if not map[row+1][col+1] == 5:
                            map[row+1][col+1] = 3
                        toVisit.append((row+1,col+1))
                    # DOWN
                    if row < map_HEIGHT-1 and map[row+1][col] in [0,5]:
                        if dist_mat[row+1][col] == 0 or dist_mat[row][col]+1 < dist_mat[row+1][col]:
                            dist_mat[row+1][col] = dist_mat[row][col]+1
                        if not map[row+1][col] == 5:
                            map[row+1][col] = 3
                        toVisit.append((row+1,col))
                    # DOWN-LEFT
                    if row < map_HEIGHT-1 and col > 0 and map[row+1][col-1] in [0,5]:
                        if dist_mat[row+1][col-1] == 0 or dist_mat[row][col]+1 < dist_mat[row+1][col-1]:
                            dist_mat[row+1][col-1] = dist_mat[row][col]+1
                        if not map[row+1][col-1] == 5:
                            map[row+1][col-1] = 3
                        toVisit.append((row+1,col-1))
                    # LEFT
                    if col > 0 and map[row][col-1] in [0,5]:
                        if dist_mat[row][col-1] == 0 or dist_mat[row][col]+1 < dist_mat[row][col-1]:
                            dist_mat[row][col-1] = dist_mat[row][col]+1
                        if not map[row][col-1] == 5:
                            map[row][col-1] = 3
                        toVisit.append((row,col-1))
                    # UP-LEFT
                    if row > 0 and col > 0 and map[row-1][col-1] in [0,5]:
                        if dist_mat[row-1][col-1] == 0 or dist_mat[row][col]+1 < dist_mat[row-1][col-1]:
                            dist_mat[row-1][col-1] = dist_mat[row][col]+1
                        if not map[row-1][col-1] == 5:
                            map[row-1][col-1] = 3
                        toVisit.append((row-1,col-1))
                    
                    
                    toVisit.pop(0)
                    grid.setStateMatrix(map)
                    grid.setDistMatrix(dist_mat)
                    draw_window(grid)

# Euclidean Distance -> Heuristic
def Dist(start, goal):
    x1, y1 = start
    x2, y2 = goal
    dist = ((x2-x1)**2 + (y2-y1)**2)**0.5
    return dist


def AStar(start, goal, grid):
    toVisit = PriorityQueue()
    toVisit.addItem(start, 0)
    global map
    global dist_mat
    map[start[0]][start[1]] = 0
    map[goal[0]][goal[1]] = 5
    
    clock = pygame.time.Clock()
    global SIM_RUN
    timer = 0 # ms, for controlling update speed.
    timer_start = 0
    goal_found = False


    while SIM_RUN:
        clock.tick(FPS_MAX)
        # print("running")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                SIM_RUN = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

        if not SIM_PAUSED:
            currTime = pygame.time.get_ticks()
            # print(currTime)

            if currTime - timer_start > timer:
                # print("step",currTime)
                timer_start = currTime

                if toVisit and not goal_found:
                    # print(toVisit[0], goal)
                    if not toVisit.isEmpty():
                        curr_cell = toVisit.get_removeMinCell()
                    else:
                        print("Path not found...")
                        break
                    # print(curr_cell)
                    if( curr_cell == goal):
                        # print("Goal found!")
                        # Print this on to the screen instead of just the console.
                        print(f"Shortest path to goal is {dist_mat[curr_cell[0]][curr_cell[1]]} units.")                        
                        map[goal[0]][goal[1]] = 5
                        goal_found = True
                        grid.setStateMatrix(TracePath(goal, map, dist_mat))
                        draw_window(grid)
                        continue

                    row, col = curr_cell

                    if not curr_cell == start:
                        map[row][col] = 2
                    else:
                        map[row][col] = 4
                    # print(curr_num, row, col, toVisit)
                    # UP
                    if row > 0 and map[row-1][col] in [0,5]:
                        dist_mat[row-1][col] = dist_mat[row][col]+1
                        if not map[row-1][col] == 5:
                            map[row-1][col] = 3
                        
                        toVisit.addItem([row-1,col], Dist([row-1,col], goal))
                    # UP-RIGHT
                    if row > 0 and col < map_WIDTH-1 and map[row-1][col+1] in [0,5]:
                        dist_mat[row-1][col+1] = dist_mat[row][col]+1
                        if not map[row-1][col+1] == 5:
                            map[row-1][col+1] = 3
                        
                        toVisit.addItem([row-1,col+1], Dist([row-1,col+1], goal))
                    # RIGHT
                    if col < map_WIDTH-1 and map[row][col+1] in [0,5]:
                        dist_mat[row][col+1] = dist_mat[row][col]+1
                        if not map[row][col+1] == 5:
                            map[row][col+1] = 3
                        
                        toVisit.addItem([row,col+1], Dist([row,col+1], goal))
                    # DOWN-RIGHT
                    if row < map_HEIGHT-1 and col < map_WIDTH-1 and map[row+1][col+1] in [0,5]:
                        dist_mat[row+1][col+1] = dist_mat[row][col]+1
                        if not map[row+1][col+1] == 5:
                            map[row+1][col+1] = 3
                        
                        toVisit.addItem([row+1,col+1], Dist([row+1,col+1], goal))
                    # DOWN
                    if row < map_HEIGHT-1 and map[row+1][col] in [0,5]:
                        dist_mat[row+1][col] = dist_mat[row][col]+1
                        if not map[row+1][col] == 5:
                            map[row+1][col] = 3
                        
                        toVisit.addItem([row+1,col], Dist([row+1,col], goal))
                    # DOWN-LEFT
                    if row < map_HEIGHT-1 and col > 0 and map[row+1][col-1] in [0,5]:
                        dist_mat[row+1][col-1] = dist_mat[row][col]+1
                        if not map[row+1][col-1] == 5:
                            map[row+1][col-1] = 3
                        
                        toVisit.addItem([row+1,col-1], Dist([row+1,col-1], goal))
                    # LEFT
                    if col > 0 and map[row][col-1] in [0,5]:
                        dist_mat[row][col-1] = dist_mat[row][col]+1
                        if not map[row][col-1] == 5:
                            map[row][col-1] = 3
                        
                        toVisit.addItem([row,col-1], Dist([row,col-1], goal))
                    # UP-LEFT
                    if row > 0 and col > 0 and map[row-1][col-1] in [0,5]:
                        dist_mat[row-1][col-1] = dist_mat[row][col]+1
                        if not map[row-1][col-1] == 5:
                            map[row-1][col-1] = 3
                        
                        toVisit.addItem([row-1,col-1], Dist([row-1,col-1], goal))
                    

                    grid.setStateMatrix(map)
                    grid.setDistMatrix(dist_mat)
                    draw_window(grid)
                
                elif not toVisit and not goal_found:
                    print("Goal not found. Terminating Search...")


def draw_window(grid):
    window.fill(BLACK)
    
    # create_grid((10,10), GRID_WIDTH, GRID_HEIGHT, GRID_SIZE)
    grid.Draw(window)

    # for node in nodes:
    #     node.Draw(window)
    
    pygame.display.update()


def main():
    pygame.init()
    # clock = pygame.time.Clock()
    # global SIM_RUN
    
    grid = Grid((10,10), map_WIDTH, map_HEIGHT, cell_SIZE)
    # grid.setState(map)

    # Pathfinding Algorithms:
    Grassfire((2,2),(26,30), grid)
    # AStar([2,2],[26,30], grid) # start and goal needs to be lists.
    
    pygame.quit()
    print("Simulation Terminated...")
    
    # for row in grid.dist_matrix:
    #     print(row)
    

if __name__ == "__main__":
    main()