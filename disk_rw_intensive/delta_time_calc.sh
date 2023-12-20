#!/bin/bash

echo "NOTE: no input validation!"
echo "---"
echo "Enter the first time components (hours minutes seconds milliseconds):"
echo "Usage: xx xx xx xxx"
echo "e.g. 01 33 33 337"
echo "---Enter Value 1---"
read hour1 min1 sec1 msec1

echo "---"
echo "Enter the second time components (hours minutes seconds milliseconds):"
echo "Usage: xx xx xx xxx"
echo "e.g. 01 33 33 337"
echo "---Enter Value 2---"
read hour2 min2 sec2 msec2

# Calculate the time difference in milliseconds
diff_msec=$(( ( (hour2 - hour1 + 24) % 24 ) * 60 * 60 * 1000 + (min2 - min1) * 60 * 1000 + (sec2 - sec1) * 1000 + (msec2 - msec1) ))

echo "---Result---"
echo "Time difference: ${diff_msec} milliseconds"
