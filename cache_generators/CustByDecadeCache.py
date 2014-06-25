#!/usr/bin/env python3
import os, json
# -------------------------------
# CustByDecadeCache.py
# Copyright (C) 2014
# Omar Lalani
# Angela Hsu
# -------------------------------



MOVIE_TITLES = '/u/downing/cs/netflix/movie_titles.txt'
NUM_MOVIES = 17770
movie_info = [None] * (NUM_MOVIES+1)

Customers = {}

def load_movie_info():
    with open(MOVIE_TITLES, 'r', encoding='latin-1') as f:
        while True:
            line = f.readline()
            if line == "":
                return None
            movie_ID, year, title = line.split(',')[:3]
            movie_ID = int(movie_ID)
            movie_info[movie_ID] = (year, title)

def init_decades_list():
    MIN_DECADE = 1890
    MAX_DECADE = 2005
    decades = {}
    range_start = MIN_DECADE
    while range_start < MAX_DECADE:
        decades[range_start] = []    
        range_start += 10
    return decades

def update_customer_ratings(movie_file):
    global Customers
    with open(movie_file, 'r') as f:
        movieID = int(f.readline()[:-2])
        movie_year = movie_info[movieID][0] 
        if movie_year != 'NULL':
            movie_year = int(movie_info[movieID][0]) 
            movie_title = movie_info[movieID][1]
            movie_decade = movie_year - (movie_year%10)
    #        print("{}: {}{}. (Decade: {})".format(movieID, movie_title, movie_year, movie_decade))

            for line in f :
                custID, rating, date = line.split(",")
                if custID in Customers :
                    Customers[custID][movie_decade].append(int(rating))
                    
                else :
                    decades = init_decades_list()
                    decades[movie_decade].append(int(rating))
                    Customers[custID] = decades

def calculate_decade_avgs():
    global Customers
    for customer, info in Customers.items():
        for decade, ratings in info.items():
            if len(ratings) != 0:
                avg_for_decade = sum(ratings)/len(ratings)
            else:
                avg_for_decade = 0
            info[decade] = avg_for_decade

def gather_all_ratings():
#    sample = [1, 76, 358, 4234]
#    for movieID in sample:
    for movieID in range(1, 17771) : #17771
        print(movieID)
        downing_dir = "/u/downing/cs/netflix/training_set"
        single_movie = 'mv_{}.txt'.format(str(movieID).zfill(7))
        movie_file = os.path.join(downing_dir, single_movie)
#        movie_file = single_movie
        update_customer_ratings(movie_file)

if __name__ == '__main__':
    load_movie_info()
    gather_all_ratings()
    print("Calculating decade avgs for each customer...")
    calculate_decade_avgs()
    print("Dumping to json...")            
    with open("cust_by_decade.json", 'w') as fp:
        json.dump(Customers, fp)
    print("Done.")


