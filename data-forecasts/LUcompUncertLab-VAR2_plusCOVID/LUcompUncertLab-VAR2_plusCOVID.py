#mcandrew

import sys
import numpy as np
import pandas as pd

from interface import interface
from model     import VAR
from visualize import viz

def getHHS():
        return { 1:["09","23","25","33","44","50"]
                ,2:["34","36","72","78"]
                ,3:["10","11","24","42","51","54"]
                ,4:["01","12","13","21","28","37","45","47"]
                ,5:["17","18","26","27","39","55"]
                ,6:["05","22","35","40","48"]
                ,7:["19","20","29","31"]
                ,8:["08","30","38","46","49","56"]
                ,9:["04","06","15","32"] # no american samoa, no mariana, no microni, no guam,nomarshall,nopa
                ,10:["02","16","41","53"]}

def getStates(HHS):
    return [state for (hhs,states) in HHS.items() for state in states]


def prepareData(f):
    fluhosp = pd.read_csv(f)   
    fluhosp = fluhosp.loc[fluhosp.ew>202101] #ONLY CONSIDERING 2021 and later

    fluhosp = fluhosp.set_index(["ew","mw","date"])
    #fluhosp = fluhosp.loc[:, fluhosp.sum(0)!=0] # REMOVE locations with all zeros
    return fluhosp
       
if __name__ == "__main__":

    #PREPARE DATA
    fluhosp   = prepareData("confirmedFluHosps__wide.csv")
    covidhosp = prepareData("confirmedCOVIDHosps__wide.csv")

    # SELECT STATES
    writeout=1
    HHS = getHHS()
    states = getStates(HHS)
    for n,includedstates in enumerate(states):
        
        # BUILD INTERFACE
        interface_local = interface(fluhosp,covidhosp,[includedstates])

        #TRAIN
        model = VAR(data = interface_local.y,L=2,F=4)
        model.fit()

        #FORMAT SAMPLES
        dataPredictions = model.formatSamples(interface_local)
        dataQuantiles   = model.fromSamples2Quantiles()

        interface_local.writeData(writeout,dataPredictions,dataQuantiles)
        if n==0:
            writeout=0

        visual = viz(dataQuantiles,fluhosp,covidhosp,[includedstates],[])
        visual.forecastVizLOCS()

    #BUILD US FORECAST
    USquantiles = model.createUnitedStatesForecast()

    interface_local.writeData(writeout=0,dataPredictions=None,dataQuantiles = USquantiles)
    
    visual = viz(USquantiles,fluhosp,covidhosp,["US"],[])
    visual.forecastVizLOCS()
