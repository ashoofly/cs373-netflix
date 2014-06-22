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

    def test_caches_1 (self) :
    	self.assertEqual(Netflix.movie_stats_cache["12582"], [3.861750254033212, 3.954606433095186, 0.9326874144951447])
    	self.assertEqual(Netflix.customer_stats_cache["341963"], [3.648, 3.7625, 1.0899981651360704])
    	self.assertEqual(Netflix.answer_cache["12582-341963"], 3)

    def test_caches_2 (self) :
    	self.assertEqual(Netflix.movie_stats_cache["5318"], [3.595210220910109, 3.701846691344674, 1.1428533047409748])
    	self.assertEqual(Netflix.customer_stats_cache["2009093"], [3.5, 4.0, 1.5811388300841898])
    	self.assertEqual(Netflix.answer_cache["5318-2009093"], 1)

    def test_caches_3 (self) :
    	self.assertEqual(Netflix.movie_stats_cache["406"], [3.7627578830450252, 3.8279188072932406, 0.9271958105755236])
    	self.assertEqual(Netflix.customer_stats_cache["1989674"], [3.7689530685920576, 3.954954954954955, 1.11958765680189])
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
        self.assertEqual(v, [3.64324048327134, 4.117403851389367, 3.7850349544635087])

    def test_eval_2 (self) :
        v = Netflix.netflix_eval('12582', ['341963', '874390', '1842453', '441381'])
        self.assertEqual(v, [3.7548751270166063, 3.705875127016606, 3.6150856533323954, 3.5975417936832725])

    def test_eval_3 (self) :
        v = Netflix.netflix_eval('10851', ['2221448', '1703866', '2118663'])
        self.assertEqual(v, [4.066092919115589, 3.6772040302267, 3.9512214974756086])

    # -------------
    # getMovieStats
    # -------------

    def test_getMovieStats_1 (self) :
        movieStats = Netflix.netflix_getMovieStats("107")
        self.assertEqual(movieStats, [3.3522316043425815, 3.5022522522522523, 1.3046952287665436])

    def test_getMovieStats_2 (self) :
        movieStats = Netflix.netflix_getMovieStats("8776")
        self.assertEqual(movieStats, [2.863905325443787, 2.8923076923076922, 1.1037049560865362])

    def test_getMovieStats_3 (self) :
        movieStats = Netflix.netflix_getMovieStats("17770")
        self.assertEqual(movieStats, [2.816503800217155, 2.8611764705882354, 0.9308263652788644])

    # ------------
    # getCustStats
    # ------------

    def test_getCustStats_1 (self) :
        customerStats = Netflix.netflix_getCustStats("1611")
        self.assertEqual(customerStats, [3.7356746765249538, 3.806547619047619, 1.0488982678195617])

    def test_getCustStats_2 (self) :
        customerStats = Netflix.netflix_getCustStats("5399")
        self.assertEqual(customerStats, [3.8123107971745713, 3.9498327759197323, 1.0981544963966021])

    def test_getCustStats_3 (self) :
        customerStats = Netflix.netflix_getCustStats("126")
        self.assertEqual(customerStats, [4.673469387755102, 4.871794871794872, 0.7663258512456566])


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
        self.assertEqual(predicted, [3.543953140433768, 3.5822712007585764])

    def test_algorithm_1_b (self):
        predicted = Netflix.netflix_algorithm_1('8776', ['1611', '5399'])
        self.assertEqual(predicted, [3.2997900009843706, 3.338108061309179])

    def test_algorithm_1_c (self):
        predicted = Netflix.netflix_algorithm_1('17770', ['126'])
        self.assertEqual(predicted, [3.7449865939861287])

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
        r = StringIO("2043:\n1417435\n2312054\n462685\n")
        w = StringIO()
        Netflix.netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "2043:\n3.6\n4.1\n3.8\nRMSE: 1.84\n")

    def test_solve_2 (self) :
        r = StringIO("2043:\n1417435\n2312054\n462685\n12582:\n341963\n874390\n1842453\n441381\n")
        w = StringIO()
        Netflix.netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "2043:\n3.6\n4.1\n3.8\n12582:\n3.8\n3.7\n3.6\n3.6\nRMSE: 1.46\n")

# ----
# main
# ----

main()