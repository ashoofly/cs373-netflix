#!/usr/bin/env python3

# -------------------------------
# TestNetflix.py
# Copyright (C) 2014
# Omar Lalani
# Angela Hsu
# -------------------------------

"""
To test the program:
    % coverage3 run --branch TestNetflix.py

To obtain coverage of the test:
    % coverage3 report -m
"""

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

#from Netflix import *
import Netflix


# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase) :

    @classmethod
    def setUpClass(self) :
        Netflix.netflix_caches()


    """
    # ------
    # caches
    # ------

    def test_caches_1 (self):
        r = StringIO("12345:\n57483\n12210\n138849\n")
        w = StringIO()
        Netflix.netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "12345:\n1.0\n1.0\n1.0\nRMSE: 1\n")
        r = StringIO("11:\n25\n83\n97\n")
        w = StringIO()
        Netflix.netflix_load_caches('test-movie_cache.json', 'test-customer_cache.json')

    # ----
    # read
    # ----

    def test_read_1 (self) :
        r    = StringIO("12345:\n57483\n12210\n138849\n")
        customers, movieID, nextMovie = Netflix.netflix_read(r, None)
        self.assertEqual(customers,  ['57483', '12210', '138849'])
        self.assertEqual(movieID, '12345')
        self.assertEqual(nextMovie, None)

    def test_read_2 (self) :
        r    = StringIO("12345:\n57483\n12210\n138849\n54321:\n47383\n73827\n")
        customers, movieID, nextMovie = Netflix.netflix_read(r, None)
        self.assertEqual(customers,  ['57483', '12210', '138849'])
        self.assertEqual(movieID, '12345')
        self.assertEqual(nextMovie, '54321')

    def test_read_3 (self) :
        r    = StringIO("57483\n12210\n138849\n")
        customers, movieID, nextMovie = Netflix.netflix_read(r, '47382')
        self.assertEqual(customers,  ['57483', '12210', '138849'])
        self.assertEqual(movieID, '47382')
        self.assertEqual(nextMovie, None)

    def test_read_4 (self) :
        r    = StringIO("57483\n12210\n138849\n58398:\n")
        customers, movieID, nextMovie = Netflix.netflix_read(r, '47382')
        self.assertEqual(customers,  ['57483', '12210', '138849'])
        self.assertEqual(movieID, '47382')
        self.assertEqual(nextMovie, '58398')

    # ----
    # eval
    # ----

    def test_eval_1 (self) :
        Netflix.netflix_caches()
        v = Netflix.netflix_eval('12582', ['341963', '874390', '1842453', '441381'])
        self.assertEqual(v, [3, 4, 4, 4])

    """

    # -----------
    # getMovieAvg
    # -----------

    def test_getMovieAvg_1 (self) :
        movieAvg = Netflix.netflix_getMovieAvg("107")
        self.assertEqual(movieAvg, 3.3522316043425815)

    def test_getMovieAvg_2 (self) :
        movieAvg = Netflix.netflix_getMovieAvg("8776")
        self.assertEqual(movieAvg, 2.863905325443787)

    # ----------
    # getCustAvg
    # ----------

    def test_custMovieAvg_1 (self) :
        customerAvg = Netflix.netflix_getCustAvg("1611")
        self.assertEqual(customerAvg, 3.74)

    def test_custMovieAvg_2 (self) :
        customerAvg = Netflix.netflix_getCustAvg("5399")
        self.assertEqual(customerAvg, 3.81)


    # -------------
    # getTrueRating
    # -------------

    def test_getTrueRating_1 (self) :
        truth = Netflix.netflix_getTrueRating("12582", ["341963", "874390", "1842453"])
        self.assertEqual(truth, [3, 4, 4])

    def test_getTrueRating_2 (self) :
        truth = Netflix.netflix_getTrueRating("5318", ["2009093", "163151"])
        self.assertEqual(truth, [1, 4])

    def test_getTrueRating_3 (self) :
        truth = Netflix.netflix_getTrueRating("406", ["1989674"])
        self.assertEqual(truth, [2])

    # ------------------
    # netflix_update_sds
    # ------------------

    def test_netflix_update_sds_1 (self) :
        Netflix.sds = 0.0
        Netflix.counter = 0
        Netflix.netflix_update_sds([1, 2, 3], [3, 1, 4])
        self.assertEqual(Netflix.sds, 6)
        self.assertEqual(Netflix.counter, 3)
        Netflix.sds = 0.0
        Netflix.counter = 0

    def test_netflix_update_sds_2 (self) :
        Netflix.sds = 0.0
        Netflix.counter = 0
        Netflix.netflix_update_sds([1, 2, 3], [3, 1, 4])
        self.assertEqual(Netflix.sds, 6)
        self.assertEqual(Netflix.counter, 3)
        Netflix.netflix_update_sds([5, 3, 4], [2, 1, 3])
        self.assertEqual(Netflix.sds, 20)
        self.assertEqual(Netflix.counter, 6)
        Netflix.sds = 0.0
        Netflix.counter = 0

    # -----------
    # algorithm_1
    # -----------

    def test_algorithm_1_a (self):
        predicted = Netflix.netflix_algorithm_1('107', ['1611', '5399'])
        self.assertEqual(predicted, [3.5461158021712906, 3.5811158021712908])    

    def test_algorithm_1_b (self):
        predicted = Netflix.netflix_algorithm_1('8776', ['1611', '5399'])
        self.assertEqual(predicted, [3.3019526627218934, 3.3369526627218935]) 
   

    """
    # -----
    # print
    # -----

    def test_print_1 (self) :
        w = StringIO()
        Netflix.netflix_print(w, '12345', [1.0, 1.0])
        self.assertEqual(w.getvalue(), "12345:\n1.0\n1.0\n")

    def test_print_2 (self) :
        w = StringIO()
        Netflix.netflix_print(w, '12345', [1.0])
        self.assertEqual(w.getvalue(), "12345:\n1.0\n")

    def test_print_3 (self) :
        w = StringIO()
        Netflix.netflix_print(w, '12345', [1.0, 1.0, 1.0])
        self.assertEqual(w.getvalue(), "12345:\n1.0\n1.0\n1.0\n")


    # -----
    # solve
    # -----

    def test_solve_1 (self) :
        r = StringIO("12345:\n57483\n12210\n138849\n")
        w = StringIO()
        Netflix.netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "12345:\n1.0\n1.0\n1.0\nRMSE: 1\n")

    def test_solve_2 (self) :
        r = StringIO("12354:\n57483\n12210\n54321:\n47583\n74837\n")
        w = StringIO()
        Netflix.netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "12354:\n1.0\n1.0\n54321:\n1.0\n1.0\nRMSE: 1\n")
    """
# ----
# main
# ----

main()
