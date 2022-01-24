library(covidHubUtils)
library(ggplot2)
fcasts <- load_forecasts(source = "local_hub_repo", models = c("CMU-TimeSeries","UT_FluCast-Voltaire",
                                                               "CU-ensemble","Flusight-baseline","LUcompUncertLab-VAR2",
                                                               "LosAlamos_NAU-CModel_Flu","PSI-DICE","JHUAPL-Gecko","IEM_Health-FluProject","GT-FluFNP","UVAFluX-Ensemble","SigSci-CREG"),dates="2022-01-10",targets = c(paste0(rep(1:4)," wk ahead inc flu hosp")),
                                data_processed_subpath = "data-forecasts/" ,hub_repo_path = "/Users/gcgibson/Flusight-forecast-data/",hub="FluSight" )

#truth <- load_truth(hub = "FluSight")
  
scores <- score_forecasts(fcasts,truth = truth,metrics = c("abs_error","wis"),use_median_as_point=TRUE)

ggplot(scores[scores$location == "US",],aes(x=model,y=log(wis))) + geom_point() + theme_bw()+ theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) +
  geom_hline(yintercept = median(log(scores[scores$model == "Flusight-baseline",]$wis)))
