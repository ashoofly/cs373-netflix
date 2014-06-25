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

# -------
# globals
# -------

CACHE_PATH = '../netflix-tests'
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

def load_movie_info():
    with open(MOVIE_TITLES, 'r', encoding='latin-1') as f:
        while True:
            line = f.readline()
            if line == "":
                return None
            movie_ID, year, title = line.split(',')[:3]
            movie_ID = int(movie_ID)
            movie_info[movie_ID] = (year, title)

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
    # Load Customer Ratings by decade
    with open(CUSTOMER_BY_DECADE, 'r') as f:
        global cust_ratings_by_decade
        cust_ratings_by_decade = json.load(f)
    # Load Movie Avgs by decade
    with open(MOVIES_BY_DECADE, 'r') as f:
        global movies_by_decade
        movies_by_decade = json.load(f)
    # Load Individual Movie Info
    load_movie_info()

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
    
# -----------------------
# netflix_getCustByDecade
# -----------------------

def netflix_getCustByDecade (customerID, decade) :
    return cust_ratings_by_decade[customerID][str(decade)]

# ----------------------------
# netflix_getAvgRatingByDecade
# ----------------------------

def netflix_getAvgRatingByDecade (decade) :
    return movies_by_decade[str(decade)]

# -------------------
# netflix_algorithm_1
# -------------------

def netflix_algorithm_1 (movieID, customerIDs) :
    """
    returns simple averages
    """
    movie_mean, movie_median, movie_std_avg, movie_std_med  = netflix_getMovieStats(movieID)
    return [((netflix_getCustStats(i)[0] + movie_mean)/2) for i in customerIDs]

# -------------------
# netflix_algorithm_2
# -------------------

def netflix_algorithm_2 (movieID, customerIDs) :
    """
    returns simple medians
    """
    movie_mean, movie_median, movie_std_avg, movie_std_med  = netflix_getMovieStats(movieID)
    return [((netflix_getCustStats(i)[1] + movie_median)/2) for i in customerIDs]

# -------------------
# netflix_algorithm_3
# -------------------

def netflix_algorithm_3 (predict_1, predict_2) :
    """
    takes in predict_1 as averages
    takes in predict_2 as medians
    returns average of average and medians
    """
#   our_predict = [map(lambda x, y: (x+y)/2, predict_1, predict_2)]
    return [(predict_1[i] + predict_2[i])/2 for i in range(0, len(predict_1))] 


# -------------------
# netflix_algorithm_4
# -------------------

def netflix_algorithm_4 (movieID, customerIDs) :
    """
    returns simple average of (best(mean, med) for movies, best(mean, med) for customers)
    """
    movie_mean, movie_median, movie_std_avg, movie_std_med  = netflix_getMovieStats(movieID)
    results = []
    value1 = None
    if movie_std_med <= movie_std_avg :
        value1 = movie_median
    else :
        value1 = movie_mean

    for i in customerIDs:
        cust_mean, cust_median, cust_std_avg, cust_std_med = netflix_getCustStats(i)
        value2 = None
        if (cust_std_med <= cust_std_avg) :
            value2 = cust_median
        else :
            value2 = cust_mean
        results.append((value1 + value2)/2)

    return results

# -------------------
# netflix_algorithm_5
# -------------------

def netflix_algorithm_5 (movieID, customerIDs) :
    """
    returns weighted average of (weightedAvg(mean, med) for movies, weightedAvg(mean, med) for customers)
    """
    movie_mean, movie_median, movie_std_avg, movie_std_med  = netflix_getMovieStats(movieID)
    
    results = []
    movieStat = None
    movieStd = None
    if movie_median != movie_mean :
        movieStat = (movie_mean*movie_std_avg + movie_median*movie_std_med) / (movie_std_med + movie_std_avg)
        movieStd = (movie_std_med + movie_std_avg) / 2
    else :
        movieStat = movie_mean
        movieStd = movie_std_avg

    for i in customerIDs:
        cust_mean, cust_median, cust_std_avg, cust_std_med = netflix_getCustStats(i)
        if cust_mean != cust_median :
            custStat = (cust_mean*cust_std_avg + cust_median*cust_std_med) / (cust_std_med + cust_std_avg)
            custStd = (cust_std_med + cust_std_avg) / 2
        else :
            custStat = cust_mean
            custStd = cust_std_avg
        results.append((custStat*custStd + movieStat*movieStd) / (movieStd + custStd))

    return results

# -------------------
# netflix_algorithm_6
# -------------------

def netflix_algorithm_6 (movieID, customerIDs) :
    """
    OffsetApproach
    """
    universal_mean = 3.604289964420661
    movie_mean, movie_median, movie_std_avg = netflix_getMovieStats(movieID)
    return [round(movie_mean + netflix_getCustStats(i)[0] - universal_mean, 1)
            for i in customerIDs]

# -------------------
# netflix_algorithm_7
# -------------------

def netflix_algorithm_7 (movieID, customerIDs) :
    """
    OffsetApproach by decade
    """
    movie_mean, movie_median, movie_std_avg = netflix_getMovieStats(movieID)
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
    #predict_1 = netflix_algorithm_1(movieID, customerIDs)
    #predict_2 = netflix_algorithm_2(movieID, customerIDs)
    #predict_3 = netflix_algorithm_3(predict_1, predict_2)
    #predict_4 = netflix_algorithm_4(movieID, customerIDs)
    #predict_5 = netflix_algorithm_5(movieID, customerIDs)
    #predict_6 = netflix_algorithm_6(movieID, customerIDs)
    predict_7 = netflix_algorithm_7(movieID, customerIDs)
    actual = netflix_getTrueRating(movieID, customerIDs)
    netflix_update_sds(predict_7, actual)
    return predict_7

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

