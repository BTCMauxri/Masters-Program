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



def main():

    # clarify maze.txt file path
    maze = read_maze("maze.txt")

    

if __name__ == "__main__":
        main()
