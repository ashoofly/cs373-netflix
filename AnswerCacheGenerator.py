#!/usr/bin/env python3

# -------------------------------
# AnswerCacheGenerator.py
# Copyright (C) 2014
# Omar Lalani
# Angela Hsu
# -------------------------------

import json

AnswerCache = {}

def getRatings (movieID, customerIDs) :
	global AnswerCache
	localCache = {}
	size = len(AnswerCache)
	f = open("/u/downing/cs/netflix/training_set/mv_" + str(movieID).zfill(7) + ".txt")
	f.readline()
	rating = -1
	for line in f :
		custID, rating, date = line.split(",")
		localCache[custID] = int(rating)
	for x in customerIDs :
		AnswerCache[movieID + "-" + x] = localCache[x] 
	assert(len(AnswerCache) - size == len(customerIDs))
	f.close()


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

getRatings('9999', ['1473765'])


with open('AnswerCache.json', 'w') as fp:
    json.dump(AnswerCache, fp)