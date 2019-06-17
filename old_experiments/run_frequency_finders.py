import frequent_item_finders
import sys
# tests frequency finders, arg1 = k, arg2= t, arg3 = b, arg4 = filename
seqFile = open(sys.argv[4], "r")
seqList = []
# Iterate over input sequence file and return a list of space, tab, or new line delimited elements
for line in seqFile:
    data = line.strip().split()
    seqList.extend(data)

freqs = {}
def main():
    mg = frequent_item_finders.MisraGries(int(sys.argv[1]))
    cs = frequent_item_finders.CountSketch(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    for item in seqList:
        if item in freqs.keys():
            freqs[item] +=1
        else:
            freqs[item] = 1
        mg.process(int(item))
        cs.process(int(item))
    print(sorted(freqs.items(), key=lambda x: x[1]))
    print(sorted(mg.most_frequent_items().items(), key=lambda x: x[1]))
    print(sorted(cs.most_frequent_items().items(), key=lambda x: x[1]))


if __name__ == "__main__":
    main()

