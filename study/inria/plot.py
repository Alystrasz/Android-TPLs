# coding=utf-8
import numpy as np
import scipy
from classes.Graph import Graph
from classes.Experiment import Experiment
from classes.ExperimentsAnalyser import ExperimentsAnalyser

def main():
    graph = Graph("Power evolution of Android libraries")

    graph.addExperiment(Experiment("Firebase", "results/firebase-release-0.csv", "firebrick"))
    graph.addExperiment(Experiment("Flurry", "results/flurry-release-0.csv", "blue"))
    graph.addExperiment(Experiment("Google", "results/google-release-0.csv", "green"))

    # graph.plotExperiments()
    graph.plotSmoothedExperiments()
    graph.show()

    runs_per_scenario = 30

    firebase_analyser = ExperimentsAnalyser("firebase-release", runs_per_scenario)
    firebase_analyser.print_results()
    flurry_analyser = ExperimentsAnalyser("flurry-release", runs_per_scenario)
    flurry_analyser.print_results()
    google_analyser = ExperimentsAnalyser("google-release", runs_per_scenario)
    google_analyser.print_results()

if __name__ == "__main__":
    main()
