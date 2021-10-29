#!/usr/bin/env python

# importing necessary libraries
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



# defining a function which would return the zscore if standard-deviation is not 0,  else it will return 0
def zscore(row):
    column=list(row.index)
    if row[column[3]]==0:
        return 0
    else:
        return (row[column[1]]-row[column[2]])/row[column[3]]



# merging the case-data with neighbor and state data to get appropriate dataframes
neighbor_week= pd.merge(cases_week,neighbor_week, on=['districtid','weekid'])
neighbor_month= pd.merge(cases_month,neighbor_month, on=['districtid','monthid'])
neighbor_overall= pd.merge(cases_overall,neighbor_overall, on=['districtid','overallid'])

state_week= pd.merge(cases_week,state_week, on=['districtid','weekid'])
state_month= pd.merge(cases_month,state_month, on=['districtid','monthid'])
state_overall= pd.merge(cases_overall,state_overall, on=['districtid','overallid'])



# calculating zscore for each dataframe row by using the zscore() defined above
neighbor_week["neighborhoodzscore"] = neighbor_week.apply(zscore,axis=1)
neighbor_month["neighborhoodzscore"] = neighbor_month.apply(zscore,axis=1)
neighbor_overall["neighborhoodzscore"] = neighbor_overall.apply(zscore,axis=1)
state_week["statezscore"] = state_week.apply(zscore,axis=1)
state_month["statezscore"] = state_month.apply(zscore,axis=1)
state_overall["statezscore"] = state_overall.apply(zscore,axis=1)




# merging the neighbor and state zscore data for each district per week, month and overall
data_week= pd.merge(neighbor_week,state_week,on=["districtid","weekid"],how="inner").round(2)
data_week= data_week[["weekid","neighborhoodzscore","statezscore"]]

data_month= pd.merge(neighbor_month,state_month,on=["districtid","monthid"],how="inner").round(2)
data_month= data_month[["monthid","neighborhoodzscore","statezscore"]]

data_overall= pd.merge(neighbor_overall,state_overall,on=["districtid","overallid"],how="inner").round(2)
data_overall= data_overall[["overallid","neighborhoodzscore","statezscore"]]




# storing the output into zscore-time.csv files
data_week.to_csv("csv-files/zscore-week.csv")
data_month.to_csv("csv-files/zscore-month.csv")
data_overall.to_csv("csv-files/zscore-overall.csv")







