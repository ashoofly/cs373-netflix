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

    # ------
    # caches
    # ------

    def test_cache_1 (self) :
        self.assertEqual(Netflix.answer_cache["12582-341963"], 3)

    def test_cache_2 (self) :
        self.assertEqual(Netflix.answer_cache["5318-2009093"], 1)

    def test_cache_3 (self) :
        self.assertEqual(Netflix.answer_cache["406-1989674"], 2)

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
        v = Netflix.netflix_eval('2043', ['1417435', '2312054', '462685'])
        self.assertEqual(v, [3.643832422817939, 4.118832422817939, 3.783832422817939])

    def test_eval_2 (self) :
        v = Netflix.netflix_eval('12582', ['341963', '874390', '1842453', '441381'])
        self.assertEqual(v, [3.7558751270166058, 3.705875127016606, 3.615875127016606, 3.595875127016606])

    def test_eval_3 (self) :
        v = Netflix.netflix_eval('10851', ['2221448', '1703866', '2118663'])
        self.assertEqual(v, [4.0672040302267005, 3.6772040302267, 3.9522040302267003])

    # -----------
    # getMovieAvg
    # -----------

    def test_getMovieAvg_1 (self) :
        movieAvg = Netflix.netflix_getMovieAvg("107")
        self.assertEqual(movieAvg, 3.3522316043425815)

    def test_getMovieAvg_2 (self) :
        movieAvg = Netflix.netflix_getMovieAvg("8776")
        self.assertEqual(movieAvg, 2.863905325443787)

    def test_getMovieAvg_3 (self) :
        movieAvg = Netflix.netflix_getMovieAvg("17770")
        self.assertEqual(movieAvg, 2.816503800217155)

    # ----------
    # getCustAvg
    # ----------

    def test_custMovieAvg_1 (self) :
        customerAvg = Netflix.netflix_getCustAvg("1611")
        self.assertEqual(customerAvg, 3.74)

    def test_custMovieAvg_2 (self) :
        customerAvg = Netflix.netflix_getCustAvg("5399")
        self.assertEqual(customerAvg, 3.81)

    def test_custMovieAvg_3 (self) :
        customerAvg = Netflix.netflix_getCustAvg("126")
        self.assertEqual(customerAvg, 4.67)


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

    def test_netflix_update_sds_2 (self) :
        Netflix.sds = 0.0
        Netflix.counter = 0
        Netflix.netflix_update_sds([1, 2, 3], [3, 1, 4])
        self.assertEqual(Netflix.sds, 6)
        self.assertEqual(Netflix.counter, 3)
        Netflix.netflix_update_sds([5, 3, 4], [2, 1, 3])
        self.assertEqual(Netflix.sds, 20)
        self.assertEqual(Netflix.counter, 6)
        Netflix.netflix_update_sds([3, 2, 1], [4, 5, 4])
        self.assertEqual(Netflix.sds, 39)
        self.assertEqual(Netflix.counter, 9)
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

    def test_algorithm_1_c (self):
        predicted = Netflix.netflix_algorithm_1('17770', ['126'])
        self.assertEqual(predicted, [3.743251900108578])

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

# ----
# main
# ----

main()