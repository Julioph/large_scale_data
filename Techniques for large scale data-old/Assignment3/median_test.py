from mrjob.job import MRJob
from mrjob.step import MRStep


class Median(MRJob):

    def steps(self):
        return[
            MRStep(mapper = self.mapper,
                   combiner = self.combiner,
                   reducer = self.reducer,
                   ),
            MRStep(reducer = self.reducer2)
        ]

    def mapper(self, _, line):
        data = line.split("\t")
        numbers = float(data[2])
        yield numbers, 1

    def combiner(self, number, count):
        yield number, sum(count)


    def reducer(self, number, count):
        yield None, (number, sum(count))


    def reducer2(self, _, num_freq_pairs):
        n = [i for i in num_freq_pairs]
        a = sum(it[1] for it in n)
        median_freq = a//2
        freq_sum = 0
        index = 0
        while freq_sum < median_freq:
            freq_sum += n[index][1]
            index += 1

        if a % 2 != 0:
            median = n[index+1]
        else:
            median = (n[index][0] + n[index+1][0])/2

        yield "Freq sum", (freq_sum, index, n[index], n[index+1], a//2, len(n), median)


if __name__ == '__main__':
    Median.run()