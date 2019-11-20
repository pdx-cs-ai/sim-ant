import random

# An n-by-n maze. n must be odd and greater than 3. Cells
# with value '.' are paths. Cells with value '#' are
# walls. The maze will have no entrance or exit (the
# exterior will be all walls).  The maze will be a tree on
# the odd cells.  Uses a spanning tree algorithm adapted for
# the maze structure.
class Maze(object):
    
    def __init__(self, n, punctuated=0):
        assert n >= 4 and n % 2 == 1
        maze = dict()

        # Make walls.
        for r in range(0, n):
            for c in range(0, n, 2):
                maze[(r, c)] = '#'
        for r in range(0, n, 2):
            for c in range(0, n):
                maze[(r, c)] = '#'

        q = [(1, 1)]
        while q:
            i = random.randrange(len(q))
            r, c = q[i]
            del q[i]
            if maze.get((r, c)) != None:
                continue
            maze[(r, c)] = '.'
            neighbors = []
            for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                rw, cw = r + 2 * dr, c + 2 * dc
                if rw < 0 or rw > n - 1 or cw < 0 or cw > n - 1:
                    continue
                if maze.get((rw, cw)) == None:
                    q.append((rw, cw))
                else:
                    neighbors.append((dr, dc))
            nn = len(neighbors)
            if nn == 0:
                continue
            i = random.randrange(nn)
            dr, dc = neighbors[i]
            maze[(r + dr, c + dc)] = '.'

        self.n = n
        self.maze = maze

    # Index the maze.
    def __getitem__(self, p):
        return self.maze[p]

    # Render a maze
    def __str__(self):
        result = ''
        for r in range(self.n):
            for c in range(self.n):
                s = self.maze.get((r, c))
                if s == None:
                    result += '?'
                else:
                    result += s
            result += '\n'
        return result

