"""
PROBLEM 03
Each character of puzzle input directs Santa to move 1 coordinate in one direction.
"""

import numpy as np

#Part 1: How many unique coordinates does he visit?

# Plan to need to know how many houses (coordinates) he visits more than once, even though a set would work for pt 1.
raw_directions = open('03_input.txt', 'r').readlines()[0]

# First pass, collect coordinates he visits
def visit_houses(directions):
    move_map = {'v': np.array([0, -1]),
                '^': np.array([0, 1]),
                '>': np.array([1, 0]),
                '<': np.array([-1, 0])}

    current_position = np.array([0, 0])
    coordinates = current_position

    for c in directions:
        new_position = current_position + move_map[c]
        coordinates = np.vstack([coordinates, new_position])
        current_position = new_position

    return coordinates


pt_1_visits = visit_houses(raw_directions)

print(f"Santa visited {len(np.unique(pt_1_visits, axis=0))} unique houses.")

# Part 2: Santa and a robot santa work together, alternating with the directions. Now how many houses do they hit?
santa = visit_houses(raw_directions[1::2])
robo_santa = visit_houses(raw_directions[::2])

print(f"With the robot's help, {len(np.unique(np.append(santa, robo_santa, axis=0), axis=0))} houses are visited.")
