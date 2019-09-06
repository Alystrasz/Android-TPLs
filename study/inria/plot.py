# coding=utf-8
import plotly.graph_objects as go
import numpy as np
import csv
import scipy
from scipy import signal


class Experiment:
    def __init__(self, name, csv_path, color):
        self.name = name
        self.csv_path = csv_path
        self.time = []
        self.power = []
        self.color = color
        self.loadData()

    def loadData(self):
        with open(self.csv_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(reader, None)  # skip the headers

            for row in reader:
                # time (sec)  |  Intensity (mA)  |  Voltage (V)
                self.power.append(float(row[1])/1000 * float(row[2]))       # P(W) = I(A) * T(V)
                self.time.append(float(row[0]))

class Graph:
    def __init__(self, title):
        self.experiments = []
        self.title = title
        self.fig = go.Figure()

    def addExperiment(self, experiment):
        self.experiments.append(experiment)

    def plotExperiments(self):
        for exp in self.experiments:
            self.fig.add_trace(go.Scatter(x=exp.time, y=exp.power,
                                     name=exp.name,
                                     line=dict(color=exp.color, width=4),
                                     line_shape='spline'))

    def plotSmoothedExperiments(self):
        for exp in self.experiments:
            self.fig.add_trace(go.Scatter(x=exp.time,
                                          y=signal.savgol_filter(exp.power,
                                                                    23, # window size used for filtering
                                                                    3), # order of fitted polynomial,
                                          name=exp.name,
                                          line=dict(color=exp.color, width=8),
                                          line_shape='spline'))

    def show(self):
        """ adding title """
        self.fig.update_layout(title=self.title,
                               xaxis_title='Time (sec)',
                               yaxis_title='Power (Watt)')
        self.fig.show()

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


def main():
    """
    graph = Graph("Power evolution of Android libraries")

    graph.addExperiment(Experiment("Firebase", "results/firebase-release-0.csv", "firebrick"))
    graph.addExperiment(Experiment("Flurry", "results/flurry-release-0.csv", "blue"))
    graph.addExperiment(Experiment("Google", "results/google-release-0.csv", "green"))

    # graph.plotExperiments()
    graph.plotSmoothedExperiments()
    graph.show()
    """

    runs_per_scenario = 30

    firebase_analyser = ExperimentsAnalyser("firebase-release", runs_per_scenario)
    firebase_analyser.print_results()
    flurry_analyser = ExperimentsAnalyser("flurry-release", runs_per_scenario)
    flurry_analyser.print_results()
    google_analyser = ExperimentsAnalyser("google-release", runs_per_scenario)
    google_analyser.print_results()

if __name__ == "__main__":
    main()
