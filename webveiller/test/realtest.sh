run () {
    curl -X $1 -H "Content-Type: application/json" -d "$3" "https://webveiller.rpurp.com/api/$2"
}

echo STARTING TESTS-----------------

data=`jo token="dun-serb-thief-plank" category="cat" task="first" start_datetime="2019-04-01T09:00:00"`
run POST cancel "$data"

data=`jo token="dun-serb-thief-plank"`
run GET status "$data"

