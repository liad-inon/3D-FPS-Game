import random

def build(maze, minimum_bound, lower_bounds, upper_bounds, hor_passes=[], ver_passes=[]):
    if upper_bounds[0]-lower_bounds[0] < minimum_bound or upper_bounds[1]-lower_bounds[1] < minimum_bound:
        return maze

    hor_wall_pos = random.choice( list(set(range(lower_bounds[1]+1, upper_bounds[1]-1, 2)).difference(set(hor_passes))) )
    ver_wall_pos = random.choice( list(set(range(lower_bounds[0]+1, upper_bounds[0]-1, 2)).difference(set(ver_passes))) )
    hor_passes = [None, None]
    ver_passes = [None, None]

    for i in range(lower_bounds[0], upper_bounds[0]): 
        maze[hor_wall_pos][i] = 1
    
    ver_passes[0] = random.randrange(lower_bounds[0], ver_wall_pos, 2)
    maze[hor_wall_pos][ver_passes[0]] = 0
    ver_passes[1] = random.randrange(ver_wall_pos+1, upper_bounds[0], 2)
    maze[hor_wall_pos][ver_passes[1]] = 0

    for i in range(lower_bounds[1], upper_bounds[1]): 
        maze[i][ver_wall_pos] = 1
    
    hor_passes[0] = random.randrange(lower_bounds[1], hor_wall_pos, 2)
    maze[hor_passes[0]][ver_wall_pos] = 0
    hor_passes[1] = random.randrange(hor_wall_pos+1, upper_bounds[1], 2)
    maze[hor_passes[1]][ver_wall_pos] = 0

    maze = build(maze, minimum_bound, [ver_wall_pos+1, hor_wall_pos+1], upper_bounds[:])
    maze = build(maze, minimum_bound, lower_bounds[:], [ver_wall_pos, hor_wall_pos])
    maze = build(maze, minimum_bound, [ver_wall_pos+1, lower_bounds[1]], [upper_bounds[0], hor_wall_pos])
    maze = build(maze, minimum_bound, [lower_bounds[0], hor_wall_pos+1], [ver_wall_pos, upper_bounds[1]])

    return maze
    

def generate_maze(size, hall_size_bound):
    if size[0] %2 == 0 or size[1] %2 == 0:
        raise ValueError("Size must be an odd number.")
    if hall_size_bound < 1 or hall_size_bound > size[0]+2 or hall_size_bound > size[1]+2:
        raise ValueError("hall_size_bound is out of bounds (hall_size < 1 or hall_size > size[0]+2 or hall_size > size[1]+2).")

    maze = [[0 for raw in range(size[0])] for cloumn in range(size[1])]
    maze = build(maze, hall_size_bound+2, [0, 0], [size[0], size[1]])

    for raw in maze:
        raw.insert(0, 1)
        raw.insert(size[1]+1, 1)
    
    maze.insert(0, [1]*(size[1]+2))
    maze.insert(size[0]+1, [1]*(size[1]+2))

    return maze
