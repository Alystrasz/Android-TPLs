# coding=utf-8
import Monsoon.HVPM as HVPM
import Monsoon.LVPM as LVPM
import Monsoon.sampleEngine as sampleEngine
import Monsoon.Operations as op
import Monsoon.pmapi as pmapi
import numpy as np
import sys
import time
import subprocess
import ntpath
import os
import threading


def initLVPM(serialno=None, Protcol=pmapi.USB_protocol()):
    Mon = LVPM.Monsoon()
    Mon.setup_usb(serialno,Protcol)
    print("LVPM Serial number: " + str(serialno))
    Mon.fillStatusPacket()
    Mon.setVout(4)

    timetoBoot = 150
    print("Voltage enabled")
    print("You have %d seconds to boot your phone, disable USB charging and check it is correctly detected (under adb "
          "devices) before measurements start." % timetoBoot)

    timer = timetoBoot -1
    while timer > -1:
        print("%d seconds remaining." % timer)
        sys.stdout.write("\033[F") # Cursor up one line
        timer -= 1
        time.sleep(1)

    launchMeasurements(Mon)


def launchMeasurements(Mon):
    engine = sampleEngine.SampleEngine(Mon)
    engine.ConsoleOutput(False)
    engine.setTriggerChannel(sampleEngine.channels.timeStamp) #Start and stop judged by the timestamp channel.

    scenarios = [
        ["../Analytics/scenarios/firebase-release.sh", "ruben.soccerlab.google"],
        ["../Analytics/scenarios/flurry-release.sh", "ruben.soccerlab.flurry"],
        ["../Analytics/scenarios/google-release.sh", "ruben.soccerlab.google"]
    ]

    for scenario in scenarios:
        for i in range(5):
            launchScenario(engine, scenario[0], Mon, i)
            clearPhoneState(scenario[1])

    Mon.closeDevice()

def launchScenario(engine, path, Mon, iteration):
    name = os.path.splitext(ntpath.basename(path))[0]
    print("Launching %s scenario (iteration n°%d)" % (name, iteration))
    engine.enableCSVOutput("results/%s-%s.csv" % (name, iteration))

    thread = samplingThread(engine, Mon)                                # launching sampling in a dedicated thread
    thread.start()
    subprocess.call(path, shell = True)                                 # launching scenario
    thread.kill()
    thread.join()

class samplingThread(threading.Thread):
    def __init__(self, engine, Mon, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
        self.engine = engine
        self.Mon = Mon

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)


    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup
        self.launchSampling()


    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True
        print("Stopping sampling")
        self.Mon.stopSampling()

    def launchSampling(self):
        print("Lauching sampling")
        numSamples=sampleEngine.triggers.SAMPLECOUNT_INFINITE # Don't stop based on sample count, continue until the trigger conditions have been satisfied.
        self.engine.startSampling(numSamples, 100)            # Setting a bigger granularity

def clearPhoneState(package):
    subprocess.call('adb shell am force-stop %s' % package, shell=True)
    time.sleep(2)

def main():
    LVPMSerialNo = 12431
    initLVPM(LVPMSerialNo,pmapi.USB_protocol())

if __name__ == "__main__":
    main()
