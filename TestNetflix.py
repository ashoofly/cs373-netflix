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
from unittest import main, TestCase, mock

from Netflix import netflix_read, netflix_eval, netflix_print, netflix_solve, MOVIE_AVGS, CUSTOMER_AVGS

# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase) :

    def test_netflix_load_caches (self):
        r = StringIO("12345:\n57483\n12210\n138849\n")
        w = StringIO()
        netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "12345:\n1.0\n1.0\n1.0\nRMSE: 1\n")
        r = StringIO("11:\n25\n83\n97\n")
        w = StringIO()
        netflix_load_caches('test-movie_cache.json', 'test-customer_cache.json')

    # ----
    # read
    # ----

    def test_read_1 (self) :
        r    = StringIO("12345:\n57483\n12210\n138849\n")
        customers, movieID, nextMovie = netflix_read(r, None)
        self.assertEqual(customers,  ['57483', '12210', '138849'])
        self.assertEqual(movieID, '12345')
        self.assertEqual(nextMovie, None)

    def test_read_2 (self) :
        r    = StringIO("12345:\n57483\n12210\n138849\n54321:\n47383\n73827\n")
        customers, movieID, nextMovie = netflix_read(r, None)
        self.assertEqual(customers,  ['57483', '12210', '138849'])
        self.assertEqual(movieID, '12345')
        self.assertEqual(nextMovie, '54321')

    def test_read_3 (self) :
        r    = StringIO("57483\n12210\n138849\n")
        customers, movieID, nextMovie = netflix_read(r, '47382')
        self.assertEqual(customers,  ['57483', '12210', '138849'])
        self.assertEqual(movieID, '47382')
        self.assertEqual(nextMovie, None)

    def test_read_4 (self) :
        r    = StringIO("57483\n12210\n138849\n58398:\n")
        customers, movieID, nextMovie = netflix_read(r, '47382')
        self.assertEqual(customers,  ['57483', '12210', '138849'])
        self.assertEqual(movieID, '47382')
        self.assertEqual(nextMovie, '58398')

    # ----
    # eval
    # ----

    def test_eval_1 (self) :
        v = netflix_eval('12345', ['62728', '78193', '28119', '28171'])
        self.assertEqual(v, [1.0]*4)

    # -----
    # print
    # -----

    def test_print_1 (self) :
        w = StringIO()
        netflix_print(w, '12345', [1.0, 1.0])
        self.assertEqual(w.getvalue(), "12345:\n1.0\n1.0\n")

    def test_print_2 (self) :
        w = StringIO()
        netflix_print(w, '12345', [1.0])
        self.assertEqual(w.getvalue(), "12345:\n1.0\n")

    def test_print_3 (self) :
        w = StringIO()
        netflix_print(w, '12345', [1.0, 1.0, 1.0])
        self.assertEqual(w.getvalue(), "12345:\n1.0\n1.0\n1.0\n")



    # -----
    # solve
    # -----

    def test_solve_1 (self) :
        r = StringIO("12345:\n57483\n12210\n138849\n")
        w = StringIO()
        netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "12345:\n1.0\n1.0\n1.0\nRMSE: 1\n")

    def test_solve_2 (self) :
        r = StringIO("12354:\n57483\n12210\n54321:\n47583\n74837\n")
        w = StringIO()
        netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "12354:\n1.0\n1.0\n54321:\n1.0\n1.0\nRMSE: 1\n")

# ----
# main
# ----

main()

"""
% coverage3 run --branch TestNetflix.py
FFFF..F
======================================================================
FAIL: test_eval_1 (__main__.TestNetflix)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "TestNetflix.py", line 47, in test_eval_1
    self.assertEqual(v, 20)
AssertionError: 1 != 20

======================================================================
FAIL: test_eval_2 (__main__.TestNetflix)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "TestNetflix.py", line 51, in test_eval_2
    self.assertEqual(v, 125)
AssertionError: 1 != 125

======================================================================
FAIL: test_eval_3 (__main__.TestNetflix)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "TestNetflix.py", line 55, in test_eval_3
    self.assertEqual(v, 89)
AssertionError: 1 != 89

======================================================================
FAIL: test_eval_4 (__main__.TestNetflix)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "TestNetflix.py", line 59, in test_eval_4
    self.assertEqual(v, 174)
AssertionError: 1 != 174

======================================================================
FAIL: test_solve (__main__.TestNetflix)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "TestNetflix.py", line 78, in test_solve
    self.assertEqual(w.getvalue(), "1 10 20\n100 200 125\n201 210 89\n900 1000 174\n")
AssertionError: '1 10 1\n100 200 1\n201 210 1\n900 1000 1\n' != '1 10 20\n100 200 125\n201 210 89\n900 1000 174\n'
- 1 10 1
?      ^
+ 1 10 20
?      ^^
- 100 200 1
+ 100 200 125
?          ++
- 201 210 1
?         ^
+ 201 210 89
?         ^^
- 900 1000 1
+ 900 1000 174
?           ++


----------------------------------------------------------------------
Ran 7 tests in 0.004s

FAILED (failures=5)



% coverage3 report -m
Name           Stmts   Miss Branch BrMiss  Cover   Missing
----------------------------------------------------------
Netflix          18      0      6      0   100%
TestNetflix      33      1      0      0    97%   86
----------------------------------------------------------
TOTAL            51      1      6      0    98%
"""
