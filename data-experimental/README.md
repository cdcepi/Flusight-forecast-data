# Experimental Target Data submission instructions

This page is intended to provide teams with all the information they
need to submit experimental target forecasts for the 2022-2023 influenza. We note that these instructions have been adapted from the [COVID-19 Forecast
Hub](https://github.com/reichlab/covid19-forecast-hub).

All experimental target forecasts should be submitted directly to the [data-experimental/](./)
folder. Data in this directory should be added to the repository through a pull request that is separate from pull requests containing standard forecasts. Please note that automatic data validation checks will not be run for experimental targets and additional file formatting diligence is appreciated.


*Table of Contents*

-   [Objective](#Objective)
-   [Proposal](#Proposal)
-   [Forecast file format](#Forecast-file-format)

## Objective

The purpose of introducing an additional experimental target is to provide an opportunity for forecasting teams to submit forecasts for increasing and decreasing activity. While forecasting the magnitude of change during periods of rapid changes in hospitalizations is difficult, it may be possible to reliably forecast the direction of change. If categorical forecasts are shown to be reliable, they would provide valuable information for public health stakeholders. 

## Proposal
For the 2022-23 influenza season, we define categorical rate changes as follows. State-level changes in hospital admission incidence will be considered in terms of differences on a rate scale (counts per 100k people). Thresholds separating categories of change (e.g., separating "stable" forecasts from "increase" forecasts) will be the same across states, but are translatable into counts using the state's population size (see locations.csv, in the data-locations subfolder of the Flusight-forecast-data repository). The experimental target, named "2 wk flu hosp rate change" will be submitted as estimates of the probability of occurrence for each rate change category in a new subdirectory of the Flusight-forecast data repository: data-experimental.

Observed changes, for the purpose of evaluating experimental target forecasts, will be determined by final reported values for weekly influenza admissions in the HHS Protect dataset (see FluSight Guidelines for the 2022-23 season for additional details). As such, forecasting teams are encouraged to consider uncertainty in values as they are reported in real time.

*Note:* This season we will solicit these targets for two-week ahead horizons (i.e., rate difference between week t+2 and current week t). The utility of providing categorical forecasts at other time horizons may be considered in future seasons.

The experimental rate change targets will be reported as probabilities of occurrence and binned into the following categories: stable, increase, decrease, large increase, large decrease, and defined as follows (see Appendix 2 for equivalent diagram):

A forecasted change will be defined as the rate change between the 2-week-ahead and finalized hospitalization rates in the preceding week the forecast were made (i.e., rate_change = yt+2 - yt, where yt denotes the rate of weekly hospitalizations at time t in units of counts/100k). Corresponding count changes are based on state-level population sizes (i.e., count_change = rate_change*state_population / 100,000). See the locations.csv file in [data-locations/](../data-locations) for the population sizes that will be used to calculate rates.  

*Stable:* forecasted changes in hospitalizations qualify as stable if either the magnitude of the rate change is less than 1/100k OR the corresponding magnitude of the count change is less than 20. 
  
*Increase:* positive forecasted changes that do not qualify as stable and for which the forecasted rate change is less than 2/100k OR the magnitude of the count change is less than 40.

*Large increase:* positive forecasted rate changes that are larger than or equal to 2/100k, AND the count change is larger than or equal to 40. 

*Decrease:* negative forecasted rate changes that do not qualify as stable and for which the forecasted rate change is less than 2/100k OR the magnitude of the count change is less than 40.

*Large decrease:* negative forecasted rate changes that have a magnitude larger than or equal to 2/100k, AND the magnitude of count change is larger than or equal to 40. 



## Experimental Target forecast formatting

### Subdirectory

Each model that submits experimental target forecasts will have a unique subdirectory within the GitHub repository where forecasts will be submitted. These subdirectories should be located in the data-experimental subdirectory and must be named in accordance with the [guidelines for general forecast submissions](../data-forecasts/README.md).

In addition to forecast files (see formatting details below), subdirectories may also contain an optional metadata file or license file.  These are particularly encouraged if needed to document any differences from the corresponding files associated with a team's standard forecasts.   


### Forecasts

Each experimental forecast file should have the following
format

    YYYY-MM-DD-team-model.csv

where

-   `YYYY` is the 4 digit year,
-   `MM` is the 2 digit month,
-   `DD` is the 2 digit day,
-   `team` is the teamname, and
-   `model` is the name of your model.

The date YYYY-MM-DD is the [`forecast_date`](#forecast_date). For this
project, the `forecast_date` should always be the Monday Forecast Due Date.

The `team` and `model` in this file must match the `team` and `model` in
the directory this file is in. Both `team` and `model` should be less
than 15 characters, alpha-numeric and underscores only, with no spaces
or hyphens.

## Forecast file format 

The file must be a comma-separated value (csv) file with the following
columns (in any order):

-   `forecast_date`
-   `target`
-   `location`
-   `type`
-   `type_id`
-   `value`

No additional columns are allowed.

Each row in the file is a point forecast for a location on a particular date for the experimental target.

### `forecast_date` 

Values in the `forecast_date` column must be a date in the ISO format

    YYYY-MM-DD

This is the Forecast Due Date for the submission and will always match the weekly date of standard forecast submissions. `forecast_date` should correspond and be redundant with the date in the filename but is included here to facilitate validation and analysis.

### `target`

Values in the `target` column must be a character (string):

"2 wk flu hosp rate change".


### `location`

Values in the `location` column must be one of the "locations" in
this [FIPS numeric code file](../data-locations/locations.csv) which
includes numeric FIPS codes for U.S. states and selected jurisdictions
(Washington DC, Puerto Rico, and the US Virgin Islands) as well as
"US" for national forecasts.

Please note that when writing FIPS codes, they should be written in as a
character string to preserve any leading zeroes.

Difference in weekly rates will not be evaluated for the following territories due to small population sizes: American Samoa, Guam, Northern Mariana Islands, and Virgin Islands.

### `type`

Values in the `type` column are "category" for this experimental target.

This value indicates that the row corresponds to a categorical forecast.


### `type_id`

Values in the `type_id` column must be a character (string) indicating the experimental rate change category, formatted as follows:

- "stable"
- "increase"
- "decrease"
- "large_increase"
- "large_decrease"


### `value`

Values in the value column are probabilities (non-negative numbers that are greater than or equal to 0 and less than or equal to 1) indicating the estimated probability for the category specified in the `type_id` column for this row. 



### Forecast submission

Experimental Target Forecasts should be submitted via pull request to CDC EPI GitHub repository [https://github.com/cdcepi/Flusight-forecast-data](https://github.com/cdcepi/Flusight-forecast-data) in the data-experimental subdirectory.  
After pull requests are submitted, submissions will be scanned for formatting issues. Please
[let us know](https://github.com/cdcepi/Flusight-forecast-data/issues)
if you have any questions about submitting experimental target forecasts.


