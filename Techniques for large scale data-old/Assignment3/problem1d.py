import sys
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

    def configure_args(self):
        super(MRSummaryStatistics, self).configure_args()
        self.add_passthru_arg('--group', '-g', type=int,
                              help="restrict the analysis to records for which <group> is specified ")

    def mapper_init(self):
        self.group = int(self.options.group)

    def mapper(self, _, line):
        data = line.split("\t")
        num = float(data[2])
        group = int(data[1])
        if group == self.group:
            yield group, (num, num ** 2)

    def combiner(self, key, some_values):
        suma = 0
        suma_sq = 0
        count = 0
        minim = np.inf
        maxim = -np.inf
        all_vals = list()
        for pair in some_values:
            all_vals.append(pair[0])
            count += 1
            if pair[0] < minim:
                minim = pair[0]
            if pair[0] > maxim:
                maxim = pair[0]

            suma += pair[0]
            suma_sq += pair[1]

        yield None, (suma, suma_sq, count, minim, maxim, all_vals)

    def reducer(self, key, values):
        count = 0
        suma = 0
        suma_sq = 0
        val_list = list()
        all_values_list = list()
        for val in values:
            suma += val[0]
            suma_sq += val[1]
            count += val[2]
            val_list.append(val[3])
            val_list.append(val[4])
            all_values_list.extend(val[5])

        mean = suma / count
        std_dev = np.sqrt(suma_sq / count - (mean ** 2))
        minim = min(val_list)
        maxim = max(val_list)

        stats = {"mean": round(mean, 4),
                 "std dev": round(std_dev, 4),
                 "min": minim,
                 "max": maxim,
                 }

        yield "Statistics summary:", stats


if __name__ == '__main__':
    start = time()
    MRSummaryStatistics.run()
    end = time()
    sys.stderr.write(f"Exec time: {end - start}")
