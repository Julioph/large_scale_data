import sys
from collections import defaultdict

from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np
from time import time


class MRSummaryStatistics(MRJob):

    # def steps(self):
    #     return[
    #     MRStep(mapper = self.mapper,
    #            reducer = self.reducer),
    #     MRStep(reducer = self.reducer_all)]

    # def configure_args(self):
    #     super(MRSummaryStatistics, self).configure_args()
    #     self.add_passthru_arg('--group', '-g', type=int,
    #                           help="restrict the analysis to records for which <group> is specified ")
    #
    # def mapper_init(self):
    #     self.group = int(self.options.group)

    def make_hist_counts(self, sorted_vals):
        buckets = 10
        counts = list()
        trange = sorted_vals[-1] - sorted_vals[0]
        sequence = np.linspace(sorted_vals[0]+trange/buckets, sorted_vals[-1], num=10).tolist()
        count = 0
        # low = sorted_vals[0]
        j = 0
        k = 0
        for i in range(len(sorted_vals)):
            while j < 10 and sorted_vals[k] < sequence[j]:
                sys.stderr.write(f"{k}, {j} ---> sortVal {sorted_vals[k]}, bound: {sequence[j]}\n")
                count += 1
                k += 1
            sys.stderr.write(f"NO!")
            counts.append(count)
            count = 0
            i = k
            j += 1
            if

        return counts

    def mapper(self, _, line):
        data = line.split("\t")
        num = float(data[2])
        group = int(data[1])
        # if group == self.group:
        yield None, (num, num ** 2)

    def combiner(self, nichts, some_values):
        suma = 0
        suma_sq = 0
        count = 0
        minim = np.inf
        maxim = -np.inf
        all_vals = list()

        for pair in sorted(some_values, key=lambda t: t[0]):
            # for mean
            all_vals.append(pair[0])
            count += 1
            suma += pair[0]
            # for min max
            if pair[0] < minim:
                minim = pair[0]
            if pair[0] > maxim:
                maxim = pair[0]

            # for std_dev
            suma_sq += pair[1]
        yield None, (suma, suma_sq, count, minim, maxim, all_vals)

    def reducer(self, nichts, values):
        count = 0
        suma = 0
        suma_sq = 0
        val_list = list()
        all_values_list = list()
        for_median = list()

        for val in values:
            # for median
            suma += val[0]
            count += val[2]
            # for min max
            val_list.append(val[3])
            val_list.append(val[4])
            all_values_list.extend(val[5])
            # for stddev
            suma_sq += val[1]
            # for median
            for x in val[-1]:
                for_median.append(x)

            #escribir mejor
            sorted_val = sorted(for_median)
            median_pos = count//2
            median = None

            if count % 2 != 0: #odd
                median = sorted_val[median_pos+1]
            else:
                median = (sorted_val[median_pos] + sorted_val[median_pos+1])/2

        histogram_counts = self.make_hist_counts(sorted_val)

        mean = suma / count
        std_dev = np.sqrt(suma_sq / count - (mean ** 2))
        minim = min(val_list)
        maxim = max(val_list)

        stats = {"mean": round(mean, 4),
                 "std dev": round(std_dev, 4),
                 "min": minim,
                 "max": maxim,
                 "median": median,
                 "histogram counts": histogram_counts
                 }

        yield "Statistics summary:", stats


if __name__ == '__main__':
    start = time()
    MRSummaryStatistics.run()
    end = time()
    sys.stderr.write(f"Exec time: {end - start}")
