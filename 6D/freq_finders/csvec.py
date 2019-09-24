import math
import numpy as np
import copy
import torch

LARGEPRIME = 2**61-1
"""
Class which implements the Count Sketch algorithm and data structure. 
"""
class CSVec(object):
    """ Simple Count Sketched Vector """
    def __init__(self, d, c, r, k):
        self.r, self.c, self.d, self.k = r, c, d, k 
        self.device = 'cuda'
        
        # initialize the sketch
        self.table = torch.zeros((r, c), device=self.device)

        torch.random.manual_seed(42)
        self.hashes = torch.randint(0, LARGEPRIME, (r, 6),
                                    dtype=torch.int64, device=self.device)
        #self.topk = torch.zeros((k,2), dtype=torch.int64, device=self.device)       

    """Update the count sketch object with a vector vec of items"""
    def accumulateVec(self, coords):
        #assert(len(vec.size()) == 1 and vec.size()[0] == self.d)
        
        # the rest for not precomputed hashes case 
        h1, h2, h3, h4, h5, h6 = self.hashes[:,0:1], self.hashes[:,1:2],\
                                 self.hashes[:,2:3], self.hashes[:,3:4],\
                                 self.hashes[:,4:5], self.hashes[:,5:6]
        
        #vals = torch.zeros(self.r, vec.size()[0],dtype=torch.int64, device=self.device)#
        for r in range(self.r):
            vec = coords.clone()
            buckets = (vec.mul_(h1[r]).add_(h2[r]) % LARGEPRIME % self.c)
            signs = ((vec.mul_(h3[r]).add_(h4[r]).mul_(vec).add_(h5[r])\
                      .mul_(vec).add_(h6[r])) % LARGEPRIME % 2).float().mul_(2).add_(-1)
            self.table[r,:] += torch.bincount(input=buckets,
                                              weights=signs,
                                              minlength=self.c)

#            vals[r] = self.table[r, buckets] * signs

#        vals = vals.median(dim=0)[0]# this is their estimatesi
#        vals = torch.stack((vals, coords), dim=1)
#        print(self.topk)
#        for val in vals:#
#            in_heap = False
#            for el in self.topk:
#                if el[1] == val[1]:
                    #update existing value
                    #might double count if a lot of the same id are next to
                    #eachother but this should be the same for everything 
#                    el[0] += 1
#                    in_heap = True
#                    break
#            cutoff = torch.argmin(self.topk[:,0])
#            if ((not in_heap) and val[0] > self.topk[cutoff][0]):
#                    self.topk[cutoff] = val
                    
            #self.topk = torch.sort(self.topk, 0, descending=True)[0]

                           
    """Given a vector of items coords, estimate their values based on the Count
    Sketch data structure"""    
    def findValues(self, vec):
        # estimating frequency of input coordinates
        vals = torch.zeros(self.r, vec.size()[0], device=self.device,
                           dtype=torch.int64)
        h1, h2, h3, h4, h5, h6 = self.hashes[:,0:1], self.hashes[:,1:2],\
                                  self.hashes[:,2:3], self.hashes[:,3:4],\
                                  self.hashes[:,4:5], self.hashes[:,5:6]
        for r in range(self.r):
            coords = vec.clone()
            buckets = (coords.mul_(h1[r]).add_(h2[r]) % LARGEPRIME % self.c)
            signs = ((coords.mul_(h3[r]).add_(h4[r]).mul_(coords).add_(h5[r])\
                      .mul_(coords).add_(h6[r])) % LARGEPRIME % 2).float().mul_(2).add_(-1) 
            vals[r] = (self.table[r, buckets]* signs)
        
        # take the median over rows in the sketch
        return vals.median(dim=0)[0]

    """Return the current top k items of count sketch"""
    def getTopk(self, n=(500**3)):
        start = 0
        self.topk = torch.zeros((self.k,2), dtype=torch.int64, device=self.device)
        #all_cells = [t for t in range(500**3)]
        coords = [r for r in range(start, start + self.d)]
        vec = torch.tensor(coords, dtype=torch.int64, device='cuda')
        #coordstmp= coords.clone()
        #estimates = self.findValues(coordstmp)
        #return(torch.stack((estimates, coords)))
        while start <= n:
            #coordstmp = coords.clone()
            estimates = self.findValues(vec)
            estimates = torch.stack((estimates, vec), dim=1)
            estimates = torch.cat((self.topk, estimates), 0)
            sort, ind = torch.sort(estimates, 0, descending=True)
            self.topk = estimates[ind[:self.k,0]]
        #    all_cells[start:start +self.d] = estimates.cpu()
            vec.add_(self.d)
            start += self.d

        return self.topk

