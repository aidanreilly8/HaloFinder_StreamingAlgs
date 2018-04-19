# Class which creates a Misra Gries sketch and another with Count Sketch

#NOTE: Maybe switch to using a min heap in count sketch??
import sys
sys.path.insert(0, '~/Documents/halo_finder_research/PyHashFamily/')
from PyHashFamily.HashFamily import HashFamily
import random
import statistics

class MisraGries(object):
    def __init__(self, k):
        self.A = {}
        self.k = k 
        self.total_viewed = 0

    def process(self, item):
        self.total_viewed += 1
        if item in self.A.keys():
            self.A[item] += 1
        elif len(self.A.keys()) < self.k - 1:
            self.A[item] = 1
        else:
            keys_to_del = []
            for key in self.A.keys():
                self.A[key] -= 1
                if self.A[key] < 1:
                    keys_to_del.append(key)
            for key in keys_to_del:
                del self.A[key]
                #self.A = {k : (v - 1) for k, v in self.A.items() if v > 1} #just decrement don't copy
            

    def estimate(self, item):
        """ Return the estimation of the frequncy of _item """
        return self.A[item] if item in self.A.keys() else 0
    
    def most_frequent_items(self):
        return self.A





class CountSketch(object):
    # t hash functions (h1, ... , ht) to {1,...,b}
    # t hash function (s1, ... , st) from {-1, 1}
    # t x b array of counters (count sketch), interpreted as an array of t hash tables, each containing b buckets
    def __init__(self, k, t, b):
        self.A = {} # heap of top k elemenets so far 
        self.k = k
        self.t = t
        self.b = b
        # h_hashes is a family of t hashes from an item to {1,...,b}
        self.h_hashes = HashFamily(self.t, self.b)
        # s_hashes is a family of t hashes from an item to {+1,-1}
        self.s_hashes = HashFamily(self.t, 2)
        self.count_sketch = [[0 for i in range(self.b)] for j in range(self.t)]

    def add(self, item):
        for i in range(self.t):
            c = 1
            if self.s_hashes.evalFunction(item, i) == 0:
                c = -1
            idx = self.h_hashes.evalFunction(item,i)
            self.count_sketch[i][idx] += c
    
    def estimate(self, item):
        est_list = []
        for i in range(self.t):
            sign = 1
            if self.s_hashes.evalFunction(item, i) == 0:
                sign = -1
            idx = self.h_hashes.evalFunction(item,i)   
            est_list.append((self.count_sketch[i][idx]) * sign)

        return statistics.median(est_list) 

    def process(self, item):
        self.add(item)
        if item in self.A.keys():
            self.A[item] += 1
        elif len(self.A.keys()) < self.k:
            self.A[item] = self.estimate(item)
        else:
            est = self.estimate(item)
            min_freq_item = min(self.A.items(), key=lambda x: x[1])[0]
            if est > self.A[min_freq_item]:
                del self.A[min_freq_item]
                self.A[item] = est

    def most_frequent_items(self):
        return self.A
  


"""
import hashlib

#Old, trying to use hashlib

class CountSketch(object):
    def __init__(self, k, t, b):
        self.A = {}
        self.k = k
        self.t = t
        self.b = b
        # h_hashes[i] hashes from an item to {1,...,b}
        self.h_hashes= []
        # s_hashes[i] hashes from an item to {+1,-1}
        self.s_hashes = []
        self.count_sketch = [[0 for i in range(self.b)] for j in range(self.t)]
        for _ in range(self.t):
            self.h_hashes.append(hashlib.sha1())
            self.s_hashes.append(hashlib.sha1())

    def add(self, item):
        for i in range(self.t):
            c = 1
            if s_hashes[i].update(item).digest()%2 == 0:
                c = -1
            self.count_sketch[h_hashes[i].update(item).digest()%self.b] += c
    
    def estimate(self, item):
        est_list = []
        for i in range(self.t):
            sign = 1
            if s_hashes[i].update(item).digest()%2 == 0:
                sign = -1
            est_list.append((self.h_hashes[i].update(item).digest() % self.b) * sign)

        return statistics.median(est_list)

    def process(self, item):
        self.add(item)
        if item in self.A.keys():
            self.A[item] += 1
        else:
            est = self.estimate(item)
            min_freq_item = min(d.items(), key=lambda x: x[1])[0]
            if est < self.A[min_freq_item]:
                del self.A[min_freq_item]
                self.A[item] = est

"""


