#mcandrew

import sys
import numpy as np
import pandas as pd

from glob import glob

def checkNumberOfLocations(f,raw=1):
    d = pd.read_csv(f)
    if raw:
        d = d.set_index(["ew","mw","date"])
        locs = len(d.columns)
        return d,locs

    else:
        locs = len(d.location.unique())
        return d,locs

def missingLocations(data,forecast):
    missing = list(set(data.columns) - set( [ "{:s}".format(x) for x in forecast.location.unique()]))
    
    if len(missing):
        missinglocs = ", ".join(missing)
        print("Missing the following locations {:s}".format(missinglocs))
    else:
        print("Not missing locations")
        
if __name__ == "__main__":

    f = "confirmedFluHosps__wide.csv"
    fludata,locs = checkNumberOfLocations(f)
    print("Number of Locations for file {:s} {:d}".format(f,locs))
    
    for f in glob("*LUcompUncertLab-VAR2.csv"):
        d,locs = checkNumberOfLocations(f,0)
        print("Number of Locations for file {:s} {:d}".format(f,locs))

        missingLocations(fludata,d)
        
