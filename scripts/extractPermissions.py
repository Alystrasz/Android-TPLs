__author__ = 'rsain'

'''
This script processes APK files in a folder getting for each file its Android permissions.
It prints for each APK file its Android permissions.
It generates a CSV file with the list of Android permissions of each file.
'''

from subprocess import *
import os.path

#The API library under study
SDK_TYPE = "CrashReporting"

# Folder containing the apk files
APKS_FOLDER = "/Experiments/" + SDK_TYPE + "/apks/"

# Folder where the CSV file is going to be saved
OUTPUT = "/Experiments/" + SDK_TYPE + "/results/permissions.csv"

outputFile = open(OUTPUT, "w")
outputFile.write("SdkName,SdkType,Permission\n")

# for each apk in the folder
for file in sorted(os.listdir(APKS_FOLDER)):
    if os.path.isfile(APKS_FOLDER + '/' + file):
        fileName, fileExtension = os.path.splitext(file)

        # Use only apk files
        if fileExtension == '.apk':
            print("Processing file '" + fileName + ".apk' ...")            
            sdkName = fileName.split("-")[0]

            # get Android permissions (reading the apk file)            
            permissions = check_output("aapt d permissions " + APKS_FOLDER + '/' + file, shell=True, universal_newlines=True)        
            
            totalPermissions = 0
            for permission in permissions.splitlines():
		permissionName = ""
		permissionInfo = permission.split("uses-permission: name=")
		if len(permissionInfo) > 1:
			totalPermissions = totalPermissions + 1
			permissionName = permissionInfo[1].replace("'","")
			print (" -> " + permissionName)
			outputFile.write(sdkName + "," + SDK_TYPE + "," + permissionName)
			outputFile.write("\n")
            if (totalPermissions == 0):
		print (" -> NA")
		outputFile.write(sdkName + "," + SDK_TYPE + ",NA")
		outputFile.write("\n")
outputFile.close()

print("DONE!")
