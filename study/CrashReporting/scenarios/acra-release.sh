PACKAGE="ruben.soccerlab.acra"
ACTIVITY="ruben.soccerlab.acra.MainActivity"

# Launch app ("Launch app" entry in partition_info.csv file)
adb shell am start -n $PACKAGE/$ACTIVITY

# Wait few seconds to simulate user waiting
sleep 3

# Press button to crash the app
adb shell input tap 300 600

# Sleep some time (expecting that information is sent to the server)
sleep 3

# Close Android message about the crash
adb shell input tap 500 1300

# Sleep some time (expecting that information is sent to the server)
sleep 3
