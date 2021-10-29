#!/usr/bin/env python

# importing necessary packages
import json
import pandas as pd


#loading required data files
state_week =pd.read_csv("csv-files/state-spot-week.csv").set_index("districtid")
state_month =pd.read_csv("csv-files/state-spot-month.csv").set_index("districtid")
state_overall = pd.read_csv("csv-files/state-spot-overall.csv").set_index("districtid")

neighbor_week =pd.read_csv("csv-files/neighborhood-spot-week.csv").set_index("districtid")
neighbor_month =pd.read_csv("csv-files/neighborhood-spot-month.csv").set_index("districtid")
neighbor_overall = pd.read_csv("csv-files/neighborhood-spot-overall.csv").set_index("districtid")

zscore_week=pd.read_csv("csv-files/zscore-week.csv").set_index("districtid")
zscore_month =pd.read_csv("csv-files/zscore-month.csv").set_index("districtid")
zscore_overall = pd.read_csv("csv-files/zscore-overall.csv").set_index("districtid") 



'''
defining a function which would return top 5 hotspots and coldspots according to the parameters provided. 
   Here, time			= week/month/overall
		 timeid 		= weekid/monthid/overallid
	 	 data 			= neighbor_time/state_time
	 	 zscore_data	= zscore_time
		 method			= neighborhood/state
'''
def find_top_spots(data,timeid,zscore_data,method):
    s_cold=dict()
    s_hot=dict()
    t=pd.merge(data[data["spot"].notna()], zscore_data,on=[timeid,"districtid"],how="left").reset_index().set_index(timeid)
    if timeid=="monthid":
        timeid_list=range(1,8)
    elif timeid=="weekid":
        timeid_list=range(1,26)
    else:
        timeid_list=[1]
    for tid in timeid_list:
        if tid not in t.index:
            s_cold[tid]= ["-"]*5
            s_hot[tid] =["-"]*5
        else:
            df = t.loc[tid]
            cold = df[ df["spot"]=="coldspot" ].sort_values(method+"zscore",ascending=True).head(5)
            hot = df[ df["spot"]=="hotspot" ].sort_values(method+"zscore",ascending=True).tail(5)
            s_cold[tid] = list(cold["districtid"])
            s_hot[tid] = list(hot["districtid"])
            l_cold=len(s_cold[tid])
            if l_cold<5:
                s_cold[tid].extend(['-']*(5-l_cold))
           
            l_hot=len(s_hot[tid])
            if l_hot<5:
                s_hot[tid].extend(['-']*(5-l_hot))
    result_cold=pd.DataFrame(s_cold).T
    result_cold["spot"]=["coldspot"]*len(result_cold)
    result_hot=pd.DataFrame(s_hot).T
    result_hot["spot"]=["hotspot"]*len(result_hot)
    result= result_cold.append(result_hot)
    result=result.rename(columns={0:"districtid1",1:"districtid2",2:"districtid3",3:"districtid4",4:"districtid5"})
    result.index.name=timeid
    result["method"]= [method]*len(result)
    return result



# Finding top 5 spots per week
n_week=   find_top_spots(neighbor_week,"weekid",zscore_week,"neighborhood")
s_week = find_top_spots(state_week,"weekid",zscore_week,"state")
week = n_week.append(s_week).sort_values(["weekid","method"])
week.to_csv("csv-files/top-week.csv")

# Finding top 5 spots per month
n_month=   find_top_spots(neighbor_month,"monthid",zscore_month,"neighborhood")
s_month = find_top_spots(state_month,"monthid",zscore_month,"state")
month = n_month.append(s_month).sort_values(["monthid","method"])
month.to_csv("csv-files/top-month.csv")

# Finding top 5 spots overall
n_overall=   find_top_spots(neighbor_overall,"overallid",zscore_overall,"neighborhood")
s_overall = find_top_spots(state_overall,"overallid",zscore_overall,"state")
overall = n_overall.append(s_overall).sort_values(["overallid","method"])
overall.to_csv("csv-files/top-overall.csv")

