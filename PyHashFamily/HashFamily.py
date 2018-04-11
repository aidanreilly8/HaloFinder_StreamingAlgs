from random import random

#I think that family size i the number of hash functions I want, and range is the range of each one
#So I probably need to make two hash family classes for CountSketch
class HashFamily(object):
    def __init__(self, hashFamilySize, hrange):
        self.familySize = hashFamilySize
        self.n = hrange
        self.aParams = []
        self.bParams = []
        self.primeNumber = 6700417#39916801


        for i in range(self.familySize):
            self.aParams.append(random() % self.primeNumber)
            self.bParams.append(random() % self.primeNumber)

    def evalFunction(self, x, iFunction):
        return int(((self.aParams[iFunction] * x + self.bParams[iFunction]) % self.primeNumber) % self.n)
   

#NTS: I think iFunction will be the hash function I need to create