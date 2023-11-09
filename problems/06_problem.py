"""
Problem 6
You've decided to deploy one million lights in a 1000x1000 grid, 0 indexed.

* The instructions include whether to turn on, turn off, or toggle various _inclusive_ ranges given as coordinate pairs.
* Each coordinate pair represents opposite corners of a rectangle, inclusive;
    * a coordinate pair like 0,0 through 2,2 therefore refers to 9 lights in a 3x3 square.
* The lights all start turned off.
"""

import numpy as np

# Part 1: After following the instructions, how many lights are lit?

# First, we need to be able to parse the input to extract the direction and the pair of coordinates
def parse_coord(coord_string):
    x, y = coord_string.split(',')
    return int(x), int(y)


def parse_direction(line):
    if 'off' in line:
        action = 'off'
    elif 'on' in line:
        action = 'on'
    else:
        action = 'toggle'

    split_on_space = line.split(' ')
    corner_1 = parse_coord(split_on_space[-3])
    corner_2 = parse_coord(split_on_space[-1])

    return [action, corner_1, corner_2]

raw_directions = open('06_input.txt', 'r').readlines()
directions = [parse_direction(line) for line in raw_directions]

# Option 1: Build a grid and fill it in with ones and zeros
# Option 2: Save all the coordiantes that are "on" and then just find the length when done.
# Let's start with Option 2... Note coordinates seem to be given as upper left to lower right.

def generation_rectangle_coords(corner_1, corner_2):
    x1, y1 = corner_1
    x2, y2 = corner_2
    coords = []
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            coords.append((x, y))
    return set(coords)


# Follow directions:
lights_on = set()
for d in directions:
    action = d[0]
    coords_impacted = generation_rectangle_coords(d[1], d[2])
    if action == 'on':
        lights_on.update(coords_impacted)
    elif action == 'off':
        lights_on = lights_on.copy() - coords_impacted
    else:
        to_turn_off = lights_on.intersection(coords_impacted)
        lights_on = lights_on.copy() - to_turn_off
        to_turn_on = coords_impacted - to_turn_off
        lights_on.update(to_turn_on)

print(f"At the end of the directions, there are {len(lights_on)} lights on.")

"""
Part 2:
The phrase turn on actually means that you should increase the brightness of those lights by 1.
The phrase turn off actually means that you should decrease the brightness of those lights by 1, to a minimum of zero.
The phrase toggle actually means that you should increase the brightness of those lights by 2.

What is the total brightness of all lights combined after following Santa's instructions?
"""

# Meh. Kind of have to start over.
lights = np.zeros((1000, 1000))
for d in directions:
    action = d[0]
    x1, y1 = d[1]
    x2, y2 = d[2]
    if action == 'on':
        lights[x1:(x2+1), y1:(y2+1)] += 1
    elif action == 'toggle':
        lights[x1:(x2+1), y1:(y2+1)] += 2
    else:
        lights[x1:(x2+1), y1:(y2+1)] -= 1
        lights[lights < 0] = 0

print(f"Total brightness = {lights.sum()}")
