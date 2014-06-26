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
        self.assertEqual(Netflix.cust_ratings_by_decade["378466"], {'1990': 4.348178137651822, 
                                                                    '1980': 4.591304347826087, 
                                                                    '1940': 0, 
                                                                    '1960': 4.769230769230769, 
                                                                    '1970': 4.696969696969697, 
                                                                    '1920': 0, 
                                                                    '2000': 4.423357664233577, 
                                                                    '1930': 0, 
                                                                    '1950': 5.0, 
                                                                    '1910': 0, 
                                                                    '1890': 0, 
                                                                    '1900': 0})
        self.assertEqual(Netflix.movies_by_decade["1990"], 3.617264036843734)
        self.assertEqual(Netflix.movie_info[12582], ('2003', 'Mystic River'))

    def test_caches_2 (self) :
        self.assertEqual(Netflix.movie_stats_cache["5318"], [3.595210220910109, 3.701846691344674, 1.1428533047409748])
        self.assertEqual(Netflix.customer_stats_cache["2009093"], [3.5, 4.0, 1.5811388300841898])
        self.assertEqual(Netflix.answer_cache["5318-2009093"], 1)
        self.assertEqual(Netflix.cust_ratings_by_decade["778283"], {'1990': 3.5369127516778525, 
                                                                    '1980': 3.792452830188679, 
                                                                    '1940': 4.666666666666667, 
                                                                    '1960': 4.4, 
                                                                    '1970': 4.258620689655173, 
                                                                    '1920': 0, 
                                                                    '2000': 3.445273631840796, 
                                                                    '1930': 4.5, 
                                                                    '1950': 4.25, 
                                                                    '1910': 0, 
                                                                    '1890': 0, 
                                                                    '1900': 0})
        self.assertEqual(Netflix.movies_by_decade["2000"], 3.522762354036767)
        self.assertEqual(Netflix.movie_info[5318], ('1995', 'Tommy Boy'))

    def test_caches_3 (self) :
        self.assertEqual(Netflix.movie_stats_cache["406"], [3.7627578830450252, 3.8279188072932406, 0.9271958105755236])
        self.assertEqual(Netflix.customer_stats_cache["1989674"], [3.7689530685920576, 3.954954954954955, 1.11958765680189])
        self.assertEqual(Netflix.answer_cache["406-1989674"], 2)
        self.assertEqual(Netflix.cust_ratings_by_decade["585188"], {'1990': 4.0, 
                                                                    '1980': 5.0, 
                                                                    '1940': 4.0, 
                                                                    '1960': 0, 
                                                                    '1970': 4.0, 
                                                                    '1920': 0, 
                                                                    '2000': 3.5714285714285716, 
                                                                    '1930': 4.333333333333333, 
                                                                    '1950': 4.666666666666667, 
                                                                    '1910': 0, 
                                                                    '1890': 0, 
                                                                    '1900': 0})
        self.assertEqual(Netflix.movies_by_decade["1900"], 2.7889908256880735)
        self.assertEqual(Netflix.movie_info[406], ('2005', 'Hostage'))

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
        self.assertEqual(v, [4.0, 3.6, 4.0])

    def test_eval_2 (self) :
        v = Netflix.netflix_eval('12582', ['341963', '874390', '1842453', '441381'])
        self.assertEqual(v, [4.0, 3.7, 3.6, 4.3])

    def test_eval_3 (self) :
        v = Netflix.netflix_eval('10851', ['2221448', '1703866', '2118663'])
        self.assertEqual(v, [5.0, 3.3, 4.3])

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

    # -----------------------
    # netflix_getCustByDecade
    # -----------------------

    def test_getCustByDecade_1 (self) :
        avgRating = Netflix.netflix_getCustByDecade("378466", 1920)
        self.assertEqual(avgRating, 0)

    def test_getCustByDecade_2 (self) :
        avgRating = Netflix.netflix_getCustByDecade("778283", 1990)
        self.assertEqual(avgRating, 3.5369127516778525)

    def test_getCustByDecade_3 (self) :
        avgRating = Netflix.netflix_getCustByDecade("585188", 1950)
        self.assertEqual(avgRating, 4.666666666666667)

    # ----------------------------
    # netflix_getAvgRatingByDecade
    # ----------------------------

    def test_getAvgRatingByDecade_1 (self) :
        avgRating = Netflix.netflix_getAvgRatingByDecade("1990")
        self.assertEqual(avgRating, 3.617264036843734)

    def test_getAvgRatingByDecade_2 (self) :
        avgRating = Netflix.netflix_getAvgRatingByDecade("2000")
        self.assertEqual(avgRating, 3.522762354036767)

    def test_getAvgRatingByDecade_3 (self) :
        avgRating = Netflix.netflix_getAvgRatingByDecade("1900")
        self.assertEqual(avgRating, 2.7889908256880735)

    # ------------------
    # netflix_print_RMSE
    # ------------------

    def test_print_RMSE_1 (self) :
        w = StringIO()
        Netflix.sds = 6.0
        Netflix.counter = 3
        Netflix.netflix_print_RMSE(w)
        self.assertEqual(w.getvalue(), "RMSE: 1.4142\n")
        Netflix.sds = 0.0
        Netflix.counter = 0

    def test_print_RMSE_2 (self) :
        w = StringIO()
        Netflix.sds = 39.0
        Netflix.counter = 9
        Netflix.netflix_print_RMSE(w)
        self.assertEqual(w.getvalue(), "RMSE: 2.0817\n")
        Netflix.sds = 0.0
        Netflix.counter = 0

    def test_print_RMSE_3 (self) :
        w = StringIO()
        Netflix.sds = 20.0
        Netflix.counter = 6
        Netflix.netflix_print_RMSE(w)
        self.assertEqual(w.getvalue(), "RMSE: 1.8257\n")
        Netflix.sds = 0.0
        Netflix.counter = 0

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

    def test_netflix_update_sds_3 (self) :
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
    # algorithm_7
    # -----------

    def test_algorithm_7_1 (self):
        predicted = Netflix.netflix_algorithm_7('107', ['1611', '5399'])
        self.assertEqual(predicted, [3.6, 3.6])

    def test_algorithm_7_2 (self):
        predicted = Netflix.netflix_algorithm_7('8776', ['1611', '5399'])
        self.assertEqual(predicted, [3.0, 3.1])

    def test_algorithm_7_3 (self):
        predicted = Netflix.netflix_algorithm_7('17770', ['126'])
        self.assertEqual(predicted, [3.6])

    def test_algorithm_7_4 (self):
        predicted = Netflix.netflix_algorithm_7('4794', ['126'])
        self.assertEqual(predicted, [4.1])

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
        self.assertEqual(w.getvalue(), '2043:\n4.0\n3.6\n4.0\nRMSE: 1.6083\n')

    def test_solve_2 (self) :
        r = StringIO("2043:\n1417435\n2312054\n462685\n12582:\n341963\n874390\n1842453\n441381\n")
        w = StringIO()
        Netflix.netflix_solve(r, w)
        self.assertEqual(w.getvalue(), '2043:\n4.0\n3.6\n4.0\n12582:\n4.0\n3.7\n3.6\n4.3\nRMSE: 1.2985\n')

# ----
# main
# ----

main()