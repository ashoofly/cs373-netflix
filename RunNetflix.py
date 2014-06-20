#!/usr/bin/env python3

# ------------------------------
# RunNetflix.py
# Copyright (C) 2014
# Omar Lalani
# Angela Hsu
# ------------------------------

"""
To run the program
    % coverage3 run --branch RunNetflix.py < RunNetflix.in

To obtain coverage of the run:
    % coverage3 report -m

To document the program
    % pydoc -w Netflix
"""

# -------
# imports
# -------

import sys

from Netflix import netflix_solve

# ----
# main
# ----

netflix_solve(sys.stdin, sys.stdout)

"""
% coverage3 run --branch RunNetflix.py < RunNetflix.in > RunNetflix.out



% coverage3 report -m
Name          Stmts   Miss Branch BrMiss  Cover   Missing
---------------------------------------------------------
Netflix         18      0      6      0   100%
RunNetflix       5      0      0      0   100%
---------------------------------------------------------
TOTAL           23      0      6      0   100%
"""