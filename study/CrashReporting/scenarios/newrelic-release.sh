PACKAGE="ruben.soccerlab.newrelic"
ACTIVITY="ruben.soccerlab.newrelic.MainActivity"

# Launch app ("Launch app" entry in partition_info.csv file)
am start -n $PACKAGE/$ACTIVITY

# Wait few seconds to simulate user waiting
sleep 3

# Press button to crash the app
input tap 300 600

# Sleep some time (expecting that information is sent to the server)
sleep 3

# Close Android message about the crash
input tap 626 667

# Sleep some time (expecting that information is sent to the server)
sleep 3
