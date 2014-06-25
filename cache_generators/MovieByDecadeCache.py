#!/usr/bin/env python3
import os, json
# -------------------------------
# MovieByDecadeCache.py
# Copyright (C) 2014
# Omar Lalani
# Angela Hsu
# -------------------------------



MOVIE_TITLES = '/u/downing/cs/netflix/movie_titles.txt'
NUM_MOVIES = 17770
movie_info = [None] * (NUM_MOVIES+1)
RatingsByDecade = {}

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
    global RatingsByDecade
    MIN_DECADE = 1890
    MAX_DECADE = 2005
    RatingsByDecade = {}
    range_start = MIN_DECADE
    while range_start < MAX_DECADE:
        RatingsByDecade[range_start] = [0, 0]  #[sum, count]    
        range_start += 10

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
    global RatingsByDecade
    for decade in RatingsByDecade:
    #avg movie rating for decade
        RatingsByDecade[decade] = RatingsByDecade[decade][0]/
                                  RatingsByDecade[decade][1]  

def add_movie_ratings(movie_file):
    global RatingsByDecade
    with open(movie_file, 'r') as f:
        movieID = int(f.readline()[:-2])
        movie_year = movie_info[movieID][0] 
        if movie_year != 'NULL':
            movie_year = int(movie_info[movieID][0]) 
            movie_title = movie_info[movieID][1]
            movie_decade = movie_year - (movie_year%10)
    #        print("{}: {}{}. (Decade: {})".format(movieID, movie_title, movie_year, movie_decade))
            running_sum = 0
            for line in f :
                custID, rating, date = line.split(",")
                RatingsByDecade[movie_decade][0] += int(rating)
                RatingsByDecade[movie_decade][1] += 1
                 

def sum_ratings_per_decade():
#    sample = [1, 76, 358, 4234]
#    for movieID in sample:
    for movieID in range(1, 17771) : #17771
        print(movieID)
        downing_dir = "/u/downing/cs/netflix/training_set"
        single_movie = 'mv_{}.txt'.format(str(movieID).zfill(7))
        movie_file = os.path.join(downing_dir, single_movie)
#        movie_file = single_movie
        add_movie_ratings(movie_file)

if __name__ == '__main__':
    load_movie_info()
    init_decades_list()
    sum_ratings_per_decade()
    print("Calculating decade avgs for each customer...")
    calculate_decade_avgs()
    print("Dumping to json...")            
    with open("ratings_by_decade.json", 'w') as fp:
        json.dump(RatingsByDecade, fp)
    print("Done.")


