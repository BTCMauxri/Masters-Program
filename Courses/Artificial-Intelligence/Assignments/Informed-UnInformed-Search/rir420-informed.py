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
def read_maze(file):
    