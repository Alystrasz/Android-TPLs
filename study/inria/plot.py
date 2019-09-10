# coding=utf-8
from classes.Graph import Graph
from classes.Experiment import Experiment

def main():
    graph = Graph("Power evolution of Android libraries")

    """
    graph.addExperiment(Experiment("Firebase", "results/firebase-release-0.csv", "firebrick"))
    graph.addExperiment(Experiment("Flurry", "results/flurry-release-0.csv", "blue"))
    graph.addExperiment(Experiment("Google", "results/google-release-0.csv", "green"))
    """

    graph.addExperiment(Experiment("Acra", "results/acra-release-0.csv", "firebrick"))
    graph.addExperiment(Experiment("Newrelic", "results/newrelic-release-0.csv", "blue"))
    graph.addExperiment(Experiment("Crashlytics", "results/crashlytics-release-0.csv", "green"))

    # graph.plotExperiments()
    graph.plotSmoothedExperiments()
    graph.show()

if __name__ == "__main__":
    main()
