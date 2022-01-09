#mcandrew

class interface(object):
    def __init__(self,fluhosp,covidhosp,includedstates):
        self.fluhosp   = fluhosp
        self.covidhosp = covidhosp
        
        self.includedstates = includedstates
        self.timeseriesName = includedstates

        self.buildDataForModel()
        self.getForecastDate()
        self.generateTargetEndDates()
        self.generateTargetNames()

        self.numOfForecasts = 4 # FOR NOW THIS IS HARDCODED AS a 4 WEEK AHEAD

    def buildDataForModel(self):
        import numpy as np
        yflu   = np.array(self.fluhosp[self.includedstates]).T
        ycovid = np.array(self.covidhosp[self.includedstates]).T

        y = np.vstack( (yflu,ycovid) )
        
        self.y = y
        return y

    def getForecastDate(self):
        import datetime
        from epiweeks import Week

        from datetime import datetime as dt

        today = dt.today()
        dayofweek = today.weekday()

        thisWeek = Week.thisweek()
        if dayofweek in {6,0}: # a SUNDAY or MONDAY
            thisWeek = thisWeek-1
        else:
            pass
        self.thisWeek = thisWeek
        
        forecastDate = ((thisWeek+1).startdate() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.forecast_date = forecastDate
        return forecastDate

    def generateTargetEndDates(self):
        import numpy as np
        
        target_end_dates = []
        for f in np.arange(1,4+1): # four weeks ahead
            ted = ((self.thisWeek+int(f)).enddate()).strftime("%Y-%m-%d")
            target_end_dates.append(ted)
        self.target_end_dates = target_end_dates
        return target_end_dates

    def generateTargetNames(self):
        import numpy as np

        targets = ["{:d} wk ahead inc flu hosp".format(ahead) for ahead in np.arange(1,4+1)]
        self.targets = targets
        return targets

    def writeData(self,writeout,dataPredictions,dataQuantiles):
        if dataPredictions is not None:
            predictString = "{:s}-allPredictions.csv".format(self.forecast_date)
            quantileString = "{:s}-LUcompUncertLab-VAR2_plusCOVID-preprocess.csv".format(self.forecast_date)
        
            if writeout==0:
                dataPredictions.to_csv(predictString,header=False,mode="a",index=False)
                dataQuantiles.to_csv(quantileString,header=False ,mode="a",index=False)

            else:
                dataPredictions.to_csv(predictString,header=True,mode="w",index=False)
                dataQuantiles.to_csv(quantileString ,header=True,mode="w",index=False)
        else:
            quantileString = "{:s}-LUcompUncertLab-VAR2_plusCOVID-preprocess.csv".format(self.forecast_date)
        
            if writeout==0:
                dataQuantiles.to_csv(quantileString,header=False ,mode="a",index=False)

            else:
                dataQuantiles.to_csv(quantileString ,header=True,mode="w",index=False)

if __name__ == "__main__":
    pass

