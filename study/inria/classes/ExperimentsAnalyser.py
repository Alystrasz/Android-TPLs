from Experiment import Experiment
import math

class ExperimentsAnalyser:
    def __init__(self, name, count):
        self.name = name
        self.experiments = []
        self.count = count
        self.load_experiments()

    def load_experiments(self):
        for i in range(self.count):
            self.experiments.append(Experiment(self.name, "results/%s-%d.csv" % (self.name, i), "blue"))

    def get_mean(self):
        mean = 0

        for exp in self.experiments:
            selfmean = 0
            for point in exp.power:
                selfmean += float(point)
            mean += (selfmean/len(exp.power))

        return float(mean)/self.count

    def get_standard_deviation(self):
        deviation = 0

        for exp in self.experiments:
            mean = 0
            distance = 0

            for point in exp.power:
                mean += point
            mean = float(mean)/len(exp.power)

            for point in exp.power:
                distance += (point - mean)**2

            deviation += math.sqrt(distance/len(exp.power))

        return float(deviation)/len(self.experiments)


    def get_markers(self):
        max = 0
        min = 500
        for exp in self.experiments:
            for point in exp.power:
                if point < min: min = point
                if point > max: max = point
        return {"min": min, "max": max}

    def get_quartiles(self):
        allvalues = []
        for exp in self.experiments:
            for point in exp.power:
                allvalues.append(point)
        allvalues.sort()

        size = len(allvalues)
        median = allvalues[int(round(size/2))-1]
        i = int(round(size/4))
        firstQ = allvalues[i-1]
        thirdQ = allvalues[i*3-1]

        return {"firstQ": firstQ, "thirdQ": thirdQ, "median": median}

    def print_results(self):
        print("Library tested: %s" % self.name)
        print("Number of runs: %d" % self.count)
        print("Average power withdrawn: %fW" % self.get_mean())
        markers = self.get_markers()
        print("Min value: %fW, max value: %fW" % (markers['min'], markers['max']))
        quartiles = self.get_quartiles()
        print("1st quartile: %fW, 3rd quartile: %fW, median: %fW" % (quartiles["firstQ"], quartiles["thirdQ"], quartiles["median"]))
        print("Average standard deviation: %fW" % self.get_standard_deviation())
        print("------------------------------------------------")
