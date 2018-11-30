import requests, time

# some useful global variables
url_that_returns_token = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session'
maze_url_template = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token='
token = requests.post(url_that_returns_token,
                      data = {'uid': '104790253'}).json()['token']
maze_state_url = maze_url_template + token
url_to_move_in_maze = maze_url_template + token
opposite_direction = {
    'UP': 'DOWN',
    'DOWN': 'UP',
    'LEFT': 'RIGHT',
    'RIGHT': 'LEFT'
}
direction_to_deltas = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

# defining the Maze struct which stores path & known 2D representation of maze
class Maze():
    def __init__(self, representation):
        self.path = []
        self.representation = representation

# toplevel algorithm
def solve_challenge():
    game_details = get_game_details() # so we don't waste time get requesting
    if game_details['status'] == 'FINISHED':
        print('You have completed the mazes!')
        return True
    elif game_details['status'] == 'PLAYING':
        print('Game state is PLAYING')
        print('Resetting visited places')
        print('Now on level {} of {}'.format(game_details['levels_completed'] + 1,
                                             game_details['total_levels']))
        print('This maze has size {}'.format(game_details['maze_size']))
        print('Current location: {}'.format(game_details['current_location']))
        rep = create_maze(game_details['maze_size'])
        The_maze = Maze(rep)
        print('Starting challenge...')
        if solve_maze(None, The_maze) == True: # solves challenge
            solve_challenge()
    elif game_details['status'] == 'NONE':
        print('Game session expired or does not exist')
    else: # 'GAME_OVER'
        print('Game over')

# returns whether you can get to the end of the maze from current location
def solve_maze(prev_dir, maze):
    # print the maze representation
    print_rep_as_string(maze.representation)
    # if you have already visited current location, backtrack & return false
    location = get_game_details()['current_location']
    if location in maze.path:
        try_move(opposite_direction[prev_dir])
        return False
    # mark location as visited
    maze.path.append(location)
    # update the maze representation
    x, y = location
    maze.representation[y][x] = 'o' # o for on the path
    for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        # don't go back the way you came just yet                
        if prev_dir != None and direction == opposite_direction[prev_dir]:
            continue;
        # check to see if moving in the direction would be bad
        dx, dy = direction_to_deltas[direction]
        if (x + dx < 0 or x + dx > len(maze.representation[0]) - 1
            or y + dy < 0 or y + dy > len(maze.representation) - 1
            or maze.representation[y + dy][x + dx] == '*' # wall
            or maze.representation[y + dy][x + dx] == 'd'): # dead end
            continue
        try_move_result = try_move(direction).json()['result']
        if try_move_result == 'END':
            print('Reached the end of the maze!')
            return True
        elif try_move_result == 'SUCCESS':
            if solve_maze(direction, maze) == True:
                return True
        else: # hit a wall
            # store a * into the wall's position
            maze.representation[y + dy][x + dx] = '*'
            continue
    maze.path.remove(location)
    maze.representation[y][x] = 'd'
    # d for dead end; all paths from here will never go anywhere
    print_rep_as_string(maze.representation)
    try_move(opposite_direction[prev_dir])
    return False

# returns the initial 2D rep of the maze using the dimensions from the details
# for example, if dimensions is [3, 2], then the return value would be
# [['.', '.'], ['.', '.'], ['.', '.']]
def create_maze(dimensions):
    rep = []
    width, height = dimensions
    for h in range(height):
        row = []
        for w in range(width):
            row.append('.')
        rep.append(row)
    return rep

# prints the representation object line by line
def print_rep_as_string(rep):
    print("Maze:")
    for row in rep:
        print(''.join(row))

# attempts to move in the direction specified and returns the object returned
# by requests
def try_move(direction):
    return requests.post(url_to_move_in_maze, {'action': direction})

def get_game_details():
    return requests.get(maze_state_url).json()

def main():
    solve_challenge()

if __name__ == '__main__':
    main()
