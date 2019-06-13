import sys
import math
import numpy as np
'''
This file finds the top 100,000 cells from position only frequency finder data
'''
heavy_cells_file = open("/srv/scratch1/millennium/exact_cells/new_pos_only",
                        "r")
heavy_cells = np.zeros(500**3, dtype=np.int32)
i = 0
for line in heavy_cells_file:
    heavy_cells[i] = int(float(line.strip()))
    i +=1 
heavy_cells_file.close()

heavy_cells *= -1

topk = np.argpartition(heavy_cells, 100000)
heavy_cells *= -1
fout = open("topk_exact/top100000_new_pos_only.csv", "w")
fout.write("cell_id,weight\n")
c = 0
for idx in topk:
    if c >= 100000:
        break
    fout.write("{},{}\n".format(idx,heavy_cells[idx]))
    c += 1

fout.close()

