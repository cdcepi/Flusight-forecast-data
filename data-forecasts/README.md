Data submission instructions
============================

This page is intended to provide teams with all the information they
need to submit forecasts. We note that these instructions have been adapted from the [COVID-19 Forecast Hub](https://github.com/reichlab/covid19-forecast-hub).

All forecasts should be submitted directly to
the [data-forecasts/](./) folder. Data in this directory should be added
to the repository through a pull request so that automatic data
validation checks are run.

These instructions provide detail about the [data
format](#Data-formatting) as well as [validation](#Data-validation) that
you can do prior to this pull request. In addition, we describe
[metadata](https://github.com/cdcepi/Flusight-forecast-data/blob/master/data-forecasts/METADATA.md) that each model should provide.

*Table of Contents*

-   [What is a forecast](#What-is-a-forecast)
-   [ground truth data](#ground-truth-data)
-   [data formatting](#Data-formatting)
-   [forecast file format](#Forecast-file-format)
-   [forecast data validation](#Forecast-validation)
-   [weekly ensemble build](#Weekly-ensemble-build)
-   [policy on late submissions](#policy-on-late-or-updated-submissions)


What is a forecast
-----------------

Models are asked to make specific quantitative forecasts about data that will be observed in the future. These forecasts are interpreted as "unconditional" predictions about the future. That is, they are not predictions only for a limited set of possible future scenarios in which a certain set of conditions (e.g. vaccination uptake is strong, or new social-distancing mandates are put in place) hold about the future -- rather, they should characterize uncertainty across all reasonable future scenarios. In practice, all forecasting models make some assumptions about how current trends in data may change and impact the forecasted outcome; some teams select a "most likely" scenario or combine predictions across multiple scenarios that may occur. Forecasts submitted to this repository will be evaluated against observed data. 

We note that other modeling efforts, such as the [COVID-19 Scenario Modeling Hub](https://covid19scenariomodelinghub.org/), have been launched to collect and aggregate model outputs from "scenario projection" models. These models create longer-term projections under a specific set of assumptions about how the main drivers of the pandemic (such as non-pharmaceutical intervention compliance, or vaccination uptake) may change over time.

Ground truth data
-----------------

This project treats hospitalization data reported from the HHS Protect system at  HealthData.gov as "ground truth" data. We create processed versions of these data
that are stored in this repository. 

Details on how ground truth data are defined can be found in 
the [data-truth folder README file](../data-truth/README.md).


Data formatting
---------------

The automatic checks in place for forecast files submitted to this repository
validates both the filename and file contents to
ensure the file can be used in the visualization and ensemble
forecasting.

### Subdirectory

Each subdirectory within the [data-forecasts/](data-forecasts/)
directory has the format

    team-model

where

-   `team` is the teamname and
-   `model` is the name of your model.

Both team and model should be less than 15 characters and not include
hyphens. The `model` should be unique from any other model in the project.

Within each subdirectory, there should be a metadata file, a license
file (optional), and a set of forecasts.

### Metadata

The metadata file should have the following format

    metadata-team-model.txt

and here is [the structure of the metadata
file](https://github.com/cdcepi/Flusight-forecast-data/blob/master/data-forecasts/METADATA.md).

### License (optional)

By default, forecasts are released under a CC-BY 4.0 license. If you would like to release your forecasts under a different license, please specify a [standard
license](../accepted-licenses.csv) in the `license` field of your metadata file. Alternatively, if you wish to use a license that is not in the list of [standard
licenses](../accepted-licenses.csv), you may include a 

    LICENSE.txt

file in your model directory. 

### Forecasts

Each forecast file within the subdirectory should have the following
format

    YYYY-MM-DD-team-model.csv

where

-   `YYYY` is the 4 digit year,
-   `MM` is the 2 digit month,
-   `DD` is the 2 digit day,
-   `team` is the teamname, and
-   `model` is the name of your model.

The date YYYY-MM-DD is the [`forecast_date`](#forecast_date). For this project, the `forecast_date` should always be the Monday on which the submission is due.

The `team` and `model` in this file must match the `team` and `model` in
the directory this file is in. Both `team` and `model` should be less
than 15 characters, alpha-numeric and underscores only, with no spaces
or hyphens.

Forecast file format
--------------------

The file must be a comma-separated value (csv) file with the following
columns (in any order):

-   `forecast_date`
-   `target`
-   `target_end_date`
-   `location`
-   `type`
-   `quantile`
-   `value`

No additional columns are allowed.

Each row in the file is either a point or quantile forecast for a
location on a particular date for a particular target.

### `forecast_date`

Values in the `forecast_date` column must be a date in the format

    YYYY-MM-DD

This is the date of the Monday on which the forecasts were due to be submitted.  `forecast_date` should correspond
and be redundant with the date in the filename, and is included here by
request from some analysts. 

### `target`

Values in the `target` column must be a character (string) and be one of
the following specific targets:

-   “N wk ahead inc flu hosp” where N is a number between 1 and 4


For week-ahead forecasts, we will use the specification of
epidemiological weeks (EWs) [defined by the US
CDC](https://wwwn.cdc.gov/nndss/document/MMWR_Week_overview.pdf) which
run Sunday through Saturday. There are standard software packages to
convert from dates to epidemic weeks and vice versa. E.g.
[MMWRweek](https://cran.r-project.org/web/packages/MMWRweek/) for R and
[pymmwr](https://pypi.org/project/pymmwr/) and
[epiweeks](https://pypi.org/project/epiweeks/) for python.

For week-ahead forecasts with `forecast_date` of Monday of
EW12, a 1 week ahead forecast corresponds to EW12 and should have
`target_end_date` of the Saturday of EW12. 

#### N week ahead inc flu hosp

This target is the number of new weekly hospitalizations predicted by the
model during the week that is N weeks after `forecast_date`.

### `target_end_date`

Values in the `target_end_date` column must be a date in the format

    YYYY-MM-DD

This is the date for the forecast `target`. For “\# wk”
targets, `target_end_date` will be the Saturday at the end of the week
time period.

### `location`

Values in the `location` column must be one of the “locations” in this
[FIPS numeric code file](../data-locations/locations.csv) which includes
numeric FIPS codes for U.S. states and selected jurisdictions (Washington DC, Puerto Rico, and the US Virgin Islands) as well as “US” for national forecasts.

Please note that when writing FIPS codes, they should be written in as a
character string to preserve any leading zeroes.

### `type`

Values in the `type` column are either

-   “point” or
-   “quantile”.

This value indicates whether that row corresponds to a point forecast or
a quantile forecast. Point forecasts are used in visualization while
quantile forecasts are used in visualization and in ensemble
construction.

**When point forecasts are not included, the median for every
location-target pair will be interpreted as the point forecast.**

### `quantile`

Values in the `quantile` column are either “NA” (if `type` is “point”)
or a quantile in the format

    0.###

For quantile forecasts, this value indicates the quantile for the
`value` in this row.

Teams must provide the following 23 quantiles:

    c(0.01, 0.025, seq(0.05, 0.95, by = 0.05), 0.975, 0.99)

    ##  [1] 0.010 0.025 0.050 0.100 0.150 0.200 0.250 0.300 0.350 0.400 0.450 0.500
    ## [13] 0.550 0.600 0.650 0.700 0.750 0.800 0.850 0.900 0.950 0.975 0.990


### `value`

Values in the `value` column are non-negative numbers indicating the
“point” or “quantile” prediction for this row. For a “point” prediction,
`value` is simply the value of that point prediction for the `target`
and `location` associated with that row. For a “quantile” prediction,
`value` is the inverse of the cumulative distribution function for
the `target`, `location`, and `quantile` associated with that row.


Forecast validation
-------------------

To ensure proper data formatting, pull requests for new data in
`data-forecasts/` will be automatically run.

### Pull request forecast validation

When a pull request is submitted, the data are validated through [Github Actions](https://docs.github.com/en/actions) which runs the tests present in [the validations repository](https://github.com/cdcepi/Flusight-forecast-validation). The intent
for these tests are to validate the requirements above.
Please [let us
know](https://github.com/cdcepi/Flusight-forecast-data/issues)  if you are facing issues while running the tests.


Weekly ensemble build
-----------

Every Monday at 11pm ET, we will generate the ensemble forecast using a single valid forecast from each team that submitted in the current week.


Policy on late or updated submissions
------------------

In order to ensure that forecasting is done in real-time, all forecasts are required to be submitted to this repository by 11pm ET on Mondays each week. We do not accept late forecasts. 
