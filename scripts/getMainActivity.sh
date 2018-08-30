#!/bin/bash

#This script gets the main activity of an APK file (app)
#It takes as parameter the path to an APK file.

activity=`aapt dump badging $* | grep launchable-activity: | awk '{print $2}' | sed s/name=//g | sed s/\'//g`
echo $activity
