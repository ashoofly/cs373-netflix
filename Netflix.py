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
ANSWER_CACHE = os.path.join(CACHE_PATH, 'osl62-AnswerCache.json')
avg_movie_ratings = {}
avg_customer_ratings = {}
answer_cache = {}
sds = 0.0
counter = 0

# --------------
# netflix_caches
# --------------

def netflix_caches () :
    # Load Average Rating Per Movie Cache
    with open(MOVIE_AVGS, 'r') as f:
        global avg_movie_ratings
        avg_movie_ratings = json.load(f)
    # Load Average Rating Given Per Customer Cache
    with open(CUSTOMER_AVGS, 'r') as f:
        global avg_customer_ratings
        avg_customer_ratings = json.load(f)
    # Load Answer Cache
    with open(ANSWER_CACHE, 'r') as f:
        global answer_cache
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

# -------------------
# netflix_getMovieAvg
# -------------------

def netflix_getMovieAvg (movieID) :
    return avg_movie_ratings[movieID]

# ------------------
# netflix_getCustAvg
# ------------------

def netflix_getCustAvg (customerID) :
    return avg_customer_ratings[customerID]

# --------------------
# netflix_getTrueRating
# ---------------------

def netflix_getTrueRating (movieID, customerIDs) :
    return [answer_cache[movieID + "-" + i] for i in customerIDs]
    
# ------------------
# netflix_getCustAvg
# ------------------

def netflix_algorithm_1 (movieID, customerIDs) :
    predict_list = []
    movieAvg = netflix_getMovieAvg (movieID)
    for i in customerIDs:
        predict_list.append((netflix_getCustAvg(i) + movieAvg)/2)
    return predict_list

# ------------------
# netflix_update_sds
# ------------------

def netflix_update_sds (predict, actual) :
    global sds, counter
    sds += sum(map(lambda x,y: (x-y)**2, predict, actual))
    counter += len(actual)

# ------------
# netflix_eval
# ------------

def netflix_eval (movieID, customerIDs) :
    """
    movieID is the movie id
    customerIDs is the list of customer ids
    return list of customer ratings

    """
    predict_1 = netflix_algorithm_1(movieID, customerIDs)
    actual = netflix_getTrueRating(movieID, customerIDs)
    netflix_update_sds(predict_1, actual)
    return predict_1

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

# ------------------
# netflix_print_RMSE
# ------------------

def netflix_print_RMSE(w):
    w.write("RMSE: " + str(math.sqrt(sds / counter)) + "\n")

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    read, eval, print loop
    r is a reader
    w is a writer
    """
    movie_ID = None
    while True:
        customer_IDs, movie_ID, next_movie = netflix_read(r, movie_ID) 
        customer_ratings = netflix_eval(movie_ID, customer_IDs) 
        netflix_print(w, movie_ID, customer_ratings)
        if next_movie:
            movie_ID = next_movie
        else:
            break
    print_RMSE(w)

