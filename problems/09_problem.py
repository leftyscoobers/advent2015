#!/usr/bin/env python3
import sys 
from itertools import permutations
from pathlib import Path
from typing import List, Set, Tuple, Dict

# 1. Build dictionary of pairs - distance and full set of cities
def parse_pairs(lines: List[str]) -> Tuple[Dict[Tuple[str, str], int], Set[str]]:
    """
    Parse input lines into city-pairs and distance between them.
    """

    # Initiallize distance dictionary and set of cities
    pair_dict: Dict[Tuple[str, str], int] = {}
    city_set: Set[str] = set()
    
    for line in lines:
        # Sample - Faerun to Norrath = 129
        split_line = line.split()
        city1 = split_line[0]
        city2 = split_line[2]
        distance = int(split_line[-1])

        city_set.update([city1, city2])

        pair_dict[(city1, city2)] = distance
        pair_dict[(city2, city1)] = distance

    return pair_dict, city_set


# 2. Find distances for all possible paths (not that many cities)
def total_distance(dist_dict: Dict[Tuple[str, str], int], path: List[str]) -> int:
    """
    Given path, find distance - note that path might not be valid.
    """

    dist = 0 # Start with zero 

    for i in range(len(path)-1):
        dist += dist_dict[(path[i], path[i+1])]

    return dist


def get_all_distances(dist_dict: Dict[Tuple[str, str], int], cities: Set[str]) -> List[int]:
    """
    Find all permutations of city-paths, then calculate distance for each.
    """

    poss_distances: List[int] = []

    for poss_path in permutations(cities):
        dist = total_distance(dist_dict, poss_path)
        poss_distances.append(dist)

    return poss_distances


if __name__ == "__main__":
    INPUT_PATH = Path(sys.argv[1])
    raw_lines = INPUT_PATH.read_text().splitlines()

    distance_dict, cities = parse_pairs(raw_lines)
    possible_distances = get_all_distances(distance_dict, cities)

    print("Part 1 shortest distance :", min(possible_distances))
    print("Part 2 longest distance :", max(possible_distances))
