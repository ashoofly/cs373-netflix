#!/usr/bin/env python3

# -------------------------------
# MovieCacheGenerator.py
# Copyright (C) 2014
# Omar Lalani
# Angela Hsu
# -------------------------------

import json, statistics

MovieCache = {}
Customers = {}
CustomerCache = {}
for movieID in range(1, 17771) :
	f = open("/u/downing/cs/netflix/training_set/mv_" + str(movieID).zfill(7) + ".txt")
	f.readline()
	Ratings = []
	for line in f :
		custID, rating, date = line.split(",")
		Ratings.append(int(rating))
		if custID in Customers :
			Customers[custID] += [int(rating)]
		else :
			Customers[custID] = [int(rating)]
	mu = statistics.mean(Ratings)
	MovieCache[str(movieID)] = (mu, statistics.median_grouped(Ratings), statistics.pstdev(Ratings,mu))
	print(movieID)
	f.close()
for customer in Customers:
	mu = statistics.mean(Customers[customer])
	CustomerCache[customer] = (mu, statistics.median_grouped(Customers[customer]), statistics.pstdev(Customers[customer],mu))

with open('MovieCache.json', 'w') as fp:
    json.dump(MovieCache, fp)

with open("CustomerCache.json", 'w') as fp:
	json.dump(CustomerCache, fp)