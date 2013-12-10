#!/bin/sh
for entry in "data"/*.txt
do
	for i in {1..3}
	do
		for j in {1..3}
		do
			python kNN.py -i $entry -k $i -y $j	
		done
	done
	echo "$entry"
done
