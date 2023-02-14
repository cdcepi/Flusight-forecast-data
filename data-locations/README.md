Data locations
============================

This folder contains a single comma-separated text file `locations.csv` that 
contains the location name, FIPS code, and population for each valid forecast location.

Note that national, state, and Puerto Rico population sizes are taken from the [U.S. Census Bureau 2021 Vintage population totals](https://www.census.gov/data/tables/time-series/demo/popest/2020s-state-total.html). Population information provided for other territories is taken from the [JHU CSSE GitHub repository](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data).

Additional columns `count_rate1per100k` and `count_rate2per100k` have been added for the 2022-2023 experimental target count thresholds based on the rate boundaries of 1/100,000 and 2/100,000 population. Please note however that the difference in weekly rates will not be evaluated for the following territories due to small population sizes: American Samoa, Guam, Northern Mariana Islands, and Virgin Islands. 


