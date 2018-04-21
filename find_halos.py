import frequent_item_finders
import sys
# Find halos using frequency finders,
# Brute force, Misa Gries, and Count Sketch impemented
k = 1000
#k = 10
t = 480 # approximately log(n/0.05) This is equivalent to r in halo finder paper 
#t = 24
b = 1000000 # equivalent to t in halo finder paper
#b = 100
# arg1 = data file name
# items ordered x,y,z order 
seqFile = open(sys.argv[1], "r")
seqList = []
#Skip over 8 header lines
for _ in range(8):
    seqFile.readline()


# It looks like the range is 500,000. If we assume that the units are in (1/1000)Mpc/h
# Then  will make boxes of side length 1000, and thus have 500^3 boxes, following "Streaming
# Algorithms for Halo Finders"
# I  will then order the boxes in x,y,z order.
#  i.e. label = (z//1000)(250000) + (y//1000)(500) + (x//1000)
# It should then be that (z//1000) = label // 250000
#                        (y//1000) = (label % 250000) // 500 
#                        (x//1000) = label %% 500




def main():
    freqs = {} # true brute force freqs
    mg = frequent_item_finders.MisraGries(k)
    cs = frequent_item_finders.CountSketch(k, t, b)
    #for item in seqList:
        #if item in freqs.keys():
         #   freqs[item] +=1
        #else:
        #    freqs[item] = 1
    # Iterate over input sequence file and return a list of labeled points
    #c = 0
    for line in seqFile:
        #if c == 10000:
            #break
        point = list(map(float,line.strip().strip(";").split(",")))
        label = int(((point[2])//1000)*(250000) + ((point[1])//1000)*(500) + ((point[0])//1000))
        if label in freqs.keys():
            freqs[label] +=1
        else:
            freqs[label] = 1
        mg.process(int(label))
        cs.process(int(label))
        #c+=1
    print("brute")
    for pair in sorted(freqs.items(), key=lambda x: x[1]):
        print(pair)
    print("mg")
    for pair in sorted(mg.most_frequent_items().items(), key=lambda x: x[1]):
        print(pair)
    print("cs")
    for pair in sorted(cs.most_frequent_items().items(), key=lambda x: x[1]):
        print(pair)


if __name__ == "__main__":
    main()

