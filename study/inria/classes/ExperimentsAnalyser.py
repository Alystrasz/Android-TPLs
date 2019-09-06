from Experiment import Experiment

class ExperimentsAnalyser:
    def __init__(self, name, count):
        self.name = name
        self.experiments = []
        self.count = count
        self.load_experiments()

    def load_experiments(self):
        for i in range(self.count):
            self.experiments.append(Experiment(self.name, "results/%s-%d.csv" % (self.name, i), "blue"))

    def get_mean_data(self):
        mean = 0

        for exp in self.experiments:
            selfmean = 0
            for point in exp.power:
                selfmean += float(point)
            mean += (selfmean/len(exp.power))

        return float(mean)/self.count

    def get_markers(self):
        max = 0
        min = 500
        for exp in self.experiments:
            for point in exp.power:
                if point < min: min = point
                if point > max: max = point
        return {"min": min, "max": max}

    def print_results(self):
        print("Library tested: %s" % self.name)
        print("Number of runs: %d" % self.count)
        print("Average power withdrawn: %fW" % self.get_mean_data())
        markers = self.get_markers()
        print("Min value: %fW, max value: %fW" % (markers['min'], markers['max']))
        print("------------------------------------------------")
