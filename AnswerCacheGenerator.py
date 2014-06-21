#!/usr/bin/env python3

# -------------------------------
# AnswerCacheGenerator.py
# Copyright (C) 2014
# Omar Lalani
# Angela Hsu
# -------------------------------

import json

def getRatings (movieID, customerIDs) :
	f = open("/u/downing/cs/netflix/training_set/mv_" + str(movieID).zfill(7) + ".txt")
	f.readline()
	rating = -1
	for line in f :
		custID, rating, date = line.split(",")
		if custID in customerIDs :
			AnswerCache[str(movieID) + "-" + str(custID)] = rating
	f.close()

	

AnswerCache = {}
probe = open("/u/downing/cs/netflix/probe.txt")
movieID = None
customerIDs = None
for line in probe :
	if ":" in line :
		if movieID :
			getRatings(movieID, customerIDs)
		movieID = line.rstrip()[:-1]
		customerIDs = []
		print(movieID)
		continue
	customerIDs.append(line.rstrip())
probe.close()


with open('AnswerCache.json', 'w') as fp:
    json.dump(AnswerCache, fp)