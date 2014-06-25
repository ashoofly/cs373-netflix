#!/usr/bin/env python3
import random

probe_text = '/u/downing/cs/netflix/probe.txt'


def read_probe_txt(movieID, probe_data):
    if not movieID:
        movieID = r.readline()[:-2]
    probe_data[movieID] = []
    line = r.readline()
    while ':' not in line:
        # customer ID
        probe_data[movieID].append(line.rstrip())
        line = r.readline()
        if line == "":
            return None, probe_data
    next_movie = line[:-2]
    return next_movie, probe_data


movie_ID = None
probe_data = {}
with open(probe_text, 'r') as r:
    while True:
        next_movie, probe_data = read_probe_txt(movie_ID, probe_data)
        if next_movie:
            movie_ID = next_movie
        else:
            break


# choose random movie ID
# Choose random number of customers from movie ID up to length of customer list
# up until 1 thousand lines

max_lines = 1010
line_count = 0
movie_count = 0
with open('RunNetflix.in', 'w') as w:
    random_movie_list = random.sample(list(probe_data.keys()), max_lines)
    while line_count < max_lines: 
        random_movie = random_movie_list[movie_count]
        w.write(random_movie + ":\n")
        num_customers = random.randint(1, len(probe_data[random_movie]))
        random_customers = random.sample(probe_data[random_movie], num_customers)
        for i in random_customers:
            w.write(i + "\n")
        line_count += num_customers + 1
        movie_count += 1
