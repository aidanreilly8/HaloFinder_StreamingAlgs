import frequent_item_finders
import sys
# Find halos using frequency finders,
# Brute force, Misa Gries, and Count Sketch impemented

#k = 10
t = 28 # approximately log(n/0.05) This is equivalent to r in halo finder paper 
#t = 24
b = 1000000 # equivalent to t in halo finder paper
#b = 100
# arg1 = data file name
# items ordered x,y,z order 


# It looks like the range is 500,000. If we assume that the units are in (1/1000)Mpc/h
# Then  will make boxes of side length 1000, and thus have 500^3 boxes, following "Streaming
# Algorithms for Halo Finders"
# I  will then order the boxes in x,y,z order.
#  i.e. label = (z//1000)(250000) + (y//1000)(500) + (x//1000)
# It should then be that (z//1000) = label // 250000
#                        (y//1000) = (label % 250000) // 500 
#                        (x//1000) = label % 500




def main():
    seqFile = open(sys.argv[1], "r")
    outfile = open("MG_processed.txt", "w")
    k = 10000
    #Skip over 8 header lines    
    for _ in range(8):
        seqFile.readline()
    pos = seqFile.tell()
    for i in range(100):  
        seqFile.seek(pos)
        k *= 2

    
        mg = frequent_item_finders.MisraGries(k)
        #cs = frequent_item_finders.CountSketch(k, t, b)
        """
        freqs = {} # true brute force freqs
        for item in seqList:
            if item in freqs.keys():
                freqs[item] +=1
            else:
                freqs[item] = 1
        """
        for line in seqFile:
            point = list(map(float,line.strip().strip(";").split(",")))
            label = int(((point[2])//1000)*(250000) + ((point[1])//1000)*(500) + ((point[0])//1000))
            """if label in freqs.keys():
                freqs[label] +=1
            else:
            freqs[label] = 1"""
            mg.process(int(label))
            #cs.process(int(label))

        """
        print("brute")
        for pair in sorted(freqs.items(), key=lambda x: x[1]):
            print(pair)
        """
        outfile.write('k = {}'.format(k) + '\n')
        for pair in reversed(sorted(mg.most_frequent_items().items(), key=lambda x: x[1])):
            outfile.write(str(pair)[1:-1] + '\n')
        
        """
        print("cs")
        for pair in sorted(cs.most_frequent_items().items(), key=lambda x: x[1]):
           print(pair)
      """
    outfile.close()

if __name__ == "__main__":
    main()

