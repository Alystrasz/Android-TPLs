import csv

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
