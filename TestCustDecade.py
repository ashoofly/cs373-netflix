#!/usr/bin/env python3

import unittest
import CustByDecadeCache as dcache
import json

'''Test dependencies:
Sample files currently located in 'test_files' directory: 
mv_0000076.txt  1952
mv_0004234.txt  1989
mv_0000358.txt  1979
mv_0000001.txt  2003
mv_0000024.txt  1981
mv_0000544.txt  1987 *not currently used
mv_0000131.txt  2002

'''

class TestDecadeCache(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        dcache.load_movie_info()

    def test1_update_customer_ratings(self):
        dcache.Customers = {}
        movie_file = 'mv_0000076.txt'  # 1952: I Love Lucy
        dcache.update_customer_ratings(movie_file)
        self.assertEqual(dcache.Customers['1527030'][1950], [1])
        self.assertEqual(dcache.Customers['622194'][1950], [5])
        self.assertEqual(dcache.Customers['1780909'][1950], [3])

    def test2_update_customer_ratings(self):
        '''Adding to already populated Customers dictionary.'''
        movie_file = 'mv_0004234.txt' #1989: As Tears Go By        
        dcache.update_customer_ratings(movie_file)
        # maintain past listings
        self.assertEqual(dcache.Customers['1527030'][1950], [1])
        self.assertEqual(dcache.Customers['622194'][1950], [5])
        self.assertEqual(dcache.Customers['1780909'][1950], [3])
        # added new ones
        self.assertEqual(dcache.Customers['769'][1980], [4])
        self.assertEqual(dcache.Customers['1037088'][1980], [1])
        self.assertEqual(dcache.Customers['1405978'][1980], [5])

    def test3_update_customer_ratings(self):
        '''Adding to same customer, same decade'''
        movie_file = 'mv_0000024.txt' #1981: My Bloody Valentine
        dcache.update_customer_ratings(movie_file)
        # maintain past listings
        self.assertEqual(dcache.Customers['1527030'][1950], [1])
        self.assertEqual(dcache.Customers['622194'][1950], [5])
        self.assertEqual(dcache.Customers['1780909'][1950], [3])
        
        # modify existing entries
        self.assertEqual(dcache.Customers['769'][1980], [4,2])
        self.assertEqual(dcache.Customers['1037088'][1980], [1,4])
        self.assertEqual(dcache.Customers['1405978'][1980], [5,2])

        # added new entries
        self.assertEqual(dcache.Customers['134211'][1980], [1])
        self.assertEqual(dcache.Customers['67224'][1980], [3])
        self.assertEqual(dcache.Customers['774432'][1980], [5])

    def test4_calculate_decade_avgs(self):
        '''Make sure decades avg out'''
        movie_file = 'mv_0000001.txt' #2004: Dinosaur Planet
        dcache.update_customer_ratings(movie_file)
        movie_file = 'mv_0000131.txt' #2002: Arachnid
        dcache.update_customer_ratings(movie_file)

        dcache.calculate_decade_avgs()
       
        self.assertEqual(dcache.Customers['769'][1980], 3.0)
        self.assertEqual(dcache.Customers['1037088'][1980], 2.5)
        self.assertEqual(dcache.Customers['1405978'][1980], 3.5)
        self.assertEqual(dcache.Customers['1488844'][2000], 2.5)
        self.assertEqual(dcache.Customers['893988'][2000], 3.5)        

    def test5_update_customer_ratings(self):
        movie_file = '/u/downing/cs/netflix/training_set/mv_0004388.txt'
        dcache.update_customer_ratings(movie_file) 
    
    def test6_length_of_cache(self):
        cache = 'cust_by_decade.json'
        with open(cache, 'r') as f:
            dictionary = json.load(f)
        self.assertEqual(len(dictionary), 480189)




unittest.main()
        
