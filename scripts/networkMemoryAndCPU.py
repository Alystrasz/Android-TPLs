__author__ = 'ruben'

'''
This script processes APK files (apps) in a folder and plays, for each app, the associated scenario while collects information about three metrics: memory, CPU, and network usages.
Each app is run RUNS times to get statistical values.

Memory usage is measured using the Android tool dumpsys on the phone.
CPU usage is measured using the linux command top on the phone.
Network usage is measured using the tool tcpdump on the phone.
'''

#IMPORTANT NOTES:
#Copy the file runcommand.sh to folder SCRIPTS_ON_PHONE on the phone.
#Copy the program tcpdump to folder /system/bin/ on the phone and set permissions to 777 for this file.

import time
from subprocess import *
import subprocess
import os.path

#Constants
ADB_PATH = "/Android/Sdk/platform-tools/adb"
TOOLS_PATH = "/Android/Sdk/tools/bin"
RUNS = 30
PROJECT_FOLDER = "/Experiments/CrashReporting/"
APKS_FOLDER = PROJECT_FOLDER + "apks/"
SCENARIOS_FOLDER = PROJECT_FOLDER + "scenarios/"
OUTPUT_FOLDER = PROJECT_FOLDER + "data/"
SCENARIOS_ON_PHONE = "/mnt/sdcard/experiments/scenarios/"
SCRIPTS_ON_PHONE = "/mnt/sdcard/experiments/scripts/"
SAMPLING_TIME_FOR_MEMORY_IN_SECONDS = 1
SAMPLING_TIME_FOR_CPU_IN_SECONDS = 1
MEMINFO_OUTPUT_ON_PHONE = "/data/meminfo.dat"
TOPINFO_OUTPUT_ON_PHONE = "/data/topinfo.dat"
TCPDUMP_OUTPUT_ON_PHONE = '/data/network.pcap'
BUFFER_SIZE_FOR_TCPDUMP = 30000

#Copying scenarios on phone
print ("Copying scenarios on phone ...")
output = check_output(ADB_PATH + " push " + SCENARIOS_FOLDER + "* " + SCENARIOS_ON_PHONE, shell=True, universal_newlines=True)
print ("OUTPUT: " + output)

#Several runs to conduct statistical analysis)
for iteration in range(0, RUNS):
    appNumber = 0

    #for each file in the folder
    for file in os.listdir(APKS_FOLDER):
         if os.path.isfile(APKS_FOLDER + '/' + file):
             fileName, fileExtension = os.path.splitext(file)

             #Use only apk files
             if fileExtension == '.apk':
                #Info about current run
                appNumber = appNumber + 1
                sdkName = fileName.split("-")[0]
                appType = fileName.split("-")[1]
                pathScenario = SCENARIOS_ON_PHONE + sdkName + "-" + appType + ".sh"
                print("")
                print("+++++++++++++++++++++++++++++++++++++")
                print("RUN " + str(iteration + 1) + "/" + str(RUNS) + ", APP number " + str(appNumber))
                print("SDK name:    " + sdkName)                
                print("Type:        " + appType)
                print("Scenario:    " + pathScenario)
                print("+++++++++++++++++++++++++++++++++++++")
                package = subprocess.check_output(['./getPackageName.sh', APKS_FOLDER + '/' + file],
                                                  universal_newlines=True).strip()
                activity = subprocess.check_output(['./getMainActivity.sh', APKS_FOLDER + '/' + file],
                                                   universal_newlines=True).strip()
                outputDirectory = OUTPUT_FOLDER + str(sdkName) + "-" + str(package)
                outputFile = OUTPUT_FOLDER + sdkName + '-' + str(iteration + 1)
                
                # Disable auto-rotate option for screen
                subprocess.call(ADB_PATH + " shell settings put system accelerometer_rotation 0", shell=True)
                
                # Screen always is on
                subprocess.call(ADB_PATH + " shell svc power stayon true", shell=True)
                
                # Set battery level to 100%
                subprocess.call(ADB_PATH + " shell dumpsys battery set level 100", shell=True)
                
                # Clean the logcat on the phone
                subprocess.call(ADB_PATH + " logcat -c", shell=True)

                # Install the app
                print ("Installing app " + file + " ...")
                installOutput = check_output(ADB_PATH + " install " + APKS_FOLDER + '/' + file, shell=True, universal_newlines=True)
                print ("OUTPUT: " + installOutput)
                
                # Call to meminfo in the android phone (to measure memory)
                subprocess.call(ADB_PATH + " shell 'sh " + str(SCRIPTS_ON_PHONE) + "/runcommand.sh " + str(SAMPLING_TIME_FOR_MEMORY_IN_SECONDS) + " \"dumpsys meminfo --local " + package + "| grep TOTAL\" " + MEMINFO_OUTPUT_ON_PHONE + "' &", shell=True, universal_newlines=True)
                print("measuring meminfo on the phone")

                # Get the pid associated to meminfo
                pidMemory = subprocess.check_output(ADB_PATH + " shell ps | grep -w sh |  awk '{print $2}'", shell=True, universal_newlines=True)
                print("The PID associated to meminfo on the phone is " + pidMemory)
                
                # Call to top in the android phone (to measure CPU)
                subprocess.call(ADB_PATH + " shell 'top -d " + str(SAMPLING_TIME_FOR_CPU_IN_SECONDS) + " | grep " + package + " > " + TOPINFO_OUTPUT_ON_PHONE + "' &", shell=True, universal_newlines=True)
                print("top command started on the phone")
                
                # Get the pid associated to top
                pidTop = subprocess.check_output(ADB_PATH + " shell ps | grep -w top |  awk '{print $2}'", shell=True, universal_newlines=True)
                print("The PID associated to top on the phone is " + pidTop)
                
                #Call to tcpdump in the android phone (to measure network usage)
                tcp_file = open(outputFile + '.tcp_stats', 'w')
                subprocess.call(ADB_PATH + " shell tcpdump -s 0 -n -B " + str(BUFFER_SIZE_FOR_TCPDUMP) + " -i wlan0 -w" + TCPDUMP_OUTPUT_ON_PHONE + "&", shell=True, universal_newlines=True, stdout = tcp_file)
                tcp_file.close()
                print("tcpdump started")
                
                #Get the pid associated to tcpdump
                pidTcpdump = subprocess.check_output(ADB_PATH + " shell ps | grep tcpdump |  awk '{print $2}'", shell=True, universal_newlines=True)
                print("The PID associated to TCPDUMP is " + pidTcpdump)
                
                #Play the scenario
                print("Playing scenario.")
                subprocess.call(ADB_PATH + " shell 'sh " + pathScenario + "'", shell=True, universal_newlines=True)
                print("Scenario has finished.")
                
                # Kill the meminfo process
                subprocess.call(ADB_PATH + " shell kill -SIGTERM " + str(pidMemory), shell=True, universal_newlines=True)
                print("meminfo process in phone killed")
                
                # Kill the top process
                subprocess.call(ADB_PATH + " shell kill -SIGTERM " + str(pidTop), shell=True, universal_newlines=True)
                print("top process in phone killed")
                
                #Kill the tcpdump process and capture its output
                subprocess.call(ADB_PATH + " shell kill -SIGTERM " + str(pidTcpdump), shell=True, universal_newlines=True)
                print("tcpdump process in phone killed")
                
                #Stop the application
                print ("Stopping the app ...")
                call(ADB_PATH + " shell am force-stop " + str(package), shell=True)

                #Clean the application data
                print ("Cleaning cache for the app ...")
                call(ADB_PATH + " shell pm clear " + str(package), shell=True)

                #Uninstall the application
                print ("Uninstalling the app ...")
                uninstallOutput = check_output(ADB_PATH + " uninstall " + package, shell=True, universal_newlines=True)
                print ("OUTPUT: " + uninstallOutput)

                # Download the meminfo file from the phone
                print("downloading file generated by meminfo from phone")
                call(ADB_PATH + " pull " + MEMINFO_OUTPUT_ON_PHONE + " " + outputFile + '.mem', shell=True)
                print("finish download of file generated by meminfo from phone")
                # Cleaning format of memory file
                os.system("column -t " + outputFile + ".mem > " + outputFile + ".meminfo")
                # Generating file containing PSS information
                os.system("awk '{print $2}' " + outputFile + ".meminfo > " + outputFile + ".pss")  
                # Removing temp file about memory
                os.system("rm -fr " + outputFile + ".mem")  

                # Delete the file generated by meminfo on phone
                call(ADB_PATH + " shell rm " + MEMINFO_OUTPUT_ON_PHONE, shell=True)
                print("File generated by meminfo removed in phone")
                
                # Download the top file from the phone
                print("downloading file generated by top from phone")
                call(ADB_PATH + " pull " + TOPINFO_OUTPUT_ON_PHONE + " " + outputFile + ".top", shell=True)
                print("finish download of file generated by top from phone")

                # Delete the file generated by top from phone
                call(ADB_PATH + " shell rm " + TOPINFO_OUTPUT_ON_PHONE, shell=True)
                print("File generated by top removed in phone")                                
                
                #Download the tcpdump file from the phone
                print("downloading tcpdump file from phone")
                call(ADB_PATH + " pull " + TCPDUMP_OUTPUT_ON_PHONE + " " + outputFile + '.pcap', shell=True)
                print("finish download of tcpdump file from phone")
                
                #Delete the TCPDUMP file from phone
                call(ADB_PATH + " shell rm " + TCPDUMP_OUTPUT_ON_PHONE, shell=True)
                print("tcpdump file removed in phone")

#The screen is now off
subprocess.call(ADB_PATH + " shell svc power stayon false", shell=True)

#Removing scenarios on phone
print ("Removing scenarios on phone ...")
output = check_output(ADB_PATH + " shell rm -fr " + SCENARIOS_ON_PHONE + "*", shell=True, universal_newlines=True)
print ("OUTPUT: " + output)

print ("DONE!")
