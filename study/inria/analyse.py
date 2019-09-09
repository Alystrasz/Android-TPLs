# coding=utf-8
from classes.ExperimentsAnalyser import ExperimentsAnalyser

def main():
    runs_per_scenario = 30

    firebase_analyser = ExperimentsAnalyser("firebase-release", runs_per_scenario)
    firebase_analyser.print_results()
    flurry_analyser = ExperimentsAnalyser("flurry-release", runs_per_scenario)
    flurry_analyser.print_results()
    google_analyser = ExperimentsAnalyser("google-release", runs_per_scenario)
    google_analyser.print_results()

if __name__ == "__main__":
    main()
