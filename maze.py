from typing import Tuple

def create_maze(width: int=5, height: int=5):
    maze = []
    for y in range(height*2+1):
        maze.append([])
        for x in range(width*2+1):
            if x == 0 or x == width*2 or y == 0 or y == height*2:
                maze[y].append("#")
            elif x%2==0 and y%2==0:
                maze[y].append("#")
            else: 
                maze[y].append(".")
    return maze

def add_horizontal_wall(maze, x_coordinate, horizontal_line):

    maze[-(horizontal_line*2+1)][x_coordinate*2+1]="#"

def add_vertical_wall(maze, y_coordinate, vertical_line):
    maze[-(y_coordinate*2+2)][vertical_line*2]="#"

def get_dimensions(maze) -> tuple[int, int]:
    y=int((len(maze)-1)/2)
    x=int((len(maze[1])-1)/2)
    return (x, y)

def get_walls(maze, x_coordinate: int, y_coordinate: int) -> Tuple[bool, bool, bool, bool]:
    North=East=South=West=False
    if maze[-((y_coordinate+1)*2)-1][x_coordinate*2+1]=="#":
        North=True
    if maze[-((y_coordinate+1)*2)][x_coordinate*2+2]=="#":
        East=True
    if maze[-((y_coordinate+1)*2)+1][x_coordinate*2+1]=="#":
        South=True
    if maze[-((y_coordinate+1)*2)][x_coordinate*2]=="#":
        West=True
    return (North, East, South, West)
