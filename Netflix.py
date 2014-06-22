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
import math

# -------
# globals
# -------

CACHE_PATH = '../netflix-tests'
MOVIE_STATS = os.path.join(CACHE_PATH, 'osl62-MovieCache.json')
CUSTOMER_STATS = os.path.join(CACHE_PATH, 'osl62-CustomerCache.json')
ANSWER_CACHE = os.path.join(CACHE_PATH, 'osl62-AnswerCache.json')
movie_stats_cache = {}
customer_stats_cache = {}
answer_cache = {}
sds = 0.0
counter = 0

# --------------
# netflix_caches
# --------------

def netflix_caches () :
    # Load Average Rating Per Movie Cache
    with open(MOVIE_STATS, 'r') as f:
        global movie_stats_cache
        movie_stats_cache = json.load(f)
    # Load Average Rating Given Per Customer Cache
    with open(CUSTOMER_STATS, 'r') as f:
        global customer_stats_cache
        customer_stats_cache = json.load(f)
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

def netflix_getMovieStats (movieID) :
    return movie_stats_cache[movieID]

# ------------------
# netflix_getCustAvg
# ------------------

def netflix_getCustStats (customerID) :
    return customer_stats_cache[customerID]

# --------------------
# netflix_getTrueRating
# ---------------------

def netflix_getTrueRating (movieID, customerIDs) :
    return [answer_cache[movieID + "-" + i] for i in customerIDs]
    
# -------------------
# netflix_algorithm_1
# -------------------

def netflix_algorithm_1 (movieID, customerIDs) :
    movie_mean, movie_median, movie_std_avg, movie_std_med  = netflix_getMovieStats(movieID)
    return [((netflix_getCustStats(i)[0] + movie_mean)/2) for i in customerIDs]

# -------------------
# netflix_algorithm_2
# -------------------

def netflix_algorithm_2 (movieID, customerIDs) :
    movie_mean, movie_median, movie_std_avg, movie_std_med  = netflix_getMovieStats(movieID)
    return [((netflix_getCustStats(i)[1] + movie_median)/2) for i in customerIDs]


# -------------------
# netflix_algorithm_3
# -------------------

def netflix_algorithm_3 (predict_1, predict_2) :
    '''Returns predicted rating from avg & median'''
 #   our_predict = [map(lambda x, y: (x+y)/2, predict_1, predict_2)]
    return [(predict_1[i] + predict_2[i])/2 for i in range(0, len(predict_1))] 


# -------------------
# netflix_algorithm_4
# -------------------

def netflix_algorithm_4 (movieID, customerIDs) :
    movie_mean, movie_median, movie_std_avg, movie_std_med  = netflix_getMovieStats(movieID)
    for i in customerIDs:
        cust_mean, cust_median, cust_std_avg, cust_std_med = netflix_getCustStats(i)


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
    predict_2 = netflix_algorithm_2(movieID, customerIDs)
    predict_3 = netflix_algorithm_3(predict_1, predict_2)
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
        w.write(str(format(i, '.1f')) + "\n")

# ------------------
# netflix_print_RMSE
# ------------------

def netflix_print_RMSE(w):
    w.write("RMSE: " + str( format( math.sqrt(sds / counter), '.4f' ) + "\n") )

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
    netflix_print_RMSE(w)

