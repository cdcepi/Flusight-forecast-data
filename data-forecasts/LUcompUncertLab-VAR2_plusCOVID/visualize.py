class viz(object):
    
    def __init__(self,dataQuantiles,fluhosp,covidhosp,includedstates,hhsregion):
        self.d = dataQuantiles
        self.flu   = fluhosp
        self.covid = covidhosp

        self.flusubset   = fluhosp[includedstates].reset_index().drop(columns=["mw","ew"]).set_index("date")
        self.covidsubset = covidhosp[includedstates].reset_index().drop(columns=["mw","ew"]).set_index("date")
        
        self.nlocs = len(self.d.location.unique())

        self.HHS = hhsregion

        self.forecast_date = str(dataQuantiles.forecast_date.values[0])

        self.includedstates = includedstates
        
    def mm2inch(self,x):
        return x/25.4

    def checkDir(self):
        import os
        dir = "./viz/{:s}".format(self.forecast_date)
        if os.path.isdir(dir):
            pass
        else:
            os.mkdir(dir)
        return dir
    
    def forecastVizHHS(self):
        import os
        import matplotlib.pyplot as plt
        import seaborn as sns

        dir = self.checkDir()
        
        plt.style.use("fivethirtyeight")
        fig,ax = plt.subplots()
        p = ax.plot(self.flusubset)
        
        colors = [x.get_color() for x in p]
        self.colors=colors
        
        for loc,color in zip(self.includedstates,colors):
            cis = self.d.loc[ (self.d["quantile"].isin([0.025,0.50,0.975])) & (self.d.location==loc) ]
            target_end_dates = cis.target_end_date.unique()
            
            low = cis.loc[cis["quantile"]==0.025,"value"]
            mid = cis.loc[cis["quantile"]==0.50,"value"]
            hig = cis.loc[cis["quantile"]==0.975,"value"]
            
            ax.fill_between(target_end_dates , low, hig, color = color, alpha=0.50 )
            ax.plot( target_end_dates, mid, color=color, lw=1,ls="--",label="Loc = {:s}".format(loc))

        ax.set_xticks(ax.get_xticks()[::-1][::5][::-1])

        ax.tick_params(which="both",labelsize=6)
        ax.set_xlabel("Target end date",fontsize=8)
        ax.set_ylabel("Num. of confirmed flu hosps",fontsize=8)
        ax.legend(fontsize=10)

        w=self.mm2inch(183)
        fig.set_size_inches(w,w/1.6)

        plt.savefig("{:s}/HHS_{:02d}.pdf".format(dir,self.HHS))
        plt.savefig("{:s}/HHS_{:02d}.png".format(dir,self.HHS),dpi=300)

        plt.close()

    def forecastVizLOCS(self):
        def formatAxis(ax):
            ax.tick_params(which="both",labelsize=6)

            ax.set_xticks(ax.get_xticks()[::-1][::5][::-1])
            
            ax.set_xlabel("Target end date",fontsize=8)
            
            ax.legend(fontsize=10,loc="center")

        import matplotlib.pyplot as plt
        import seaborn as sns

        dir = self.checkDir()

        for loc in self.flusubset:
            subset = self.flusubset[loc]
            subsetcovid = self.covidsubset[loc]
            
            plt.style.use("fivethirtyeight")
            fig,axs = plt.subplots(2,1)
            ax = axs[0]

            p = ax.plot(subset)
           
            colors = [x.get_color() for x in p]
            color = colors[0]

            cis = self.d.loc[ (self.d["quantile"].isin([0.025,0.50,0.975])) & (self.d.location==loc) ]
            target_end_dates = cis.target_end_date.unique()

            low = cis.loc[cis["quantile"]==0.025,"value"]
            mid = cis.loc[cis["quantile"]==0.50,"value"]
            hig = cis.loc[cis["quantile"]==0.975,"value"]

            ax.fill_between(target_end_dates , low, hig, color = color, alpha=0.50 )
            ax.plot( target_end_dates, mid, color=color, lw=1,ls="--",label="Loc = {:s}".format(loc))
            
            formatAxis(ax)
            ax.set_ylabel("Num. of confirmed flu hosps",fontsize=8)
            
            #covidplot
            axs[1].plot(subsetcovid,label="covid",color="red")
            formatAxis(axs[1])
            ax.set_ylabel("Num. of confirmed covid hosps",fontsize=8)

            w=self.mm2inch(183)
            fig.set_size_inches(w,w/1.6)

            plt.savefig("{:s}/LOC_{:s}.pdf".format(dir,loc))
            plt.savefig("{:s}/LOC_{:s}.png".format(dir,loc),dpi=300)

            plt.close()
 
