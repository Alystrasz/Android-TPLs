#!/bin/bash

#This script gets the package name of an APK file (app)
#It takes as parameter the path to an APK file.

package=`aapt dump badging $* | grep package | awk '{print $2}' | sed s/name=//g | sed s/\'//g`
echo $package
