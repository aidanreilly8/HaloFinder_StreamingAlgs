import sys
import math
import numpy as np

'''
This file simply extraxts the top 100,000 cells from the exact frequency finder
data
'''

heavy_cells_file = open("/srv/scratch1/millennium/exact_cells/new_xvel_20bin",
                        "r")
heavy_cells = np.zeros(21*(501**3), dtype=np.int32)
i = 0
for line in heavy_cells_file:
    heavy_cells[i] = int(line.strip())
    i +=1 
heavy_cells_file.close()

heavy_cells *= -1

topk = np.argpartition(heavy_cells, 100000)
heavy_cells *= -1
fout = open("topk_exact/top100000_new_xvel_20bin.csv", "w")
fout.write("cell_id,weight\n")
c = 0
for idx in topk:
    if c >= 100000:
        break
    fout.write("{},{}\n".format(idx,heavy_cells[idx]))
    c += 1

fout.close()

heavy_cells_file = open("/srv/scratch1/millennium/exact_cells/new_yvel_20bin",
                        "r")
heavy_cells = np.zeros(21*(501**3), dtype=np.int32)
i = 0
for line in heavy_cells_file:
    heavy_cells[i] = int(line.strip())
    i +=1 
heavy_cells_file.close()

heavy_cells *= -1

topk = np.argpartition(heavy_cells, 100000)
heavy_cells *= -1
fout = open("topk_exact/top100000_new_yvel_20bin.csv", "w")
fout.write("cell_id,weight\n")
c = 0
for idx in topk:
    if c >= 100000:
        break
    fout.write("{},{}\n".format(idx,heavy_cells[idx]))
    c += 1

fout.close()
del heavy_cells
del topk

heavy_cells_file = open("/srv/scratch1/millennium/exact_cells/new_zvel_20bin",
                        "r")
heavy_cells = np.zeros(21*(501**3), dtype=np.int32)
i = 0
for line in heavy_cells_file:
    heavy_cells[i] = int(line.strip())
    i +=1 
heavy_cells_file.close()

heavy_cells *= -1

topk = np.argpartition(heavy_cells, 100000)
heavy_cells *= -1
fout = open("topk_exact/top100000_new_zvel_20bin.csv", "w")
fout.write("cell_id,weight\n")
c = 0
for idx in topk:
    if c >= 100000:
        break
    fout.write("{},{}\n".format(idx,heavy_cells[idx]))
    c += 1

fout.close()
