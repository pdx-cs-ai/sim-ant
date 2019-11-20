#!/usr/bin/python3

from collections import defaultdict
import random
import time

from maze import Maze

dmaze = 21

pfood = (dmaze - 1, dmaze - 1)

maze = Maze(dmaze)

pheromones = defaultdict(lambda: 0)

directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

def rotate_left(a, n):
    s = 4 - n
    return a[s:] + a[:s]

class Ant(object):
    def __init__(self, loc):
        self.loc = loc
        self.carrying = False
        self.facing = random.randrange(4)

    def move(self):

        def rel_loc(d0):
            r, c = self.loc
            d = (d0 + self.facing) % 4
            dr, dc = directions[d]
            return (r + dr, c + dc)

        scores = [0] * 4
        for d in range(4):
            p = rel_loc(d)
            m = maze[p]
            if m == '.':
                scores[d] = 1
        
        scores[0] *= 8
        scores[1] *= 5
        scores[3] *= 5

        i = random.randrange(sum(scores))
        for d in range(4):
            if i < scores[d]:
                if self.carrying:
                    pheromones[self.loc] += 1
                new_loc = rel_loc(d)
                new_facing = (self.facing + d) % 4
                if new_loc == (1, 1):
                    self.carrying = False
                if new_loc == (dmaze-2, dmaze-2):
                    self.carrying = True
                self.loc = new_loc
                self.facing = new_facing
                return
            i -= scores[d]
        assert False

ants = [Ant((1, 1)) for _ in range(10)]

def count_pheromones():
    t = 0
    for r in range(dmaze):
        for c in range(dmaze):
            t += pheromones[(r, c)]
    return t

def find_ants():
    result = dict()
    for a in ants:
        p = a.loc
        c = a.carrying
        if p in result:
            c = c or (result[p] == '*')
        if c:
            result[p] = '*'
        else:
            result[p] = '@'
    return result

def clear_screen():
    print("\033[H\033[J", end="")

def render():
    clear_screen()
    pcs = count_pheromones()
    als = find_ants()
    for r in range(dmaze):
        for c in range(dmaze):
            p = (r, c)
            if p in als:
                print(als[p], end="")
                continue
            if pheromones[p] > 0:
                ds = list("123456789")
                ph = pheromones[p] // pcs
                if ph > 1:
                    print(ds[min(ph - 1, 8)], end="")
                    continue
            if p == (1, 1):
                print("O", end="")
                continue
            if p == (dmaze-2, dmaze-2):
                print("*", end="")
                continue
            print(maze[p], end="")
        print()

render()
for _ in range(500):
    time.sleep(0.05)
    for a in ants:
        a.move()
    render()
