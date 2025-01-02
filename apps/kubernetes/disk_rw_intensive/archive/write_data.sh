#!/bin/bash

kubectl exec -it mongo-0 -- /bin/sh cat <<EOF > mongodb_script.sh
#!/bin/sh

# Save the current time in milliseconds
start_time=\$(date +%s%3N)
formatted_time=\$(date +%T)
	
# Open mongoshell and use the desired database
mongosh --eval "use test"

# Loop to insert 1000 random key-value pairs into the "your_collection_name" collection
for i in {1..1000}
do
	    key="key_\$i"
	    value="value_\$i"
	    mongosh --quiet --eval "db.rini.insertOne({ \"\$key\": \"\$value\" })"
	    echo "—————"
	    echo "Inserted document with key: 	\$key"
	    echo "Inserted document with value: 	\$value"

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
done
EOF

kubectl exec -it mongo-0 -- /bin/sh chmod 755 mongodb_script.sh

kubectl exec -it mongo-0 -- /bin/sh echo “Starting MongoDB script :D”
	
kubectl exec -it mongo-0 -- /bin/sh echo “Type exit to see output :D”

kubectl exec -it mongo-0 -- /bin/sh ./mongodb_script.sh
