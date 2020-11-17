from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np
from time import time
import sys


class MRSummaryStatistics(MRJob):

    # def steps(self):
    #     return[
    #     MRStep(mapper = self.mapper,
    #            reducer = self.reducer),
    #     MRStep(reducer = self.reducer_all)]

    def mapper(self, _, line):
        idd, group, number = line.split("\t")
        num = float(number)
        yield "Test", (num, num**2)

    def reducer(self, key, num_numsq):
        count = 0
        suma = 0
        suma_sq = 0
        minim = 1e10000
        maxim = -1e10000
        hist_array = list()
        for num_pairs in num_numsq:
            count += 1
            hist_array.append(num_pairs[0])
            if num_pairs[0] < minim:
                minim = num_pairs[0]
            if num_pairs[0] > maxim:
                maxim = num_pairs[0]

            suma += num_pairs[0]
            suma_sq += num_pairs[1]

        mean = suma / count
        std_dev = np.sqrt(suma_sq/count - (mean ** 2))

        stats = {"mean": round(mean,4),
                "std dev": round(std_dev,4),
                "min": minim,
                "max": maxim,
                "histogram counts": np.histogram(a=hist_array, bins=10)[0].tolist()
                 }

        yield "Statistics", stats


if __name__ == '__main__':
    start = time()
    MRSummaryStatistics.run()
    end = time()
    sys.stderr.write(f"Exec time: {end-start}")