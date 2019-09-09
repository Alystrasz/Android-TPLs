# coding=utf-8
import unittest
import sys
sys.path.append("..")
from classes import ExperimentsAnalyser

class TestExperimentsAnalyser(unittest.TestCase):

    def setUp(self):
        self.analyser = ExperimentsAnalyser.ExperimentsAnalyser("fake-results", 2)

    def test_experiments_count(self):
        self.assertEqual(len(self.analyser.experiments), 2) # 2 experiments were loaded

    def test_markers(self):
        markers = self.analyser.get_markers()
        self.assertEqual(markers["min"], 1.56)              # fake-results-1,  390mA * 4V / 1000
        self.assertEqual(markers["max"], 7.064)             # fake-results-0, 1766mA * 4V / 1000

    def test_mean(self):
        self.assertEqual(round(self.analyser.get_mean(), 3), round(2.751, 3))   # (2.872 + 2.630) / (2 * 1000)

    def test_standard_deviation(self):
        self.assertEqual(round(self.analyser.get_standard_deviation(), 3), round(1.335086169, 3)) # (1.577857915 + 1.092314424) / 2


if __name__ == '__main__':
    unittest.main()
