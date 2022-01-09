#mcandrew

class VAR(object):
    def __init__(self,data,F=4,L=2):
        self.F=F
        self.L=L

        self.T = data.shape[1]
        self.P = data.shape[0]

        self.data=data

    def varmodeldesc(self):
        modelDesc = """
            data {
               int T;
               int P;
               int F;
               int L;
               matrix[P,T] y;
            }
            parameters {
              matrix<lower=-1,upper=1>[P,P] B [L] ;
              vector [P] C;
              cov_matrix[P] Epsilon;
            }
            model {
               vector [P] M;
               //fitting
               for(t in (L+1):T){
                  M = C;
                  for (l in 1:L){
                     M += B[l]*y[:,(t-l)];
                  }
                  y[:,(t)]~multi_normal(M,Epsilon);
               }
            }
             generated quantities {
               matrix [P,F+L] ytilde = rep_matrix(0,P,F+L); // constrained to be at or above 0 to model counts
               vector [P] M;
               ytilde[:,1:L] = y[:,(T-(L-1)):T]; 

               //predicting
               for (f in (L+1):(L+F)){
                  M=C;
                  for (l in 1:L){
                     M += B[l]*ytilde[:,(f-l)];
                   }
                   ytilde[:,f] = multi_normal_rng(M,Epsilon);
                }
            }
            """
        return modelDesc
        
    def fit(self):
        import stan
        data = {"y":self.data,"T":self.T,"P":self.P,"F":self.F,"L":self.L}
        model = self.varmodeldesc()
        
        posterior = stan.build(model, data=data)
        fit = posterior.sample()

        self.fit = fit
        
    def formatSamples(self,timeinfo):
        import numpy as np
        import pandas as pd
        
        dataPredictions = {"forecast_date":[],"target_end_date":[],"location":[], "target":[],"sample":[],"value":[]}

        #CUT matrix in half. the top half is flu and and the bottom half is covid
        numberOfRows = self.fit["ytilde"].shape[0]
        
        predictions = self.fit["ytilde"][:int(numberOfRows/2),self.L:,:]

        F = timeinfo.numOfForecasts
        for sample,forecasts in enumerate(np.moveaxis(predictions,2,0)):
            for n,forecast in enumerate(forecasts):

                dataPredictions["forecast_date"].extend(F*[timeinfo.forecast_date])
                dataPredictions["location"].extend( F*[timeinfo.timeseriesName[n]] )
                dataPredictions["target_end_date"].extend( timeinfo.target_end_dates )
                dataPredictions["target"].extend( timeinfo.targets )
                dataPredictions["sample"].extend( F*[sample] )
                dataPredictions["value"].extend( forecast )
        dataPredictions = pd.DataFrame(dataPredictions)
        self.dataPredictions = dataPredictions
        return dataPredictions

    def createQuantiles(self,x):
        import numpy as np
        import pandas as pd
 
        quantiles = np.array([0.010, 0.025, 0.050, 0.100, 0.150, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500
                              ,0.550, 0.600, 0.650, 0.700, 0.750, 0.800, 0.850, 0.900, 0.950, 0.975, 0.990])
        quantileValues = np.percentile( x["value"], q=100*quantiles)     
        return pd.DataFrame({"quantile":list(quantiles),"value":list(quantileValues)})
    
    def fromSamples2Quantiles(self):
        dataQuantiles = self.dataPredictions.groupby(["forecast_date","target_end_date","location","target"]).apply(lambda x: self.createQuantiles(x)).reset_index().drop(columns="level_4")
        dataQuantiles["type"] = "quantile"
        
        self.dataQuantiles = dataQuantiles
        return dataQuantiles
    
    def createUnitedStatesForecast(self):
        from glob import glob

        import numpy as np
        import pandas as pd
        
        predictionFile = sorted(glob("*-allPredictions.csv"))[-1]

        allPredictions = pd.read_csv(predictionFile)

        def addUpCounts(x):
            return pd.Series({"value":x.value.sum()})
        allTtlPredictions = allPredictions.groupby(["forecast_date","target_end_date","sample","target"]).apply(addUpCounts).reset_index()
        allTtlPredictions["location"] = "US"
        allTtlPredictions["type"] = "quantile"

        USquantiles = allTtlPredictions.groupby(["forecast_date","target_end_date","location","target"]).apply(lambda x: self.createQuantiles(x) ).reset_index().drop(columns="level_4")
        return USquantiles
 

if __name__ == "__main__":
    pass

