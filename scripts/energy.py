__author__ = 'rsain'

'''
This script processes APK files (apps) in a folder and plays, for each app, the associated scenario while collects energy consumption.
Each app is run RUNS times to get statistical values.
Energy consumption is measured in Joules (J).
'''

import time
from subprocess import *
from OscilloscopeFunctions import *
from ctypes import *
import subprocess
import os

# The callback function to run when data is ready
CALLBACK_DATA_READY = CFUNCTYPE(None, c_void_p)


def myfunction1(parameters):
    global dataRead

    if scp.is_data_overflow:
        print('Data overflow!')
        sys.exit(-1)
    else:
        d = scp.get_data()
        dataRead.append(d[0])
        dataRead.append(d[1])


func_data_ready = CALLBACK_DATA_READY(myfunction1)

# The callback function to run when there is overflow
CALLBACK_DATA_OVERFLOW = CFUNCTYPE(None, c_void_p)


def myfunction2(parameters):
    if scp.is_data_overflow:
        print('Data overflow!')
        sys.exit(-1)


func_data_overflow = CALLBACK_DATA_OVERFLOW(myfunction2)

# Constants
ADB_PATH = "/Android/Sdk/platform-tools/adb"
TOOLS_PATH = "/Android/Sdk/tools"
RUNS = 30
TIME_INIT = 0
FREQUENCY = 125000  # Frequency to be set in the oscilloscope to measure.
PHONE_VOLTAGE = 3.9
PROJECT_FOLDER = "/Experiments/CrashReporting/"
APKS_FOLDER = PROJECT_FOLDER + "apks/"
SCENARIOS_FOLDER = PROJECT_FOLDER + "scenarios/"
OUTPUT_FOLDER = PROJECT_FOLDER + "data/"
SCENARIOS_ON_PHONE = "/mnt/sdcard/experiments/scenarios/"
COLLECT_DATA = True

# Prepare oscilloscope:
if COLLECT_DATA:
    dataRead = []
    print("Connecting to oscilloscope ...")
    scp = connectToOscilloscope(FREQUENCY, 1000, func_data_ready, func_data_overflow)
    print("Measuring during 5 seconds to heat the oscilloscope ...")
    measuringToHeatOscilloscope(scp, 5)

# Copying scenarios on phone
print("Copying scenarios on phone ...")
output = check_output(ADB_PATH + " push " + SCENARIOS_FOLDER + "* " + SCENARIOS_ON_PHONE, shell=True, universal_newlines=True)
print("OUTPUT: " + output)

# For each iteration
for iteration in range(0, RUNS):
    appNumber = 0

    # for each file in the folder
    for file in os.listdir(APKS_FOLDER):
        if os.path.isfile(APKS_FOLDER + '/' + file):
            fileName, fileExtension = os.path.splitext(file)

            # Use only apk files
            if fileExtension == '.apk':
                # Info about current run
                appNumber = appNumber + 1
                chunksRead = 0
                dataRead = []
                sdkName = fileName.split("-")[0]
                appType = fileName.split("-")[1]
                pathScenario = SCENARIOS_ON_PHONE + sdkName + "-" + appType + ".sh"
                print("ITERATION " + str(iteration + 1) + "/" + str(RUNS) + ", APP number 1")
                print("SDK name: " + sdkName)
                print("Type:        " + appType)
                print("Scenario:    " + pathScenario)
                package = subprocess.check_output(['./getPackageName.sh', APKS_FOLDER + '/' + file],
                                                  universal_newlines=True).strip()
                activity = subprocess.check_output(['./getMainActivity.sh', APKS_FOLDER + '/' + file],
                                                   universal_newlines=True).strip()
                outputDirectory = OUTPUT_FOLDER + str(sdkName) + "-" + str(package)
                outputFile = OUTPUT_FOLDER + sdkName + '-' + str(iteration + 1)

                # We disable auto-rotate option for screen
                subprocess.call(ADB_PATH + " shell settings put system accelerometer_rotation 0", shell=True)

                # The screen is always on
                subprocess.call(ADB_PATH + " shell svc power stayon true", shell=True)

                # Battery level to 100%
                subprocess.call(ADB_PATH + " shell dumpsys battery set level 100", shell=True)

                # We clean the logcat on the phone
                subprocess.call(ADB_PATH + " logcat -c", shell=True)

                # Install the application
                print("Installing app " + file + " ...")
                installOutput = check_output(ADB_PATH + " install " + APKS_FOLDER + '/' + file, shell=True,
                                             universal_newlines=True)
                print("OUTPUT: " + installOutput)

                if COLLECT_DATA:
                    # Start power monitor
                    scp.start()
                    print("starting to measure energy")

                #Play the scenario (it launches the app, wait 3 seconds, press a button which crashes the app, wait 3 seconds, press ok, and wait 3 seconds)
                print("Playing scenario.")
                subprocess.call(ADB_PATH + " shell 'sh " + pathScenario + "'", shell=True, universal_newlines=True)
                print("Scenario has finished.")

                # Stop power monitor
                if COLLECT_DATA:
                    scp.stop()
                    print("stopping energy measuring")

                #Stop the application
                print ("Stopping the app ...")
                call(ADB_PATH + " shell am force-stop " + str(package), shell=True)

                # Clean the application data
                print("Cleaning cache for the app ...")
                call(ADB_PATH + " shell pm clear " + str(package), shell=True)

                # Uninstall the application
                print("Uninstalling the app ...")
                uninstallOutput = check_output(ADB_PATH + " uninstall " + package, shell=True, universal_newlines=True)
                print("OUTPUT: " + uninstallOutput)

                # Save energy file
                if COLLECT_DATA:
                    print("writting energy file")
										energyTraceGenerated = saveDataToZipFileCalculatingPowerUsinguCurrentVoltageFixed(outputFile + ".energy",dataRead, float(PHONE_VOLTAGE), TIME_INIT,FREQUENCY)
                    
                    if energyTraceGenerated:
                        print('Energy file written')
                    else:
                        print('Error writing energy file')

# The screen is now off
subprocess.call(ADB_PATH + " shell svc power stayon false", shell=True)

# Removing scenarios on phone
print("Removing scenarios on phone ...")
output = check_output(ADB_PATH + " shell rm -fr " + SCENARIOS_ON_PHONE + "*", shell=True, universal_newlines=True)
print("OUTPUT: " + output)

# Close oscilloscope:
if COLLECT_DATA:
    del scp

print("DONE!")
