import sys
import math
import numpy as np


# This script analyzes the outpit from either exact frequency counts or CS
# frequency counts of 3 and 4 dimensional data combined. It uses the 4D data as velocity
# histograms at each position and searches for two peaks in a single position.
# The file names of the 3D output, and then each of the 4D outputs should be
# given as command line arguments e.g.

#     python find_interesting_cells.py 3D_output.txt 3DandVX_output.py 3DandVY_output.py 3DandVZ_output.py

# This will generate a file that contains a list of interesting positions. Here
# interesting means a single position space with two or more distinct velocity
# peaks in a single velocity direction. An approximate particle count per
# distinct peak will also be given for each of these spots, as well as the
# direction of the split. Note that this also assumes, at least currently, that
# only 2 heavy peaks are found. 

"""
This funciton takes in the name of the 3D output file and returns a list of the
heaviest 100,000 cell positions. 
"""
def position_cell_data(pos_file):
    heavy_cell_posfile = open(pos_file, "r")
    heavy_cells_pos = np.zeros(100000, dtype=np.int32)
    heavy_cell_posfile.readline()
    i = 0
    for line in heavy_cell_posfile:
        inf = line.strip().split(',')
        heavy_cells_pos[i] = int(inf[0])
        weight = int(inf[1])
        i+= 1

    heavy_cell_posfile.close()

    return heavy_cells_pos


"""
This function takes the name of a 4D output file as well as the velocity
direction of this file as a string or char, e.g. 'x' 'y' or 'z'. It returns a
list and two dictionaries. The list is simply a list of positions with multiple
velocity peaks. The first dictionary is of key = position locations that
have multiple peaks and index of the separation point of the two peaks.
The second dictionary is a key value pair (position cell
ID,[velocity histgram]) for all positions.  

"""
def velocity_cell_data(heavy_cells_pos, d):
    #heavy_cell_xfile = open("topk_exact/top100000_new_xvel_20bin.csv", "r")
    heavy_cell_xfile = open("top_tenk_CS/cs_" + d + "vel_100k", "r")
    heavy_cell_xfile.readline()
    heavy_cells_x ={}
    for line in heavy_cell_xfile:
        inf = line.strip().split(',')
        heavy_cells_x[int(inf[0])] = int(inf[1])
    heavy_cell_xfile.close()

    pos_cells_x = {}
    for total_id in heavy_cells_x:
        if (total_id//20) not in pos_cells_x:
            pos_cells_x[total_id//20] = [0]*20
        pos_cells_x[total_id//20][total_id % 20] = heavy_cells_x[total_id]


    collocated_x = {}
    collocated_list = []
    ######## Cluster x_vel_heavy_cells to find collocated halos found#########
    # very simple, if there is something in between two which dips sufficiently,
    # then label it as a double
    for pid in heavy_cells_pos:
        if pid in pos_cells_x: 
            collocated_x[pid] = -1
            for i in range(0,19):
                for j in range(i,20):
                    for t in range(i+1,j):
                        if pos_cells_x[pid][t] < pos_cells_x[pid][i]*(0.9) and \
                        pos_cells_x[pid][t] < pos_cells_x[pid][j]*(0.9):
                            # now search for the true midpoint, which I will
                            # say is just the lowest point between i and j
                            idx = t
                            for q in range(t,j):
                                if pos_cells_x[pid][q] < pos_cells_x[pid][idx]:
                                    idx = q
                            collocated_x[pid] = idx                      
                            break
                    if collocated_x[pid] >= 0:
                        break
                if collocated_x[pid] >=  0:
                    break
            if collocated_x[pid] >= 0:
                collocated_list.append(pid)

    return collocated_list, collocated_x, pos_cells_x



"""
This function finds the particle counts per velocity peak of collocated halos.
It takes the list of collocated position ID's and the dictionary of position
ID's and velocity histogram data for any singular direction. I.e. it takes the 
output of velocity_vell_data. It returns a
dictionay of key value pair (postion ID, [particle count per peak])
"""
def get_particle_counts(collocated_list, idcs, pos_cells_x):
    counts = {}
    for pid in collocated_list:
        idx = idcs[pid]
        count1 = 0
        count2 = 0
        for i in range(0, idx):
            count1 += pos_cells_x[pid][i]
        for i in range(idx, 20):
            count2 += pos_cells_x[pid][i]
        counts[pid] = [count1, count2]
        
    return counts


if __name__ == "__main__":
    #heavy_cells_pos = position_cell_data("topk_exact/top100000_new_pos_only.csv")
    heavy_cells_pos = position_cell_data("top_tenk_CS/cs_pos_100k")
    collocated_x_list, collocated_x_idcs, pos_cells_x = velocity_cell_data(heavy_cells_pos, "x")
    #collocated_y_list, collocated_y_idcs, pos_cells_y = velocity_cell_data(heavy_cells_pos, "y")
    #collocated_z_list, collocated_z_idcs, pos_cells_z = velocity_cell_data(heavy_cells_pos, "z")


    counts_x = get_particle_counts(collocated_x_list, collocated_x_idcs,
                                   pos_cells_x)
    #counts_y = get_particle_counts(collocated_y_list, collocated_y_idcs,
    #                               pos_cells_y)
    #counts_z = get_particle_counts(collocated_z_list, collocated_z_idcs,
    #                               pos_cells_z)

    total_collocated_list = set(collocated_x_list)# | set(collocated_y_list) | set(collocated_z_list)
    

    results = open("results/cs_Xonly_interesting_regions_tenk.csv", "w")
    results.write("position ID, count in first cluster, count in second" +
                    "cluster, velocity direction of seperation\n")
    # Note that we might have duplicated if it is seperable in multiple velocity
    # directions. I am just going to say that we are okay with that
    for pid in total_collocated_list:
        #is it seperatd in the x direction of velocity?
        if pid in collocated_x_list:
            results.write("{},{},{},x\n".format(pid, counts_x[pid][0],
                                                 counts_x[pid][1]))
        #is it seperatd in the y direction of velocity?
        #if pid in collocated_y_list:
        #    results.write("{},{},{},y\n".format(pid, counts_y[pid][0],
        #                                         counts_y[pid][1]))
        #is it seperatd in the z direction of velocity?
        #if pid in collocated_z_list:
        #    results.write("{},{},{},z\n".format(pid, counts_z[pid][0],
        #                                         counts_z[pid][1]))


