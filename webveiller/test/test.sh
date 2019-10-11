run () {
    curl -X $1 -H "Content-Type: application/json" -d "$3" "http://localhost:5000/api/$2"
}

echo STARTING TESTS-----------------

rm data.csv

data=`jo token="dun-serb-thief-plank" category="cat" task="first" start_datetime="2019-04-01T09:00:00"`
run POST start "$data"

data=`jo token="debug password"`
run GET status "$data"

data=`jo token="debug password" end_datetime="2019-04-01T10:10:00"`
run POST end "$data"

data=`jo token="debug password"`
run GET status "$data"

data=`jo token="debug password" category="cat" task="second" start_datetime="2019-04-01T10:15:00"`
run POST start "$data"

data=`jo token="debug password"`
run GET status "$data"


