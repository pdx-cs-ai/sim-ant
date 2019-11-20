#!/usr/bin/python3

from collections import defaultdict
import random

from maze import Maze

dmaze = 21

pfood = (dmaze - 1, dmaze - 1)

maze = Maze(dmaze)

pheromones = defaultdict(lambda: 0)

class Ant(object):
    def __init__(self, loc):
        self.loc = loc
        self.carrying = False

ants = [Ant((1, 1)) for _ in range(10)]

def count_pheromones():
    t = 0
    for r in range(dmaze):
        for c in range(dmaze):
            t += pheromones[(r, c)]
    return t

def find_ants():
    result = set()
    for a in ants:
        result.add(a.loc)
    return result

def render():
    pcs = count_pheromones()
    als = find_ants()
    for r in range(dmaze):
        for c in range(dmaze):
            p = (r, c)
            if p in als:
                print("@", end="")
                continue
            if pheromones[p] > 0:
                ds = list("123456789")
                ph = pheromones[p] // pcs
                if ph > 1:
                    print(ds[min(ph - 1, 8)], end="")
                    continue
            print(maze[p], end="")
        print()

render()
