from typing import Optional, Tuple, List
import maze as maze_module


def create_runner(x: int=0, y: int=0, orientation: str='N'):
    return {'x':x, 'y':y, 'orientation':orientation}

def get_x(runner):
    return runner['x']

def get_y(runner):
    return runner['y']

def get_orientation(runner):
    return runner['orientation']

def turn(runner, direction: str):
    all_orientations=['N', 'E', 'S', 'W']
    index=all_orientations.index(runner['orientation'])
    if direction=='Left':
        index=index-1
        runner['orientation']=all_orientations[index]
    elif direction=='Right':
        index=index+1
        if index==4:
            index=0
        runner['orientation']=all_orientations[index]
    return runner

def forward(runner):
    if runner['orientation']=='N':
        runner['y']+=1
    elif runner['orientation']=='E':
        runner['x']+=1
    elif runner['orientation']=='S':
        runner['y']-=1
    elif runner['orientation']=='W':
        runner['x']-=1
    return runner

def sense_walls(runner, maze) -> Tuple[bool, bool, bool]:
    walls=maze_module.get_walls(maze, runner['x'], runner['y'])
    #go_straight(runner, maze)according to get_walls, 0=N, 1=E, 2=S, 3=W
    if runner['orientation']=='N':
        Front=walls[0]
        Right=walls[1]
        Left=walls[3]
    elif runner['orientation']=='E':
        Front=walls[1]
        Right=walls[2]
        Left=walls[0]
    elif runner['orientation']=='S':
        Front=walls[2]
        Right=walls[3]
        Left=walls[1]
    elif runner['orientation']=='W':
        Front=walls[3]
        Right=walls[0]
        Left=walls[2]
    return (Left, Front, Right)

def go_straight(runner, maze):
    walls=sense_walls(runner, maze)
    if walls[1] != True:
        forward(runner)
        return runner
    else:
        raise ValueError

def move(runner, maze):
    original_pos={'x':runner['x'], 'y':runner['y'], 'orientation':runner['orientation']}
    action=""
    all_actions=""
    turn(runner, 'Left')
    action+="L"
    while original_pos['x']==runner['x'] and original_pos['y']==runner['y']:
        try:
            go_straight(runner, maze)
        except  ValueError:
            turn(runner, 'Right')
            action+="R"
            if action=="LR" or action=="RL":
                action=""
        else:
            action+="F"
            all_actions+=action
    return (runner, all_actions)

def explore(runner, maze, goal : Optional[Tuple[int, int]]=None) -> Tuple[str, List[Tuple[int, int]]]:
    passed_pos=[(runner['x'], runner['y'])]
    whole_movement=""
    if goal is None:
        dimension=maze_module.get_dimensions(maze)
        goal=(dimension[0]-1, dimension[1]-1)
    while runner['x']!=goal[0] or runner['y']!=goal[1]:
        movement=move(runner, maze)
        passed_pos.append((runner['x'], runner['y']))
        whole_movement+=movement[1]
    return (whole_movement, passed_pos) 
    #The return value is change since it will be useful for the shortest_path function in maze_runner.py

