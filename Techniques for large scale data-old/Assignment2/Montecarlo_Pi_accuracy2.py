import multiprocessing
import random
import time
import numpy as np
from math import pi as PI
import argparse
import matplotlib.pyplot as plt


def accuracy_pi(estimate):
    error = abs(PI - estimate)
    # percent_error = error/PI
    return error


def worker(queue, batch_size, id):
    # Run forever until accuracy level is reached --> accuracy is checked somewhere else
    random.seed(id)
    while True:
        s = sample_pi(batch_size, id)
        queue.put(s)
        # time.sleep(0.05)
        #print(f"Worker iterations: {i}")


def sample_pi(batch_size, id):
    s = 0
    for i in range(int(batch_size)):
        x = random.random()
        y = random.random()

        if x ** 2 + y ** 2 <= 1.0:
            s += 1

    #print(f"Worker {id} = put {s}")
    return s


def compute_pi(accuracy, workers):
    start = time.time()
    batch_size = 100000

    qout = multiprocessing.Queue()

    processes = list()
    for w in range(workers):
        processes.append(multiprocessing.Process(target=worker, args=(qout, batch_size, w)))

    for p in processes:
        p.start()

    estimate = 0.0
    suma = 0.0
    iter_n = 0
    total_n = 0
    while accuracy_pi(estimate) > accuracy:
        iter_n += 1
        suma += qout.get()
        total_n += batch_size
        estimate = 4 * suma / total_n


    for process in processes:
        process.terminate()
        process.join()

    end = time.time()

    print(f"Done in {round(end - start, 2)} seconds and {iter_n} iterations")
    print(f"ESTIMATE: {estimate} | ERROR: {abs(PI-estimate)}")
    return end - start


def montecarlo_pi(accuracy, workers):
    print(workers, accuracy)
    measured_speedup = list()
    theoretical_speedup = list()
    cores = workers
    for i in cores:
        print(f"=========== Computing with {i} cores ============")
        pi_time = compute_pi(accuracy, i)
        if i==1:
            normal_time = pi_time

        measured_speedup.append(normal_time / pi_time)
        theoretical_speedup.append(i)

    plt.plot(cores, measured_speedup, 'bo-', label="Measured")
    plt.plot(cores, theoretical_speedup, label="Theoretical")
    plt.title("Speed-up, measured vs theorical")
    plt.legend()
    # plt.savefig("SpeedUp.png")
    plt.show()
    # fig = go.Figure()
    # fig.add_trace(
    #     go.Scatter(x=list(range(len(workers)+1)), y=measured_speedup, name="Measured Speedup")
    # )
    # fig.add_trace(
    #     go.Scatter(x=list(range(len(workers)+1)), y=theoretical_speedup, name="Theoretical Speedup")
    # )
    #
    # fig.show()
    # fig.write_image("figureee.png")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workers", default=1, nargs = '+', type=int)
    parser.add_argument("-a", "--accuracy", default=0.001, type=float)
    args = parser.parse_args()
    montecarlo_pi(args.accuracy, args.workers)
    print("<Script end>")
    # compute_pi(args.accuracy, args.workers)
