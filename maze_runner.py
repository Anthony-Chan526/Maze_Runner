import maze as maze_module
import runner as runner_module
import argparse
import csv
from typing import Optional, Tuple, List

def shortest_path(maze, starting: Optional[Tuple[int, int]]=None, goal: Optional[Tuple[int, int]]=None) -> List[Tuple[int, int]]:
    if starting is None:
        starting=(0, 0)
    if goal is None:
        dimension=maze_module.get_dimensions(maze)
        goal=(dimension[0]-1, dimension[1]-1)
    runner=runner_module.create_runner(starting[0], starting[1]) 
    exploration=runner_module.explore(runner, maze, goal)
    
    #The return value of the explore function in runner.py is changed to a tuple with two elements. First element is the sequence of actions and the second one is a list of tuples required in this funtion
    paths=exploration[1]
    modified_paths=[]
    repeat_index=0
    for location in paths:
        if location in modified_paths:
            repeat_index=modified_paths.index(location)
            modified_paths=modified_paths[:repeat_index]
        modified_paths.append(location)
    return modified_paths


def maze_reader(maze_file: str):
    try:
        with open(maze_file, 'r') as file:
            lines = [line.rstrip('\n') for line in file.readlines()]
    except (OSError, IOError, FileNotFoundError) as e:
        raise IOError

    maze = [list(row) for row in lines]
    dimension=maze_module.get_dimensions(maze)
    
    #check if the maze has a valid dimension or not
    if dimension[0]<1 or dimension[1]<1:
        raise ValueError
    
    #check if the width is consistent
    width=len(maze[0])
    for i in range(1, len(maze)): 
        if len(maze[i])!=width:
            raise ValueError
    
    #check if the maze are fully closed
    for x in range(len(maze[0])):
        if maze[0][x]!="#" or maze[-1][x]!="#":
            raise ValueError
    for y in range(len(maze)):
        if maze[y][0]!="#" or maze[y][-1]!="#":
            raise ValueError

    #check if the format of the maze is valid
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x]!="#" and maze[y][x]!=".":
                raise ValueError
            #check if the grid cell is vaild(e.g.it is not a wall with "#")
            if x%2==1 and y%2==1:
                if maze[y][x]!=".":
                    raise ValueError
            #check intersections between horizontal amd vertical lines
            if x%2==0 and y%2==0:
                if maze[y][x]!="#":
                    raise ValueError
    return maze


def main():
    parser = argparse.ArgumentParser(description="ECS Maze Runner")
    parser.add_argument(
        "maze", type=str, help="The name of the maze file, e.g., maze1.mz"
    )
    parser.add_argument('--starting', help='The starting position, e.g., "2, 1"')
    parser.add_argument('--goal', help='The goal position, e.g., "4, 5"')
    args = parser.parse_args()
    try:
        maze = maze_reader(args.maze)
    except IOError:
        raise IOError
    except ValueError:
        raise ValueError
    
    #collect starting position and detect whether it is vaild
    if args.starting:
        star_x, start_y = map(int, args.starting.split(','))
        dimension=maze_module.get_dimensions(maze)
        if start_x>dimension[0]-1 or start_y>dimension[1]-1 or start_x<0 or start_y<0:
            raise ValueError
        else:
            start_pos=(start_x, start_y)
    else:
        start_pos=None
    
    #collect goal position and detect whether it is vaild
    if args.goal:
        goal_x, goal_y = map(int, args.goal.split(','))
        dimension=maze_module.get_dimensions(maze)
        if goal_x>dimension[0]-1 or goal_y>dimension[1]-1 or goal_x<0 or goal_y<0:
            raise ValueError
        else:
            goal_pos=(goal_x, goal_y)
    else:
        goal_pos=None

    #create exploration.csv
    with open('exploration.csv', 'w', newline='') as file1:
        headers=['Step', 'x-coordinate', 'y-coordinate', 'Actions']
        writer=csv.DictWriter(file1,fieldnames=headers)
        writer.writeheader()
        if start_pos is None:
            runner=runner_module.create_runner()
        else:
            runner=runner_module.create_runner(start_pos[0], start_pos[1])
        exploration=runner_module.explore(runner, maze, goal_pos)
        
        #make the action sequence become a list of actions
        moves=''
        actions=[]
        for char in exploration[0]:
            moves+=char
            if char=='F':
                actions.append(moves)
                moves=''
        
        #write data to the csv
        for i in range (len(actions)):
            x=exploration[1][i][0]
            y=exploration[1][i][1]
            writer.writerow({'Step':i+1, 'x-coordinate':x, 'y-coordinate':y, 'Actions':actions[i]})

    #create statistics.txt
    with open('statistics.txt', 'w') as file2:
        exploration_steps=len(exploration[1])-1
        path_length=len(shortest_path(maze, start_pos, goal_pos))
        score=exploration_steps/4+path_length
        lines=[args.maze, str(score), str(exploration_steps), str(shortest_path(maze, start_pos, goal_pos)), str(path_length)]
        for line in lines:
            file2.write(line + '\n')
if __name__ == "__main__":
    main()
