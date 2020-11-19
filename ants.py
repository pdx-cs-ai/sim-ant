#!/usr/bin/python3
# Ant Colony optimization for pathfinding.
# Bart Massey

from collections import defaultdict
import random
import time

from maze import Maze

# Size of the (square) maze in characters.
# XXX Note that some of the tuning parameters should be a
# function of maze size.
dmaze = 11

# Number of steps per second.
frame_rate = 10

# Nest is at lower-right corner.
pnest = (1, 1)

# Food is at lower-right corner.
pfood = (dmaze - 2, dmaze - 2)
assert pnest != pfood

# Fraction of pheromone decay per step.
ph_decay = 0.05

# Fraction of food-carried pheromone decay per step.
# This causes an ant to emit less pheromone as it
# wanders around with food being lost.
carry_decay = 0.001

# Scoring bias for moving forward, left, back, right.
bumps = [50, 30, 1, 30]
for b in bumps:
    assert b > 0

# The maze.
maze = Maze(dmaze)

# Amount of food delivered.
ndelivered = 0

# The pheromone value for maze cells.
pheromones = defaultdict(float)

# Ordering of move directions is W, N, S, E.
directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

# Ant with location, facing, behavior.
class Ant(object):
    def __init__(self, loc):
        self.loc = loc
        self.carrying = False
        self.facing = random.randrange(4)
        self.ph = 0

    # Move the ant one step.
    def move(self):
        global ndelivered

        # Next location and facing according to ant's facing.
        def rel_loc(d):
            r, c = self.loc
            rel = (self.facing - d + 4) % 4
            dr, dc = directions[d]
            return rel, (r + dr, c + dc)

        # Weighted random selection from a collection
        # of scores.
        def select(scores):
            tscore = sum(scores)
            assert tscore > 0
            scores = [s / tscore for s in scores]
            spin = random.random()
            for i in range(len(scores) - 1):
                if scores[i] >= spin:
                    return i
                spin -= scores[i]
            return len(scores) - 1

        # Heuristically decide which way the ant should move
        # next. Start by computing the heuristic value of
        # moving in each direction.
        scores = [0] * 4
        new_locs = [None] * 4
        stuck = True
        for d in range(4):
            rel, p = rel_loc(d)
            if maze[p] == '.':
                scores[d] = pheromones[p] + bumps[rel]
                new_locs[d] = p
                stuck = False
        assert not stuck
        direction = select(scores)
        new_loc = new_locs[direction]
        new_facing = direction

        # Perform the move.
        if self.carrying:
            pheromones[self.loc] += self.ph
            self.ph = self.ph * (1 - carry_decay)
        if new_loc == pnest:
            # Drop the food.
            if self.carrying:
                ndelivered += 1
            self.carrying = False
            self.ph = 0
        if new_loc == pfood:
            # Pick up the food.
            self.carrying = True
            self.ph = 1
        self.loc = new_loc
        self.facing = new_facing

ants = [Ant(pnest) for _ in range(10)]

def adjust_pheromones():
    for r in range(dmaze):
        for c in range(dmaze):
            p = (r, c)
            ph = pheromones[p]
            pheromones[p] = (1 - ph_decay) * pheromones[p]

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
            if p == pnest:
                print("O", end="")
                continue
            if p == pfood:
                print("*", end="")
                continue
            if p in als:
                print(als[p], end="")
                continue
            ph = pheromones[p]
            if ph > 0.05:
                ds = list("0123456789")
                print(ds[min(len(ds) - 1, max(0, int(ph / 0.1)))], end="")
                continue
            print(maze[p], end="")
        print()
    print(ndelivered)

render()
for _ in range(500):
    time.sleep(1.0 / frame_rate)
    for a in ants:
        a.move()
    adjust_pheromones()
    render()
