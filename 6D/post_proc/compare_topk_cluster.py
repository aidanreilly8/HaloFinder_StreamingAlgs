import sys
import math
import numpy as np
"""This script analyzes the outpit from either exact frequency counts or CS
frequency counts of 3 and 4 dimensional data. It used the 4D data as velocity
histograms at each position and searches for two peaks in a single position. """

#######populate date for to 100k halos from SUBFIND#################
def true_halo_data():
    true_halo_file = open("../../../Top100000SubHalos_subIDs_63_halfmassradius.csv", "r")
    true_halos = {}
    true_halo_file.readline()
    for line in true_halo_file:
        info = line.strip().split(',')
        x = int(float(info[3]))
        y = int(float(info[4])) 
        z = int(float(info[5]))
        pid = x + y*500 + z*500*500
        if pid in true_halos:
            true_halos[pid].append(info[2])
        else:
            true_halos[pid] = [info[2]]

    collocated_halos = []
    for pid in true_halos:
        if len(true_halos[pid]) > 1:
            collocated_halos.append(pid)

    true_halo_file.close()
    return true_halos, collocated_halos
##############################################################


#####populate data for heavy cells without velocity info#########
def position_cell_data(true_halos):
    heavy_cell_posfile = open("topk_exact/top100000_new_pos_only.csv", "r")
    heavy_cells_pos = np.zeros(100000, dtype=np.int32)
    heavy_cell_posfile.readline()
    i = 0
    for line in heavy_cell_posfile:
        inf = line.strip().split(',')
        heavy_cells_pos[i] = int(inf[0])
        weight = int(inf[1])
        i+= 1

    heavy_cell_posfile.close()

    accuracy_pos = 0
    for pid in true_halos:
        if pid in heavy_cells_pos:
            accuracy_pos +=1
    print("Number of halos picked up by heavy cells / number of true halos: {} /  \
      {}".format(accuracy_pos,len(true_halos)))
    return heavy_cells_pos
######################################################################


#####populate data for heavvy cells with x velocity info##############
def velocity_cell_data(true_halos, heavy_cells_pos, d):
    heavy_cell_xfile = open("topk_exact/top100000_new_" + d + "vel_20bin.csv", "r")
    heavy_cells_x ={}
    heavy_cell_xfile.readline()
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
    num_not_in_vel = 0
    num_not_in_true_halos = 0
    for pid in heavy_cells_pos:
        if pid not in pos_cells_x:
            num_not_in_vel +=1 
        if pid not in true_halos:
            num_not_in_true_halos += 1
        if pid in pos_cells_x and pid in true_halos:
            collocated_x[pid] = 1
            for i in range(0,19):
                for j in range(i,20):
                    for t in range(i+1,j):
                        if pos_cells_x[pid][t] < pos_cells_x[pid][i]*(0.9) and \
                        pos_cells_x[pid][t] < pos_cells_x[pid][j]*(0.9):
                            collocated_x[pid] = 2                      
                            break
                    if collocated_x[pid] == 2:
                        break
                if collocated_x[pid] == 2:
                    break
            if collocated_x[pid] == 2:
                collocated_list.append(pid)

    print("num not in " + d + " vel space: {}".format(num_not_in_vel))
    print("num not in true halos: {}".format(num_not_in_true_halos))
    return collocated_x,collocated_list


##########################################################################



if __name__ == "__main__":
   
    true_halos, collocated_halos = true_halo_data()
    heavy_cells_pos = position_cell_data(true_halos)
    collocated_x, collocated_x_list = velocity_cell_data(true_halos, heavy_cells_pos, "x")
    collocated_y, collocated_y_list = velocity_cell_data(true_halos, heavy_cells_pos, "y")
    collocated_z, collocated_z_list = velocity_cell_data(true_halos, heavy_cells_pos, "z")



    num_true_collocated_found = 0
    found = []
    not_found = []
    for hid in collocated_halos:
        if hid in collocated_x and hid in heavy_cells_pos and collocated_x[hid] > 1:
            num_true_collocated_found += 1
            found.append(hid)
        elif hid in collocated_y and hid in heavy_cells_pos and collocated_y[hid] > 1:
            num_true_collocated_found += 1
            found.append(hid)
        elif hid in collocated_z and hid in heavy_cells_pos and collocated_z[hid] > 1:
            num_true_collocated_found += 1
            found.append(hid)
        else:
            not_found.append(hid)

    total_collocated_list = set(collocated_x_list) | set(collocated_y_list) | set(collocated_z_list)
    false_positives = total_collocated_list.difference(set(found))
    
    fpFile = open("results_cuts/new_False_positives_dip0.9_cuts.csv", "w")
    fpFile.write("cell ID of overlaps identified by us, and not by SUBFIND " + \
                 "(i.e. false positives)\n")
    for fp in false_positives:
        fpFile.write("{}\n".format(fp))
    fpFile.close()

    tpFile = open("results_cuts/new_True_positives_dip0.9_cuts.csv", "w")
    tpFile.write("cell ID of overlaps identified by us as well as by SUBFIND "+\
            "(i.e. true positives)\n")
    for tp in found:
        tpFile.write("{}\n".format(tp))
    tpFile.close()

    fnFile = open("results_cuts/new_False_Negatives_dip0.9_cuts.csv", "w")
    fnFile.write("cell ID of overlaps identified by SUBFIND but not us "+\
            "(i.e. false negatives)\n")
    for fn in not_found:
        fnFile.write("{}\n".format(fn))
    fnFile.close()


    #overlapping = open("results/5bins.csv", "w")
    #ovelapping.write("Number of overlapping halos in the top 100000 from SUBFIND:
    #                 {}".format(len(collocated_halos)))
    print("Number of overlapping halos in the top 100000 from SUBFIND: {}".format(len(collocated_halos)))
    print("Number of true overlaps found: {}".format(num_true_collocated_found))
    print("found: {}".format(found[10:15]))
    print("not found :{}".format(not_found[10:15]))
   # might be doubled up, should take union of this later
    print("Total collocated halos found: {}".format(len(total_collocated_list)))
    #print("False positive rate: {}".format((num_collocated -\
    #                                        num_true_collocated_found)/num_collocated))

    tmp = []
    for el in collocated_x:
        if collocated_x[el] > 1 and el not in collocated_halos and el in  heavy_cells_pos and el in true_halos:
            tmp.append(el)
    print("x false positives: {}".format(tmp[10:15]))
    tmp = []
    for el in collocated_y:
        if collocated_y[el] > 1 and el not in collocated_halos and el in  heavy_cells_pos and el in true_halos:
            tmp.append(el)
    print("y false positives: {}".format(tmp[10:15]))







