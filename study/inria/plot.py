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



def main():
    graph = Graph("Power evolution of Android libraries")

    graph.addExperiment(Experiment("Firebase", "results/firebase-release-0.csv", "firebrick"))
    graph.addExperiment(Experiment("Flurry", "results/flurry-release-0.csv", "blue"))
    graph.addExperiment(Experiment("Google", "results/google-release-0.csv", "green"))

    # graph.plotExperiments()
    graph.plotSmoothedExperiments()

    graph.show()

if __name__ == "__main__":
    main()
