import math 
from multiprocessing import Pool, cpu_count, current_process
import sys
sys.path.append('/home/ivkinnikita/astro6d/virgo-python')
import virgo.sims.millennium as mill
import feather
import pandas as pd
import numpy as np

f_read_path = "/srv/scratch1/millennium/snapdir_063/snap_millennium_063."

class byte_encoder:
    def __init__(self, to_bin=True): #, num_threads):
        self.to_bin=to_bin            

    def process(self, file_num):
          f_out = "/srv/ssd/feather_particle_info_with_vel_32/" + str(file_num) + "bin"
          snap = mill.SnapshotFile(f_read_path + str(file_num))
          end = int(snap["Header"].attrs["NumPart_ThisFile"][1])
          data = np.empty(end*6, dtype=np.int32)
          for i in range(0, end):
              for j in range(3):
                      data[i*6 + j] = int(float(snap["PartType1"]["Coordinates"][i][j]))
              for k in range(3):
                      data[i*6 + 3 + k] = int(float(snap["PartType1"]["Velocities"][i][k]))
          
          df = pd.DataFrame(data)
          feather.write_dataframe(df, f_out)
def start_process():
    print("starting:", current_process().name)

if __name__ == "__main__":
    #generate list of read files
    read_files = list(range(0,512))
    encoder = byte_encoder()

    #number of cores to use
    pool_size = cpu_count()
    print("Number of processes:", pool_size)
    pool = Pool(processes=pool_size-2, initializer=start_process)
    pool.map(encoder.process, read_files)

    pool.close()
    pool.join()
