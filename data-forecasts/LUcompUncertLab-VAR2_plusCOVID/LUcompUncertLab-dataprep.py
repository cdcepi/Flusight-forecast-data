#mcandrew

import sys
import numpy as np
import pandas as pd

def fromdate2YRWK(dates):
    from epiweeks import Week
    import pandas as pd

    datesdata = {"date":[],"yr":[],"week":[],"ew":[]}

    for date in sorted(dates):
        ew = Week.fromdate(pd.to_datetime(date))

        yr   = ew.year
        week = ew.week
        
        datesdata["date"].append(date)
        datesdata["yr"].append(yr)
        datesdata["week"].append(week)
        datesdata["ew"].append(int("{:04d}{:02d}".format(yr,week)))
    return pd.DataFrame(datesdata)

def buildModelWeeks(ews):
    ewAndMW = {"ew":[],"mw":[]}
    for mw,ew in enumerate(sorted(ews)):
        ewAndMW["ew"].append(ew)
        ewAndMW["mw"].append(mw)
    return pd.DataFrame(ewAndMW)

if __name__ == "__main__":

    #FLU HOSPS
    d = pd.read_csv("../../data-truth/truth-Incident Hospitalizations.csv") # location of data-truth

    datesdata = fromdate2YRWK(d.date.unique())
    
    d = d.merge(datesdata,on="date")

    ewAndModelWeek = buildModelWeeks(d.ew.unique())
    d = d.merge(ewAndModelWeek,on="ew")

    fromMw2Ew = {row.mw:row.ew for _,row in ewAndModelWeek.iterrows() }
    
    ewByLocation = pd.pivot_table(index=["ew","mw","date"],columns=["location"],values = ["value"],data=d)
    ewByLocation.columns = [location for (x,location) in ewByLocation.columns]

    ewByLocation = ewByLocation.reset_index()

    ewByLocation.to_csv("confirmedFluHosps__wide.csv",index=False)
    d.to_csv("confirmedFluHosps__long.csv",index=False) 


    #COVIDHOSPS
    d = pd.read_csv("../../../covid19forecasthub/data-truth/truth-Incident Hospitalizations.csv")
    
    datesdata = fromdate2YRWK(d.date.unique())
    
    d = d.merge(datesdata,on="date")

    ewAndModelWeek = buildModelWeeks(d.ew.unique())
    d = d.merge(ewAndModelWeek,on="ew")

    #AGGREGATE FROM DAILY TO EPIDEMIC WEEK. THIS IS DIFFERENT THAN WITH THE FLU
    d = d.groupby(["location","location_name","yr","week","ew","mw"]).apply(lambda x: pd.Series({"value":x.value.sum(),"date":max(x["date"])   }))
    d = d.reset_index()
    
    fromMw2Ew = {row.mw:row.ew for _,row in ewAndModelWeek.iterrows() }
    
    ewByLocation = pd.pivot_table(index=["ew","mw","date"],columns=["location"],values = ["value"],data=d)
    ewByLocation.columns = [location for (x,location) in ewByLocation.columns]

    ewByLocation = ewByLocation.reset_index()

    ewByLocation.to_csv("confirmedCOVIDHosps__wide.csv",index=False)
    d.to_csv("confirmedCOVIDHosps__long.csv",index=False) 
