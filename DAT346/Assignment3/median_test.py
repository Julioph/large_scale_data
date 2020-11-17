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
        yield round(numbers, 3), 1

    def combiner(self, number, count):
        yield number, sum(count)


    def reducer(self, number, count):
        yield number, sum(count)


    def reducer2(self, _, num_freq_pairs):
        n = sum(item[1] for item in num_freq_pairs)

        if n % 2 != 0: # is odd
            median_pos = n / 2
        yield "Freq sum", median_pos


if __name__ == '__main__':
    Median.run()