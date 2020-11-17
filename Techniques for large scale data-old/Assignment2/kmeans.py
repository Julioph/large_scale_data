#!/usr/bin/env python
#
# File: kmeans.py
# Author: Alexander Schliep (alexander@schlieplab.org)
#
#
import logging
import argparse
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import time

def generateData(n, c):
    logging.info(f"Generating {n} samples in {c} classes")
    X, y = make_blobs(n_samples=n, centers = c, cluster_std=1.7, shuffle=False,
                      random_state = 2122)
    return X


def nearestCentroid(datum, centroids):
    # norm(a-b) is Euclidean distance, matrix - vector computes difference
    # for all rows of matrix
    dist = np.linalg.norm(centroids - datum, axis=1)
    return np.argmin(dist), np.min(dist)


def kmeans(k, data, nr_iter=100):
    N = len(data)
    time_to_assign = list() #yo
    time_to_update = list() #yo
    # Choose k random data points as centroids
    centroids = data[np.random.choice(np.array(range(N)), size=k, replace=False)]
    logging.debug("Initial centroids\n", centroids)

    N = len(data)

    # The cluster index: c[i] = j indicates that i-th datum is in j-th cluster
    c = np.zeros(N, dtype=int)

    logging.info("Iteration\tVariation\tDelta Variation")
    total_variation = 0.0
    for j in range(nr_iter):
        logging.debug("=== Iteration %d ===" % (j+1))

        # Assign data points to nearest centroid
        variation = np.zeros(k)
        cluster_sizes = np.zeros(k, dtype=int)

        assign_time_s=time.time()########### time to assign / yo
        for i in range(N):
            cluster, dist = nearestCentroid(data[i],centroids)
            c[i] = cluster
            cluster_sizes[cluster] += 1
            variation[cluster] += dist**2
        assign_time_e=time.time()
        time_to_assign.append(assign_time_e-assign_time_s)

        delta_variation = -total_variation
        total_variation = sum(variation)
        delta_variation += total_variation
        logging.info("%3d\t\t%f\t%f" % (j, total_variation, delta_variation))

        # Recompute centroids
        update_time_s=time.time()
        centroids = np.zeros((k,2)) # This fixes the dimension to 2
        for i in range(N):
            centroids[c[i]] += data[i]
        chetos = cluster_sizes.reshape(-1,1)
        centroids = centroids / chetos
        update_time_e=time.time()
        time_to_update.append(update_time_e-update_time_s)

        logging.debug(f"cluster sizes: \n{cluster_sizes}") #yo
        logging.debug(f"C??: \n{c}") #yo
        logging.debug(f"Centroids: \n{centroids}") #yo


    return total_variation, c, time_to_assign, time_to_update


def computeClustering(args):

    if args.verbose:
        logging.basicConfig(format='# %(message)s',level=logging.INFO)
    if args.debug:
        logging.basicConfig(format='# %(message)s',level=logging.DEBUG)


    X = generateData(args.samples, args.classes)

    start_time = time.time()
    #
    # Modify kmeans code to use args.worker parallel threads
    total_variation, assignment, time_to_assign, time_to_update = kmeans(args.k_clusters, X, nr_iter = args.iterations)
    #
    #
    end_time = time.time()

    total_time = end_time - start_time


    logging.info("Clustering complete in (TOTAL) %3.2f [s]" % (total_time))
    logging.debug(f"Total time in assignment to centroids: {sum(time_to_assign)}. --> {sum(time_to_assign)/total_time *100}% of time.") # yo
    logging.debug(f"Total time in assignment to centroids: {sum(time_to_update)}. --> {sum(time_to_update)/total_time *100}% of time.") # yo
    print(f"Total variation {total_variation}\n\n")

    if args.plot: # Assuming 2D data
        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.scatter(X[:, 0], X[:, 1], c=assignment, alpha=0.2)
        plt.title("k-means result")
        #plt.show()
        fig.savefig(args.plot)
        plt.close(fig)

if __name__ == "__main__":
    start_overall = time.time()
    parser = argparse.ArgumentParser(
        description='Compute a k-means clustering.',
        epilog = 'Example: kmeans.py -v -k 4 --samples 10000 --classes 4 --plot result.png'
    )
    parser.add_argument('--workers', '-w',
                        default='1',
                        type = int,
                        help='Number of parallel processes to use (NOT IMPLEMENTED)')
    parser.add_argument('--k_clusters', '-k',
                        default='3',
                        type = int,
                        help='Number of clusters')
    parser.add_argument('--iterations', '-i',
                        default='100',
                        type = int,
                        help='Number of iterations in k-means')
    parser.add_argument('--samples', '-s',
                        default='10000',
                        type = int,
                        help='Number of samples to generate as input')
    parser.add_argument('--classes', '-c',
                        default='3',
                        type = int,
                        help='Number of classes to generate samples from')
    parser.add_argument('--plot', '-p',
                        type = str,
                        help='Filename to plot the final result')
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='Print verbose diagnostic output')
    parser.add_argument('--debug', '-d',
                        action='store_true',
                        help='Print debugging output')
    args = parser.parse_args()
    computeClustering(args)
    end_overall = time.time()
    overall_time = end_overall - start_overall
    print("Program complete in (TOTAL) %3.2f [s]" % (overall_time))
