#!/usr/bin/env python3

# ---------------------------
# Netflix.py
# Copyright (C) 2014
# Omar Lalani
# Angela Hsu
# ---------------------------



# ------------
# netflix_read
# ------------

def netflix_read (r) :
    """
    read 
    r is a reader
    return movieID, otherwise a list of zeros
    """
    while True :
        s = r.readline()
        if s == "" :
            return None
        elif ":" in movieID :
            

    a = s.split()
    return [int(v) for v in a]

# ------------
# netflix_eval
# ------------

def netflix_eval (movieID, customerIDs) :
    """
    movieID is the movie id
    customerIDs is the list of customer ids
    return list of customer ratings
    """
    # <your code>
    return 1

# -------------
# netflix_print
# -------------

def netflix_print (w, i, j, v) :
    """
    print three ints
    w is a writer
    i is the beginning of the range, inclusive
    j is the end       of the range, inclusive
    v is the max cycle length
    """
    w.write(str(i) + " " + str(j) + " " + str(v) + "\n")

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    read, eval, print loop
    r is a reader
    w is a writer
    """
    try:
        while True :
            movieID, customerIDs = netflix_read(r) # Sends back tuple(movieID, customerIDs)
            customerRatings = netflix_eval(movieID, customerIDs) # Sends back tuple(movieID, ratings)
            netflix_print(w, movieID, customerRatings)
    except EOF:        
        #print RMSE






