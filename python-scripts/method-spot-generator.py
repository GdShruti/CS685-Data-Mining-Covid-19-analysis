#!/usr/bin/env python

# importing necessary packages
import json
import pandas as pd


# loading required files
cases_week = pd.read_csv("csv-files/cases-week.csv").set_index("districtid")
cases_month =pd.read_csv("csv-files/cases-month.csv").set_index("districtid")
cases_overall = pd.read_csv("csv-files/cases-overall.csv").set_index("districtid")

state_week = pd.read_csv("csv-files/state-week.csv").set_index("districtid")
state_month =pd.read_csv("csv-files/state-month.csv").set_index("districtid")
state_overall = pd.read_csv("csv-files/state-overall.csv").set_index("districtid")

neighbor_week = pd.read_csv("csv-files/neighbor-week.csv").set_index("districtid")
neighbor_month =pd.read_csv("csv-files/neighbor-month.csv").set_index("districtid")
neighbor_overall = pd.read_csv("csv-files/neighbor-overall.csv").set_index("districtid")



# merging case-time data with state-time and neighbor-time data
neighbor_week= pd.merge(cases_week,neighbor_week, on=['districtid','weekid'])
neighbor_month= pd.merge(cases_month,neighbor_month, on=['districtid','monthid'])
neighbor_overall= pd.merge(cases_overall,neighbor_overall, on=['districtid','overallid'])

state_week= pd.merge(cases_week,state_week, on=['districtid','weekid'])
state_month= pd.merge(cases_month,state_month, on=['districtid','monthid'])
state_overall= pd.merge(cases_overall,state_overall, on=['districtid','overallid'])



# defining functions for finding out whether the given district is a hotspot, coldspot or none in the given time period  
def check_spot(row):
    columns= list(row.index)
    cases =row[columns[1]]
    hot= row[columns[2]] + row[columns[3]]
    cold = row[columns[2]] - row[columns[3]]
    if cases >hot:
        return "hotspot"
    elif cases<cold:
        return "coldspot"
        

def find_spot(data , method , timeid):
    data['spot'] = data.apply(check_spot,axis=1)
    data['method'] = [method] * len(data)
    data = data[[timeid, "spot", "method"]].reset_index().sort_values([timeid,"districtid"]).set_index(timeid)
    return data




# calculating the required data 
neighbor_week = find_spot(neighbor_week , "neighborhood","weekid")
neighbor_week.to_csv("csv-files/neighborhood-spot-week.csv")


neighbor_month = find_spot(neighbor_month , "neighborhood","monthid")
neighbor_month.to_csv("csv-files/neighborhood-spot-month.csv")


neighbor_overall = find_spot(neighbor_overall , "neighborhood","overallid")
neighbor_overall.to_csv("csv-files/neighborhood-spot-overall.csv")


state_week =find_spot(state_week , "state","weekid")
state_week.to_csv("csv-files/state-spot-week.csv")


state_month = find_spot(state_month , "state","monthid")
state_month.to_csv("csv-files/state-spot-month.csv")


state_overall = find_spot(state_overall , "state","overallid")
state_overall.to_csv("csv-files/state-spot-overall.csv")


