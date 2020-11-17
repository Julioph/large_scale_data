import mp_pi_montecarlo_pool
import argparse
import matplotlib.pyplot as plt
import time
import os
import sys

def compute_pi_time(steps, workers):
    start = time.time()
    mp_pi_montecarlo_pool.compute_pi(steps, workers)
    end = time.time()
    return end - start


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', '-w',
                        default='1',
                        type=int,
                        nargs='+',
                        help='list of cores to try (2 threads per core)')
    parser.add_argument('--steps', '-s',
                        default='1000',
                        type = int,
                        help='Number of steps in the Monte Carlo simulation')
    args = parser.parse_args()

    steps = args.steps
    workers = args.workers

    one_core_time = compute_pi_time(steps, 2) # 2 threads = 1 core
    measured_speedup = list()
    theoretical_speedup = list()

    for k in workers:
        print(f"--- cores: {2*k} --- ")
        t = compute_pi_time(steps, 2*k)
        print(f"t: {t}")
        measured_speedup.append(one_core_time/t)
        theoretical_speedup.append(k)


    print(f"Theoretical speed up = {theoretical_speedup}")
    print(f"Measured speed up = {measured_speedup}")

    plt.plot(measured_speedup)
    plt.plot(theoretical_speedup)

    plt.title("Theoretical vs Measured speed up")
    plt.xticks(ticks=range(len(workers)), labels=workers)
    plt.legend(["Measured speedup", "Theoretical speedup"])

    pathname = os.path.dirname(sys.argv[0])
    plt.savefig(fname = os.path.abspath(pathname)+"/Graph")

    # plt.show()