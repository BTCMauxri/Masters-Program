"""
@User: Mauricio Villegas | RIR420
Course: CS 5233 
Assignment: Informed Search (A*)
Solution: Read from 'maze.txt', implement A*
informed search algorithm to find the optimal path from start
to goal state (bottom right to top left).
"""

import heapq

# Function to read 'maze.txt'
def read_maze(path):

    # open and read file, adds lines to a 2D array
    with open(path, 'r') as file:
        return [list(line.rstrip('\n')) for line in file.readlines()]

# function takes inthe  2D array (maze)
def get_points(maze):

    # Get the start and goal states of the maze
    rows = len(maze)
    columns = len(maze[0])

    # goal/exit = 1st space in top row of array
    goal = (0, maze[0].index(' '))

    # start last space in last row
    start = (rows - 1, "".join(maze[rows - 1]).rindex(' '))

    return start, goal

# Function takes in current and goal state to get manhattan distance
def get_manhattan_distance(current, goal):
     return abs(current[0]- goal[0]) + abs(current[1] - goal[1])

# Function returns possible nearby states
def get_adjacent_states(position, maze, rows, columns):

    row, column = position
    adj_states = []

    # moves -->:Up,    Down,    Left,   Right   
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for d_row, d_column in moves:
         new_row, new_column = row + d_row, column + d_column
         if 0 <= new_row < rows and 0 <= new_column < columns and maze[new_row][new_column] != 'O':
              adj_states.append((new_row, new_column))

    return adj_states

# Implementing the A* search Algorithm
def a_star_search(maze):

    start, goal = get_points(maze)
    rows, columns = len(maze), len(maze[0])

    # priority queue
    frontier = []
    heapq.heappush(frontier, (0, start))

    prior_state = {start: None}
    current_cost = {start: 0}

    while frontier:
        # rid lowest score
        current_priority, current_node = heapq.heappop(frontier)

        if current_node == goal:
               break

        # go through each valid adj states that are free spaces
        for state in get_adjacent_states(current_node, maze, rows, columns):
            new_cost = current_cost[current_node] + 1

            if state not in current_cost or new_cost < current_cost[state]:
                current_cost[state] = new_cost
                priority = new_cost + get_manhattan_distance(state, goal)
                heapq.heappush(frontier, (priority, state))
                prior_state[state] = current_node

    # no path to goal scenario
    if goal not in prior_state:
         return None, 0

    # Re-trace the optimal path to goal
    path = []
    current_state = goal
    while current_state != start:
         path.append(current_state)
         current_state = prior_state[current_state]
    path.append(start)

    return path, current_cost[goal]
 
def main():
    # Read maze array
    maze = read_maze("maze.txt")
    
    # Begin search
    path, final_cost = a_star_search(maze)
    
    # Output
    if path:
        # Make Optimal Path
        print("\nPath for maze.txt:\n")
        for row, col in path:
            maze[row][col] = '*'
            
        # Maze grid
        for row in maze:
            print("".join(row))
            
        # Path cost

        print(f"\nCost of optimal path: {final_cost}\n")
    else:
        print("Solution not found")

if __name__ == "__main__":
    main()
