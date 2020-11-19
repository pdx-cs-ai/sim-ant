import random

# Weighted random selection from a collection
# of scores.
def select(scores):
    scores = [s / sum(scores) for s in scores]
    spin = random.random()
    for i in range(len(scores) - 1):
        if scores[i] >= spin:
            return i
        spin -= scores[i]
    return len(scores) - 1

def stats(scores, trials=1000):
    tscore = sum(scores)
    sprobs = [s / tscore for s in scores]

    counts = [0] * len(scores)
    for _ in range(trials):
        counts[select(scores)] += 1
    tcount = sum(counts)
    cprobs = [c / tcount for c in counts]

    print(scores)
    for i in range(len(scores)):
        print(f"{sprobs[i]:.3} {cprobs[i]:.3}")

stats([1, 1, 1, 1])
stats([0.9, 0, 0.9, 0])
stats([0, 0.5, 0, 1.0])
