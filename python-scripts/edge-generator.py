#!/usr/bin/env python

# importing necessary packages
import json
import pandas as pd


# loading necessary files
neighbor_mod = json.load(open(r"neighbor-districts-modified.json"))



# creating a list of edges
q=[]
for x in neighbor_mod:
    for n in neighbor_mod[x]['neighbors']:
        q.append((neighbor_mod[x]['id'] , neighbor_mod[n]['id']))


# output is stored in edge-graph.csv
csv=pd.DataFrame(q,columns=["districtid","neighbor"])
csv=csv.sort_values(["districtid","neighbor"])
csv=csv.set_index("districtid")
csv.to_csv("csv-files/edge-graph.csv")



