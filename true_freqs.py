import sys

#skip header
data_file = open("data.csv", "r")
for _ in range(8):
    data_file.readline()

freqs = {} # true frequencies of boxes {box: freq}
for line in data_file:
    point = list(map(float,line.strip().strip(";").split(",")))
    label = int(((point[2])//1000)*(250000) + ((point[1])//1000)*(500) + ((point[0])//1000))
    if label in freqs.keys():
        freqs[label] +=1
    else:
        freqs[label] = 1

for pair in reversed(sorted(freqs.items(), key=lambda x: x[1])):
    print(str(pair)[1:-1])