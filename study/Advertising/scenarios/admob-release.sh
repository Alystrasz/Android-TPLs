NAME="admob"

PACKAGE="ruben.soccerlab.$NAME"
ACTIVITY="ruben.soccerlab.$NAME.MainActivity"

# Launch app
am start -n $PACKAGE/$ACTIVITY

# Wait few seconds to load first ad
sleep 10
