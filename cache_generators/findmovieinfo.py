#!/usr/bin/env python3

# -------------------------------
# MovieDecadeCache.py
# Copyright (C) 2014
# Omar Lalani
# Angela Hsu
# -------------------------------

import sys

MOVIE_TITLES = '/u/downing/cs/netflix/movie_titles.txt'
NUM_MOVIES = 17770
movie_info = [None] * (NUM_MOVIES+1)


def load_movie_info():
    with open(MOVIE_TITLES, 'r', encoding='latin-1') as f:
        while True:
            line = f.readline()
            if line == "":
                return None
#            print(line.split(','))
            movie_ID, year, title = line.split(',')[:3]
            movie_ID = int(movie_ID)
            movie_info[movie_ID] = (year, title)

def get_movie_info(movieID):
   print(movie_info[movieID])
    
if __name__ == "__main__":
    load_movie_info()
    while True:
        s = input('Enter movie ID: ')
        movieID = int(s)
        if movieID<1 or movieID>17770:
            print("Movie ID must be between 1 and 17770")
            continue
        get_movie_info(movieID)   
    

