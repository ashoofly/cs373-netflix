#!/usr/bin/env python3

# ---------------------------
# Netflix.py
# Copyright (C) 2014
# Omar Lalani
# Angela Hsu
# ---------------------------

# -------
# imports
# -------

import os
import json

# -------
# globals
# -------

CACHE_PATH = '../netflix-tests'
MOVIE_AVGS = os.path.join(CACHE_PATH, 'rbrooks-movie_average_rating.json')
CUSTOMER_AVGS = os.path.join(CACHE_PATH, 'bryan-customer_cache.json')
ANSWER_CACHE = os.path.join(CACHE_PATH, 'AnswerCache.json')
avg_movie_ratings = {}
avg_ratings_per_customer = {}
answer_cache = {}

# --------------
# netflix_caches
# --------------

def netflix_caches (self) :
    # Load Average Rating Per Movie Cache
    with open(MOVIE_AVGS, 'r') as f:
        avg_movie_ratings = json.load(f)
    # Load Average Rating Given Per Customer Cache
    with open(CUSTOMER_AVGS, 'r') as f:
        avg_ratings_per_customer = json.load(f)
    # Load Answer Cache
    with open(ANSWER_CACHE, 'r') as f:
        answer_cache = json.load(f)

# ------------
# netflix_read
# ------------

def netflix_read (r, movieID) :
    """
    netflix_read processes all customers under one movie 
    r is a reader
    return movieID, otherwise a list of zeros
    """
    if not movieID:
        movieID = r.readline()[:-2]
    customers = []
    line = r.readline()
    while ':' not in line:
        # customer ID
        customers.append(line.rstrip())
        line = r.readline()
        if line == "":
            return customers, movieID, None
    next_movie = line[:-2]
    return customers, movieID, next_movie


# ------------
# netflix_eval
# ------------

def netflix_eval (movieID, customerIDs) :
    """
    movieID is the movie id
    customerIDs is the list of customer ids
    return list of customer ratings
    """
    movie_avg = avg_movie_ratings[movieID]
    print(movie_avg)
    
    customer_avgs = [avg_ratings_per_customer[i] for i in customerIDs]
    print(customer_avgs)
    return [1.0] * len(customerIDs)

# -------------
# netflix_print
# -------------

def netflix_print (w, movie_ID, customer_ratings) :
    """
    print movie ID with colon
    print customer ratings, one on each line
    w is a writer
    """
    w.write(movie_ID + ":\n")
    for i in customer_ratings:
        w.write(str(i) + "\n")

def netflix_RSME(w):
    w.write("RMSE: 1\n")

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    read, eval, print loop
    r is a reader
    w is a writer
    """
    netflix_caches()
    movie_ID = None
    while True:
        customer_IDs, movie_ID, next_movie = netflix_read(r, movie_ID) 
        customer_ratings = netflix_eval(movie_ID, customer_IDs) 
        netflix_print(w, movie_ID, customer_ratings)
        if next_movie:
            movie_ID = next_movie
        else:
            break
    netflix_RSME(w)
