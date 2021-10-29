#!/usr/bin/env python

# importing necessary packaes
import json
import pandas as pd
from datetime import date
from datetime import datetime


#loading required data files
neighbor_districts = json.load(open(r"neighbor-districts-modified.json"))
alldata = json.load(open(r"data-all.json"))
district_wise= pd.read_csv("district_wise.csv")


# creating a dictionary of data in the date interval : 15/03/2020 to 05/09/2020
df= { x:alldata[x] for x in alldata if  str(date(2020,3,14))< x < str(date(2020,9,6)) }



# creating a dictionary of the form {state_cod : state_name} 
df3=district_wise[["State_Code","State"]]
state_code = list(df3.set_index("State_Code").to_dict().values())[0]



# collecting necessary data from data-all.json, neighbor-districts-modified.json and district-wise.csv files
data=[]
for d in df:
    for x in alldata[d]:
        if 'districts' in alldata[d][x]:
            for y in alldata[d][x]['districts']:
                if "delta" in alldata[d][x]['districts'][y] and "confirmed" in alldata[d][x]['districts'][y]["delta"] :
                    data.append([d,state_code[x].lower(),y.lower(),alldata[d][x]['districts'][y]["delta"]["confirmed"]])



# creating dataframe of collected data
dataframe = pd.DataFrame(data,columns=["date","state","district","cases"]).set_index("district")


# creating function to get week id from given date, where week 11 is given as id 1
def get_week_id(date):
    d=datetime.strptime(date,"%Y-%m-%d").date()
    return int(d.strftime("%U"))-10


# creating function to get month id from given date, where month 3 is given as id 1
def get_month_id(date):
    d=datetime.strptime(date,"%Y-%m-%d").date().month
    return d-2




# Code for calculating cases per week 
cases=pd.DataFrame()
series=dict()
for x in neighbor_districts:
    i=x.index("_")
    dist= x[0:i ]
    state = x[i+1:]
    dist_id= neighbor_districts[x]["id"]
    d=dataframe.loc[dist].copy()
    if type(d)==pd.Series:
        series[dist_id]=[get_week_id(d['date']) , d['cases']]
    else:
        d=d[d['state']==state]
        d['weekid'] = d['date'].apply(lambda x : get_week_id(x)) 
        d1=d.groupby(by='weekid' ).sum()
        d1['districtid']= [dist_id]*len(d1)
        cases=pd.concat([cases,d1])
cases=cases.reset_index().set_index("districtid")
for x in series:
    cases.loc[x] = series[x]
cases=cases.sort_values(by=["districtid","weekid"])

#storing output in cases-week.csv
cases.to_csv("csv-files/cases-week.csv")






# Code for calculating cases per month 
cases=pd.DataFrame()
series=dict()
for x in neighbor_districts:
    i=x.index("_")
    dist= x[0:i ]
    state = x[i+1:]
    dist_id= neighbor_districts[x]["id"]
    d=dataframe.loc[dist].copy()
    if type(d)==pd.Series:
        series[dist_id]=[get_month_id(d['date']) , d['cases']]
    else:
        d=d[d['state']==state]
        d['monthid'] = d['date'].apply(lambda x : get_month_id(x)) 
        d1=d.groupby(by='monthid' ).sum()
        d1['districtid']= [dist_id]*len(d1)
        cases=pd.concat([cases,d1])
cases=cases.reset_index().set_index("districtid")
for x in series:
    cases.loc[x] = series[x]
cases=cases.sort_values(by=["districtid","monthid"])

#storing output in cases-month.csv
cases.to_csv("csv-files/cases-month.csv")




#Code for calculating overall cases

cases=pd.DataFrame(columns=["districtid",'overallid','cases']).set_index("districtid")
series= dict()
for x in neighbor_districts:
    i=x.index("_")
    dist= x[0:i ]
    state = x[i+1:]
    dist_id= neighbor_districts[x]["id"]
    d = dataframe.loc[dist].copy()
    if type(d) != pd.Series:
        d= d[d["state"]==state]
        cases.loc[dist_id] = [1, sum(d["cases"])]
    else:
        cases.loc[dist_id] = [1, d["cases"]]
cases=cases.sort_values(by=["districtid","overallid"])

#storing output in cases-overall.csv
cases.to_csv("csv-files/cases-overall.csv")



