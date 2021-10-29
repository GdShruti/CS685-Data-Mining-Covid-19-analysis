#!/usr/bin/env python

# importing necessary packages
import json
import pandas as pd


# loading necessary files
edge_graph = pd.read_csv("csv-files/edge-graph.csv").set_index("districtid")
cases_week = pd.read_csv("csv-files/cases-week.csv").set_index("districtid")
cases_month =pd.read_csv("csv-files/cases-month.csv").set_index("districtid")
cases_overall = pd.read_csv("csv-files/cases-overall.csv").set_index("districtid")



# caluculating mean and standard deviation of neighbor districts per week

df=edge_graph.join(cases_week,on="neighbor",lsuffix="default").drop('neighbor',axis=1)
df_std = pd.DataFrame(df.groupby(['districtid','weekid']).std().round(2)['cases']).rename(columns={"cases":'neighborstdev'})
df_mean= pd.DataFrame(df.groupby(['districtid','weekid']).mean().round(2)['cases']).rename(columns={"cases":'neighbormean'})
neighbor_week = df_mean.join(df_std)
neighbor_week.to_csv("csv-files/neighbor-week.csv")



# caluculating mean and standard deviation of neighbor districts per month

df=edge_graph.join(cases_month,on="neighbor",lsuffix="default").drop('neighbor',axis=1)
df_std = pd.DataFrame(df.groupby(['districtid','monthid']).std().round(2)['cases']).rename(columns={"cases":'neighborstdev'})
df_mean= pd.DataFrame(df.groupby(['districtid','monthid']).mean().round(2)['cases']).rename(columns={"cases":'neighbormean'})
neighbor_month = df_mean.join(df_std)
neighbor_month.to_csv("csv-files/neighbor-month.csv")



# caluculating overall mean and standard deviation of neighbor districts 

df=edge_graph.join(cases_overall,on="neighbor",lsuffix="default").drop('neighbor',axis=1)
df_std = pd.DataFrame(df.groupby(['districtid','overallid']).std().round(2)['cases']).rename(columns={"cases":'neighborstdev'})
df_mean= pd.DataFrame(df.groupby(['districtid','overallid']).mean().round(2)['cases']).rename(columns={"cases":'neighbormean'})
neighbor_overall = df_mean.join(df_std)
neighbor_overall.to_csv("csv-files/neighbor-overall.csv")



