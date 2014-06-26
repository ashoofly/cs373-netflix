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
import decimal

# --------
# globals
# --------

CACHE_PATH = '/u/mukund/netflix-tests'
MOVIE_STATS = os.path.join(CACHE_PATH, 'osl62-MovieCache.json')
CUSTOMER_STATS = os.path.join(CACHE_PATH, 'osl62-CustomerCache.json')
ANSWER_CACHE = os.path.join(CACHE_PATH, 'osl62-AnswerCache.json')
CUSTOMER_BY_DECADE = os.path.join(CACHE_PATH, 'ahsu-cust_by_decade.json')
MOVIES_BY_DECADE = os.path.join(CACHE_PATH, 'ahsu-ratings_by_decade.json')

movie_stats_cache = {}
customer_stats_cache = {}
answer_cache = {}
cust_ratings_by_decade = {}
movies_by_decade = {}
sds = 0.0
counter = 0

MOVIE_TITLES = '/u/downing/cs/netflix/movie_titles.txt'
NUM_MOVIES = 17770
movie_info = [None] * (NUM_MOVIES+1)
universal_mean = 3.604289964420661

# --------------
# netflix_caches
# --------------

def netflix_caches () :
    """Load all caches. Return nothing.

    """
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
    # Load Customer Ratings by decade
    with open(CUSTOMER_BY_DECADE, 'r') as f:
        global cust_ratings_by_decade
        cust_ratings_by_decade = json.load(f)
    # Load Movie Avgs by decade
    with open(MOVIES_BY_DECADE, 'r') as f:
        global movies_by_decade
        movies_by_decade = json.load(f)
    # Load Individual Movie Info
    with open(MOVIE_TITLES, 'r', encoding='latin-1') as f:
        while True:
            line = f.readline()
            if line == "":
                return None
            movie_ID, year, title = line.split(',')[:3]
            movie_ID = int(movie_ID)
            movie_info[movie_ID] = (year, title.rstrip())

# ------------
# netflix_read
# ------------

def netflix_read (r, movieID) :
    """Read one block (one movie, list of customers) from probe.txt
    
    Arguments:
        r - reader
        movieID - None if first movie; string otherwise
   
    Return:
        customers - list of customers IDs (strings)
        movieID - string 
        next_movie - string, or None

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
    """Look up statistics for specific movie in movie_stats_cache.
    
    Arguments:
        movieID - string
    Return:
        movie_mean, movie_median, movie_std - tuple 

    """
    return movie_stats_cache[movieID]

# ------------------
# netflix_getCustAvg
# ------------------

def netflix_getCustStats (customerID) :
    """Look up statistics for specific customer in customer_stats_cache.

    Arguments:
        customerID - string
    Return:
        cust_mean, cust_median, cust_std - tuple

    """
    return customer_stats_cache[customerID]

# --------------------
# netflix_getTrueRating
# ---------------------

def netflix_getTrueRating (movieID, customerIDs) :
    """Look up true customer rating for all 'customerIDs' for 'movieID'.
    
    Arguments:
        movieID - string
        customerIDs - list of strings  
    Return:
        list of true ratings in order of customerID
         
    """
    return [answer_cache[movieID + "-" + i] for i in customerIDs]
    
# -----------------------
# netflix_getCustByDecade
# -----------------------

def netflix_getCustByDecade (customerID, decade) :
    """Look up average customer rating per decade for a specific customerID.

    Arguments:
        customerID - string
        decade - int

    Return:
        float of avg rating
        
    """ 
    return cust_ratings_by_decade[customerID][str(decade)]

# ----------------------------
# netflix_getAvgRatingByDecade
# ----------------------------

def netflix_getAvgRatingByDecade (decade) :
    """Look up average movie rating by decade.

    Arguments:
        decade - int

    Return:
        float of avg movie rating

    """
    return movies_by_decade[str(decade)]

# -------------------
# netflix_algorithm_7
# -------------------

def netflix_algorithm_7 (movieID, customerIDs) :
    """Predict customer ratings of particular movie using the offset approach
       by decade if movie year available.

    Arguments:
        movieID - string
        customerIDs - list of strings
    Return:
        list of predicted customer ratings

    """
    movie_mean, movie_median, movie_std = netflix_getMovieStats(movieID)
    movie_year = movie_info[int(movieID)][0]
    if movie_year != 'NULL':
        movie_year = int(movie_year)
        movie_decade = movie_year - (movie_year%10)
        avg_rating_per_decade = netflix_getAvgRatingByDecade(movie_decade)
        return [round(movie_mean + netflix_getCustByDecade(i, movie_decade) - 
                avg_rating_per_decade, 1) for i in customerIDs]
    else:
        return [round(movie_mean + netflix_getCustStats(i)[0] - universal_mean, 1)
                for i in customerIDs]

# ------------------
# netflix_update_sds
# ------------------

def netflix_update_sds (predict, actual) :
    """Update running sum of squared differences between predicted and actual rating.
    
    Arguments:
        predict - our predicted rating (float)
        actual - true rating from answer cache (float) 
    Return:
        Nothing

    """
    global sds, counter
    sds += sum(map(lambda x,y: (x-y)**2, predict, actual))
    counter += len(actual)

# ------------
# netflix_eval
# ------------

def netflix_eval (movieID, customerIDs) :
    """Run prediction algorithm, get true rating, update running sum of squared differences.

    Arguments:
        movieID - string
        customerIDs - list of strings
    Return:
        predicted rating - float
    
    """
    predict_7 = netflix_algorithm_7(movieID, customerIDs)
    actual = netflix_getTrueRating(movieID, customerIDs)
    netflix_update_sds(predict_7, actual)
    return predict_7

# -------------
# netflix_print
# -------------

def netflix_print (w, movie_ID, customer_ratings) :
    """Output movieID and one customer rating on each line.
    
    Arguments:
        w - writer
        movie_ID - string
        customer_ratings - string

    Return:
        Nothing    

    """
    w.write(movie_ID + ":\n")
    for i in customer_ratings:
        w.write(str(format(i, '.1f')) + "\n")

# ------------------
# netflix_print_RMSE
# ------------------

def netflix_print_RMSE(w):
    """Output RMSE.

    Arguments:
        w - writer

    Return:
       Nothing 

    """
    w.write("RMSE: " + str( format( math.sqrt(sds / counter), '.4f' ) + "\n") )

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """Main function to run solver.

    Arguments:
        r - reader
        w - writer

    Return:
        Nothing

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

