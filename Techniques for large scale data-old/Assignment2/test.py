import numpy as np


def worker(seed):
    np.random.seed(seed)
    workerResult = []
    for i in range(5):
        workerResult.append(np.random.random())

    return workerResult


allWorkers = [1, 2, 4, 8]
allResults = []

for w in allWorkers:
    print(w)
    print(worker(w))
