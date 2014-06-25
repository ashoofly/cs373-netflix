#!/usr/bin/env python3

# -------------------------------
# MovieCustomerCacheGenerator.py
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
	med = statistics.median_grouped(Ratings)
	MovieCache[str(movieID)] = (mu, med, statistics.pstdev(Ratings,mu), statistics.pstdev(Ratings,med))
	print(movieID)
	f.close()
for customer in Customers:
	mu = statistics.mean(Customers[customer])
	med = statistics.median_grouped(Customers[customer])
	CustomerCache[customer] = (mu, med, statistics.pstdev(Customers[customer],mu), statistics.pstdev(Customers[customer], med))

with open('MovieCache.json', 'w') as fp:
    json.dump(MovieCache, fp)

with open("CustomerCache.json", 'w') as fp:
	json.dump(CustomerCache, fp)