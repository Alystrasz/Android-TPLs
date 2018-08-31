PACKAGE="ruben.soccerlab.flurry"
ACTIVITY="ruben.soccerlab.flurry.MainActivity"

# Launch app
am start -n $PACKAGE/$ACTIVITY

# Wait few seconds to simulate user waiting
sleep 1

# Swipe left
input swipe 600 500 100 500 100

# Wait few seconds to simulate user waiting
sleep 1

# Swipe left
input swipe 600 500 100 500 100

# Wait few seconds to simulate user waiting
sleep 1

# Swipe left
input swipe 600 500 100 500 100

# Wait few seconds to simulate user waiting
sleep 1

# Swipe right
input swipe 100 500 600 500 100

# Wait few seconds to simulate user waiting
sleep 1

# Swipe right
input swipe 100 500 600 500 100

# Wait few seconds to simulate user waiting
sleep 1

# Swipe right
input swipe 100 500 600 500 100

# Wait few seconds to simulate user waiting
sleep 1

# Back button (to pause/put the app in background)
input tap 145 1230

# Wait few seconds to wait until report is sent
sleep 12
