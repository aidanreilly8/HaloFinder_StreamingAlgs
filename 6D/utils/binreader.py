import math 
import sys
import os
import struct
import numpy as np
import pandas as pd
import feather


class binreader:
   
    """
    Initializes a binreader class by opening up one of the binary data files to start reading at (defaults to 0).
    Binary data must be written as pandas data frame with one column using
    feather (as done by write_binary_data.py).
    """
    def __init__(self, file_num=0):
        self.f_num = file_num
        # replace the string here with desired directory of binary data
        self.df = feather.read_dataframe("/srv/ssd/feather_particle_info_with_vel_32/" + str(file_num) + "bin")
        self.curr_idx = 0


    """
    Reads the next num_partilcles worth of information out of binary data files and returns an array of
    this data. If there are notnum_particles number left to be read it just reads the rest and returns an
    array of that size.
    """
    def process(self, num):
        num_particles = num*6 # 6, 2 byte pieces of information for each
        num_processed = 0
        arr = np.zeros(num_particles, dtype=np.int32) 
        arr_idx = 0
        while (num_processed < num_particles):
            end = min(len(self.df['0']), self.curr_idx + num_particles - num_processed)
            arr [arr_idx: arr_idx + end - self.curr_idx]= self.df['0'][self.curr_idx: end]
            num_processed += end - self.curr_idx 
            self.curr_idx = end
            arr_idx = num_processed
            if (num_processed < num_particles):
                if (self.f_num < 511):
                    self.f_num += 1
                    self.curr_idx = 0                    
                    print(self.f_num)
                    # if changing the directory of binary data, it must also be
                    # done here
                    self.df = feather.read_dataframe("/srv/ssd/feather_particle_info_with_vel_32/" + str(self.f_num) + "bin")
                else:
                    return arr[:num_processed]
        return arr
         

if __name__ == "__main__":
    encoder = binreader()
    count = 0
    result = encoder.process(1000000000)
    while (count < 10000000000):
        count += len(result)/6
        result = encoder.process(1000000)
    print("FINISHED PROCESSING {} particles".format(count))
















