import csv
import re

SEPERATOR = "----------------------------------------------------------------------------------------------------------------------------------"


# Read and parse the volunteers from NYC file
volunteers = [re.sub("\s\s+", " ", line.strip()).split(" ") for line in open("names.txt", "r").readlines()]

# Parse the names as last_first
v_simplified = [v[1] + "_" + v[0] for v in volunteers]

#Ties each name to its index for searching later
v_dict = {v_simplified[i]: i for i in range(len(v_simplified))} 

# Convert to a set for faster searching
volunteers = set(v_simplified) 

# volunteers froms stuy will be stored here
stuy_volunteers = {}

# Parse the list of stuy graduates then check for matches
with open('stuy_graduates.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in reader:
        name =  row[0] + "_" + row[1]
        if name in volunteers:
            print " ".join(name.split("_")[::-1]), row[2]
            stuy_volunteers[v_dict[name]] = (" ".join(name.split("_")[::-1]), row[2])

"""
#Now, get the bios for all the NYC volunteers
big_data = [line.strip() for line in open("data.txt", "r").readlines()]
print len(big_data)
volunteer_num = -1
for i in range(len(big_data)):
    if SEPERATOR in big_data[i]:
        volunteer_num += 1
    if volunteer_num in stuy_volunteers:
        if "-----------------------" in big_data[i]:
            print "\n\n", stuy_volunteers[volunteer_num], volunteer_num, i
        else:
            print big_data[i]
print volunteer_num

"""
