#!/usr/bin/python3

from collections import defaultdict
import random
import time

from maze import Maze

dmaze = 11

frame_rate = 10

pfood = (dmaze - 1, dmaze - 1)

maze = Maze(dmaze)

pheromones = defaultdict(lambda: 0)

ph_decay = 0.99

carry_decay = 1.0

directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

class Ant(object):
    def __init__(self, loc):
        self.loc = loc
        self.carrying = False
        self.facing = random.randrange(4)
        self.ph = 0

    def move(self):

        def rel_loc(d0):
            r, c = self.loc
            d = (d0 + self.facing) % 4
            dr, dc = directions[d]
            return (r + dr, c + dc)

        scores = [0] * 4
        bumps = [30, 10, 0, 10]
        for d in range(4):
            p = rel_loc(d)
            m = maze[p]
            if m == '.':
                scores[d] = 10 + pheromones[p] + bumps[d]
        
        i = random.randrange(int(sum(scores)))
        for d in range(4):
            if i < scores[d]:
                pheromones[self.loc] += self.ph
                self.ph = self.ph * carry_decay
                new_loc = rel_loc(d)
                new_facing = (self.facing + d) % 4
                if new_loc == (1, 1):
                    self.carrying = False
                    self.ph = 0
                if new_loc == (dmaze-2, dmaze-2):
                    self.carrying = True
                    self.ph = 20
                self.loc = new_loc
                self.facing = new_facing
                return
            i -= scores[d]
        assert False

ants = [Ant((1, 1)) for _ in range(10)]

def adjust_pheromones():
    m = 0
    for r in range(dmaze):
        for c in range(dmaze):
            m = max(m, pheromones[(r, c)])
    if m == 0:
        return

    for r in range(dmaze):
        for c in range(dmaze):
            ph = pheromones[(r, c)]
            ph = ph_decay * 10 * ph / m
            pheromones[(r,c)] = ph

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
    als = find_ants()
    for r in range(dmaze):
        for c in range(dmaze):
            p = (r, c)
            if p in als:
                print(als[p], end="")
                continue
            if pheromones[p] > 0:
                ds = list(".123456789")
                ph = pheromones[p]
                if ph > 1:
                    print(ds[min(int(ph), 9)], end="")
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
    time.sleep(1.0 / frame_rate)
    for a in ants:
        a.move()
    adjust_pheromones()
    render()
