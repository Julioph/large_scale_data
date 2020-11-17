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
import os

def generateData(n, c):
    logging.info(f"Generating {n} samples in {c} classes")
    X, y = make_blobs(n_samples=n, centers=c, cluster_std=1.7, shuffle=False,
                      random_state=2122)
    return X


def nearestCentroid(data_chunk, centroids):
    logging.debug(f"Process {os.getpid()} GOT {len(data_chunk)} POINTS OF DATA ")
    assignments = list()
    for datum in data_chunk:
        dist = np.linalg.norm(centroids - datum, axis=1)
        assignments.append((np.argmin(dist), np.min(dist)))
    return assignments


def kmeans(k, data, workers, nr_iter=100):
    N = len(data)
    # Choose k random data points as centroids
    centroids = data[np.random.choice(np.array(range(N)), size=k, replace=False)]
    logging.debug("Initial centroids\n", centroids)

    # The cluster index: c[i] = j indicates that i-th datum is in j-th cluster
    c = np.zeros(N, dtype=int)

    logging.info("Iteration\t Variation\t Delta Variation")
    total_variation = 0.0


    for j in range(nr_iter):
        estar = time.time()
        logging.debug("=== Iteration %d ===" % (j+1))


        pool = multiprocessing.Pool(processes=workers)
        y = time.time()
        process_objects = [pool.apply(nearestCentroid, args=(data_chunk, centroids)) \
                           for data_chunk in np.array_split(data, workers)]
        z = time.time()
        logging.warning(f"Procesing:  {z-y}")

        a = time.time()
        pool.close()
        pool.join()
        b = time.time()
        logging.warning(f"pool closing time: {b-a}")

        # list_of_lists = [p.get() for p in process_objects]

        list_of_lists = process_objects

        flat_list = [item for sublist in list_of_lists for item in sublist]

        # Assign data points to nearest centroid
        variation = np.zeros(k)
        cluster_sizes = np.zeros(k, dtype=int)

        for i in range(N):
            cluster = flat_list[i][0]
            c[i] = cluster
            dist = flat_list[i][1]
            cluster_sizes[cluster] += 1
            variation[cluster] += dist**2
        delta_variation = -total_variation
        total_variation = sum(variation)
        delta_variation += total_variation
        logging.info("%3d\t\t%f\t%f" % (j, total_variation, delta_variation))

        # Recompute centroids
        centroids = np.zeros((k,2)) # This fixes the dimension to 2
        for i in range(N):
            centroids[c[i]] += data[i]
        centroids = centroids / cluster_sizes.reshape(-1,1)

        endu = time.time()
        logging.warning(f"Took {endu-estar} seconds to do iteration")

        logging.debug(cluster_sizes)
        logging.debug(c)
        logging.debug(centroids)

    return total_variation, c


def computeClustering(args):
    if args.verbose:
        logging.basicConfig(format='# %(message)s',level=logging.INFO)
    if args.debug:
        logging.basicConfig(format='# %(message)s',level=logging.DEBUG)
    if args.warning:
        logging.basicConfig(format='# %(message)s',level=logging.WARNING)


    X = generateData(args.samples, args.classes)

    start_time = time.time()
    #
    # Modify kmeans code to use args.worker parallel threads
    total_variation, assignment = kmeans(args.k_clusters, X, workers=args.workers , nr_iter=args.iterations)
    #
    #
    end_time = time.time()
    logging.info("Clustering complete in %3.2f [s]" % (end_time - start_time))
    print(f"Total variation {total_variation}")

    if args.plot: # Assuming 2D data
        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.scatter(X[:, 0], X[:, 1], c=assignment, alpha=0.2)
        plt.title("k-means result")
        #plt.show()
        fig.savefig(args.plot)
        plt.close(fig)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Compute a k-means clustering.',
        epilog = 'Example: kmeans.py -v -k 3 --samples 10000 --classes 3 --plot result.png'
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
    parser.add_argument('--warning', '-x',
                        action='store_true',
                        help='Print debugging output')
    args = parser.parse_args()
    computeClustering(args)
