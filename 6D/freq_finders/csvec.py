import math
import numpy as np
import copy
import torch

LARGEPRIME = 2**61-1


class CSVec(object):
    """ Simple Count Sketched Vector """
    def __init__(self, d, c, r, k):
        self.r, self.c, self.d, self.k = r, c, int(d), k 
        self.device = 'cuda'
        
        # initialize the sketch
        self.table = torch.zeros((r, c), device=self.device)

        torch.random.manual_seed(42)
        self.hashes = torch.randint(0, LARGEPRIME, (r, 6),
                                    dtype=torch.int64, device=self.device)
        self.topk = torch.zeros((k, 2), device=self.device)       
    
    def accumulateVec(self, vec):
        # updating the sketch
        assert(len(vec.size()) == 1 and vec.size()[0] == self.d)
        
        # the rest for not precomputed hashes case 
        h1, h2, h3, h4, h5, h6 = self.hashes[:,0:1], self.hashes[:,1:2],\
                                 self.hashes[:,2:3], self.hashes[:,3:4],\
                                 self.hashes[:,4:5], self.hashes[:,5:6]
        
       # vals = torch.zeros(self.r, vec.size()[0], device=self.device)
        for r in range(self.r):
            buckets = (vec.mul_(h1[r]).add_(h2[r]) % LARGEPRIME % self.c)
            signs = ((vec.mul_(h3[r]).add_(h4[r]).mul_(vec).add_(h5[r])\
                      .mul_(vec).add_(h6[r])) % LARGEPRIME % 2).float().mul_(2).add_(-1)
            self.table[r,:] += torch.bincount(input=buckets,
                                              weights=signs,
                                              minlength=self.c)
       #     vals[r] = self.table[r, buckets[coords]] * signs[coords]
       # vals = vals.median(dim=0)[0]
       # cutoff = self.topk[-1, -1] 
       # vals = torch.stack((vec[vals > cutoff], vals[vals > cutoff]), dim=1)
       # if vals.size > 0:
       #    #updated existing values 
       #     for val in vals:
       #         if val[0] in self.topk[:,0]:

       #            
       #            = torch.cat((self.topk, vals), dim=0)
       #    #update the queue
       #    vals = torch.cat((self.topk, vals), dim=0)
       #    torch.sort()

        
    def findValues(self, coords):
        # estimating frequency of input coordinates
        vals = torch.zeros(self.r, coords.size()[0], device=self.device)
        h1, h2, h3, h4, h5, h6 = self.hashes[:,0:1], self.hashes[:,1:2],\
                                  self.hashes[:,2:3], self.hashes[:,3:4],\
                                  self.hashes[:,4:5], self.hashes[:,5:6]
        for r in range(self.r):
            buckets = (coords.mul_(h1[r]).add_(h2[r]) % LARGEPRIME % self.c)
            signs = ((coords.mul_(h3[r]).add_(h4[r]).mul_(coords).add_(h5[r])\
                      .mul_(coords).add_(h6[r])) % LARGEPRIME % 2).float().mul_(2).add_(-1) 
            vals[r] = (self.table[r, buckets]* signs)
        
        # take the median over rows in the sketch
        return vals.median(dim=0)[0]
