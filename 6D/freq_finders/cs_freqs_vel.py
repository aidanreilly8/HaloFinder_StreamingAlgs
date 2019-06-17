from multiprocessing import Pool, cpu_count, current_process
import math
import sys
sys.path.insert(0, "/home/ivkinnikita/astro6d/py_halo/utils/")
import binreader as br
import numpy as np
import pprint as pp
import torch
from csvec import *

"""This class processes the data, uses Count Sketch, and finds heavy hitters 4D"""
class hh:
        box_size = 500      
        vel_size = 20
        c = 10**3; r = 5; k = 100000

        """
        Initializes an exact heavy hitter finding object. 
        """
        def __init__(self,p):
                self.reader = br.binreader()
                self.cs = CSVec(d, c, r, k)
                self.data = None
                self.device = 'cuda'
                self.p = p

        """
        Iterates through all particle information and gets counts for every
        single cell 
        """
        def count(self):
            num_parts = 10**7
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
                args3 = torch.tensor(np.array([self.data[i*6+(self.p)] for i in\
                                             range(len(self.data)//6)]),\
                                    device=self.device).long()
                

                args1.mul_(500)
                args2.mul_(500*500)
                
                # shift relevant particles into positives
                args3.add_(2000)

                # break 0-4000 velocities into 0 - 20 boxes
                args3.div_(200) 
                                
                keys = (args0.add(args1)).add(args2)
                keys.mul_(20)
                keys.add_(args3)
                # get rid of overly high or low velocities send them all to the
                # cell with key_id = 0
                zeros = torch.zeros(len(args3), device=self.device).long()
                keys = torch.where((args3 < 0), zeros, keys)
                keys = torch.where((args3 > 4000), zeros, keys)
                self.cs.accumulateVec(keys)

                self.data = self.reader.process(num_parts)
                
                      
 
if __name__ == "__main__":
        hh1 = exact_hh(3)
        hh1.count()
        out = open("/srv/scratch1/millennium/exact_cells/cs_xvel_20bin", "w")
        for cell in hh1.cs.getTopk():
            out.write(str(cell[1]) + ',' + str(cell[0]) + '\n')
        out.close()
 
        hh2 = exact_hh(4)
        hh2.count()
        out = open("/srv/scratch1/millennium/exact_cells/cs_yvel_20bin", "w")
        for cell in hh2.cs.getTopk():
            out.write(str(cell[1]) + ',' + str(cell[0]) + '\n')
        out.close()
        
        hh3 = exact_hh(5)
        hh3.count()
        out = open("/srv/scratch1/millennium/exact_cells/cs_zvel_20bin", "w")
        for cell in hh3.cs.gtTopk():
            out.write(str(cell[1]) + ',' + str(cell[0]) + '\n')
        out.close()


