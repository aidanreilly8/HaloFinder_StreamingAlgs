import sys
from priority_dict import priority_dict
import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams.update({'font.size': 22})
#Will open and read the results for find_halos.py
#note that find_halos.py ouputs three lists, the first is true, second mg, third cs
#list is [(item, freq_est), (),...()] sorted worst too best (lowest freq first) 

true_items = set()
true_counts = priority_dict()
#mg_freq = []
#cs_items = set()
#cs_freq = []
curr = ""
#First retrieve top 1000 elements of true most frequent
c = 0
for line in list(open("true_freqs.txt")):
    if c == 1000:
        break
    data = line.strip().split(',')
    true_items.add(data[0])
    if c < 11:
        print(data[0])
    true_counts[data[0]] = data[1]
    c+=1


b_vals = []
recall_points = []
false_pos_points = []
c = 0
cs_items = set()
b = 2
for line in reversed(list(open("CS_t30.txt"))):
    if line[0] == 'b':
        c = 0
        b = int(line.strip()[4:])
        recall = len(cs_items.intersection(true_items))/10
        false_pos = len(cs_items.difference(true_items))/10
        recall_points.append(float(recall))
        false_pos_points.append(float(false_pos))
        b_vals.append(b)
        cs_items.clear()
    elif c < 1000:
        data = line.strip().split(',')
        cs_items.add(data[0])
        c+=1


plt.plot(b_vals, recall_points, 'g')
plt.plot(b_vals, false_pos_points, 'r')
ax = plt.gca()
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)
ax.spines['bottom'].set_position(('data',0))
        #plt.plot(k_vals, plot_array[x], color='red')
        #plt.annotate('$X = $' + str(x) + '$, Y = $' + str(plot_array[x]),
        #     xy=(x, plot_array[x]), xycoords='data',
        #     xytext=(+100, +60), textcoords='offset points', fontsize=32,
        #     arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
ax.set_title('True top item recall (t=10)', fontsize=60)
ax.set_xlabel('b size', fontsize=40)
ax.set_ylabel('recall percentage', fontsize=40)
#plt.ylim(-(max_diff + 5), max_diff + 5)
plt.show()
"""
    if line.strip() in ("brute", "mg", "cs"):
        curr = line.strip()
        next   
    data = (line.strip().strip(')')[1:]).split(',')
    if curr == "brute":
        brute_items.append(data[0])
        brute_freq.append(data[1])
    elif curr == "mg":
        mg_items.append(data[0])
        mg_freq.append(data[1])
    elif curr == "cs":    
        cs_items.append(data[0])
        cs_freq.append(data[1])
    """
