__author__ = 'rsain'

'''
This script processes APK files in a folder computing for each file its size.
It prints for each APK file its size (in MB).
It generates a CSV file with the size (in MB) of each file.
'''

import os
import natsort

#The API library under study
SDKTYPE = "CrashReporting"

# Folder containing the apk files
DATA_FOLDER = '/Experiments/' + SDKTYPE + '/apks/' 

# Folder where the CSV file is going to be saved
OUTPUT_FOLDER = '/Experiments/' + SDKTYPE + '/results/' 

# Filename for the CSV file containing the information for each run
OUTPUT_FILE = 'apkSizes.csv'

outputFile = open(OUTPUT_FOLDER + OUTPUT_FILE, "w")
outputFile.write("SdkName,SdkType,Size\n")

# for each apk in the folder
for file in natsort.natsorted(os.listdir(DATA_FOLDER)):
    if os.path.isfile(DATA_FOLDER + file):
        fileName, fileExtension = os.path.splitext(file)

        # Use only apk files
        if fileExtension == '.apk':
		print("Processing file '" + fileName + ".apk' ...") 
		sdkName = fileName.split('-')[0]
		size = float(os.path.getsize(DATA_FOLDER + file))/1024/1024
		print("-> " + str(size) + "MB")
		outputFile.write(sdkName + "," + SDKTYPE + "," + str(size) + "\n")
outputFile.close()
print("DONE!")
