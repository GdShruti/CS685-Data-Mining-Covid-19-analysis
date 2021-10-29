#!/usr/bin/env python

# importing necessary packages
import json
import pandas as pd


# loading required files
neighbor_districts = json.load(open(r"neighbor-districts-modified.json"))
cases_week = pd.read_csv("csv-files/cases-week.csv").set_index("districtid")
cases_month =pd.read_csv("csv-files/cases-month.csv").set_index("districtid")
cases_overall = pd.read_csv("csv-files/cases-overall.csv").set_index("districtid")


# creating dataframe with neighbor-districts data
neighbor_districts_df = pd.DataFrame(neighbor_districts).T.drop("neighbors",axis=1).reset_index().rename(columns={"id":"districtid"})
neighbor_districts_df["state"] = neighbor_districts_df["index"].apply(lambda x: x[x.index("_")+1  : ])
neighbor_districts_df=neighbor_districts_df.drop("index",axis=1).set_index("districtid")


# joining the above dataframe with cases_week, cases_month and cases_overall
data_week= neighbor_districts_df.join(cases_week)
data_month= neighbor_districts_df.join(cases_month)
data_overall= neighbor_districts_df.join(cases_overall)



# defining a function which can calculate the mean and standard deviation of other districts in state according to the data and time given. Here,time is either week, month or overall, whereas data refers to file with corresponding time.

def func( data  , time):
    csv = pd.DataFrame() 
    series= list()
    for state in data["state"].unique():
        data_state_wise = data[data["state"]==state]
        for dist_id in data_state_wise.index.unique():
            other_districts = data_state_wise.drop(dist_id)
            if other_districts.empty:
                for timeid in data[time].unique(): 
                    series.append({"districtid":dist_id,time: timeid })
            else:
                other_districts_mean = other_districts.groupby(time).mean().rename(columns={"cases":"statemean"})
                other_districts_std = other_districts.groupby(time).std().rename(columns={"cases":"statestdev"})
                other_districts = other_districts_mean.join(other_districts_std,lsuffix='default')
                other_districts['districtid'] = [dist_id]* len(other_districts)
                csv = pd.concat([csv,other_districts])
    csv=csv.reset_index()
    csv = csv.append(series, ignore_index=True)
    csv = csv.set_index("districtid").fillna(0).round(2).sort_values(by=["districtid",time])
    return csv




# using func() to get the required data, for overall time period
overall=func(data_overall , "overallid" )
overall.to_csv("csv-files/state-overall.csv")


# using func() to get the required data, for each week
week = func(data_week , "weekid" )
week.to_csv("csv-files/state-week.csv")


# using func() to get the required data, for each month
month=func(data_month , "monthid" )
month.to_csv("csv-files/state-month.csv")

