from multiprocessing import Pool, cpu_count, current_process
import math
import sys
sys.path.insert(0, "/home/ivkinnikita/astro6d/py_halo/utils/")
import binreader as br
import numpy as np
import pprint as pp
import torch
from csvec import *

"""This class processes the data, uses Count Sketch, and finds heavy hitters 3D"""
class hh:
        box_size = 500      
        vel_size = 20

        """
        Initializes an exact heavy hitter finding object. Takes no arguments. 
        """
        def __init__(self, d, c, r, k):
                self.reader = br.binreader()
                self.cs = CSVec(d, c, r, k)
                self.data = None
                self.device = 'cuda'
                self.d = d
                self.c = c
                self.r = r
                self.k = k

        """
        Iterates through all particle information and gets counts for every
        single cell. This method takes no arguments and returns nothing, but
        it populates the member variable self.cs which is a Count Sketch
        object. 
        """
        def count(self):
            num_parts = self.d
            self.data = self.reader.process(num_parts)
            while (len(self.data) > 0):
                args0 = torch.tensor(np.array([self.data[i*6] for i in\
                                             range(len(self.data)//6)]),\
                                     device=self.device).long()
                args1 = torch.tensor(np.array([self.data[i*6+1] for i in\
                                             range(len(self.data)//6)]),\
                                    device=self.device).long()
                args2 = torch.tensor(np.array([self.data[i*6+2] for i in\
                                             range(len(self.data)//6)]),\
                                    device=self.device).long()
                

                args1.mul_(500)
                args2.mul_(500*500)
                
                                
                keys = (args0.add(args1)).add(args2)
                self.cs.accumulateVec(keys)

                self.data = self.reader.process(num_parts)
                
                      
 
if __name__ == "__main__":
        d = 10**5; c = 10**7; r = 20; k = 100000
        hh1 = hh(d,c,r,k)
        hh1.count()
        out = open("/srv/scratch1/millennium/exact_cells/cs_pos_100k", "w")
        for cell in hh1.cs.getTopk():
            out.write(str(int(cell[1])) + ',' + str(int(cell[0])) + '\n')
        out.close()

