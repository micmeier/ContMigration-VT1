cat <<EOF >mongodb_script.sh
#!/bin/bash



# Retrieve the last inserted key or initialize it
last_key=\$(mongosh --quiet --eval "db.testTony.findOne({}, { _id: 0, key: 1 }).key")

if [ -z "\$last_key" ]; then
    last_key=0
fi

# Save the current time in milliseconds
start_time=\$(date +%s%3N)
formatted_time=\$(date +%T)

# Open mongoshell and use the desired database
mongosh --eval "use test"

# print last inserted key
echo "Last inserted key:   \$last_key"

# Loop to insert 1000 random key-value pairs into the "testTony" collection
for ((i = \$last_key + 1; i <= last_key + 1000; i++)); do
    key="key_\$i"
    value="value_\$i"
    mongosh --quiet --eval "db.testTony.insertOne({ \"\$key\": \"\$value\" })"
    echo "—————"
    echo "Inserted document with key:   \$key"
    echo "Inserted document with value:         \$value"

# Calculate the elapsed time in milliseconds
	current_time=\$(date +%s%3N)
	elapsed_time=\$((current_time - start_time))

# Print the starting time
	echo "Starting Time: 			\$formatted_time"

# Print the current time
	current_time=\$(date +%T.%3N)
	echo "Current Time: 			\$current_time"


# Print the elapsed time
	echo "Elapsed Time: 			\$elapsed_time ms"

# Retrieve the last inserted key and store it for future runs
	last_inserted_key=\$(mongosh --quiet --eval "db.testTony.find().sort({key: -1}).limit(1).next().key" | awk "{print $2}")
	echo "Last inserted key: \$last_inserted_key"

done




EOF

chmod 755 mongodb_script.sh

echo “Starting MongoDB script :D”

echo “Type exit to see output :D”

./mongodb_script.sh
