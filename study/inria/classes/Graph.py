import plotly.graph_objects as go
from scipy import signal

""" This class stores experiments and plots them on a user-manipulable graph """
class Graph:
    def __init__(self, title):
        self.experiments = []
        self.title = title
        self.fig = go.Figure()

    """ Adds an experiment to the list of stored exps """
    def addExperiment(self, experiment):
        self.experiments.append(experiment)

    """ Plots raw data on the graph """
    def plotExperiments(self):
        for exp in self.experiments:
            self.fig.add_trace(go.Scatter(x=exp.time, y=exp.power,
                                          name=exp.name,
                                          line=dict(color=exp.color, width=4),
                                          line_shape='spline'))

    """ Computes smoothed curves from data and plots them on the graph """
    def plotSmoothedExperiments(self):
        for exp in self.experiments:
            self.fig.add_trace(go.Scatter(x=exp.time,
                                          y=signal.savgol_filter(exp.power,
                                                                 23, # window size used for filtering
                                                                 3), # order of fitted polynomial,
                                          name=exp.name,
                                          line=dict(color=exp.color, width=8),
                                          line_shape='spline'))

    """ Renders and displays the final graph """
    def show(self):
        """ adding title """
        self.fig.update_layout(title=self.title,
                               xaxis_title='Time (sec)',
                               yaxis_title='Power (Watt)')
        self.fig.show()