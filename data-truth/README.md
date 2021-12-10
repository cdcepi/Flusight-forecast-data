# Ground truth data 

The data-truth folder contains the "ground truth" data that forecasts 
are eventually compared to. 

*Table of Contents*

-   [Data sources](#data-sources)
-   [Hospitalization data](#hospitalization-data)
-   [Accessing truth data](#accessing-truth-data)


Data sources
----------------------

Influenza hospitalization data are taken from the [HealthData.gov COVID-19 Reported Patient Impact and Hospital Capacity by State Timeseries](https://healthdata.gov/dataset/covid-19-reported-patient-impact-and-hospital-capacity-state-timeseries). 

Some of these data are also available progammatically through the [EpiData](https://cmu-delphi.github.io/delphi-epidata/) API. 


Hospitalization data
------------

### HealthData.gov Hospitalization Timeseries

The truth data that hospitalization forecasts (`inc hosp` targets) will
be evaluated against are the [HealthData.gov COVID-19 Reported Patient
Impact and Hospital Capacity by State
Timeseries](https://healthdata.gov/Hospital/COVID-19-Reported-Patient-Impact-and-Hospital-Capa/g62h-syeh).
These data are released weekly.

A supplemental data source with daily counts that is updated more
frequently (typically daily) but does not include the full time-series
is [HealthData.gov COVID-19 Reported Patient Impact and Hospital
Capacity by
State](https://healthdata.gov/dataset/COVID-19-Reported-Patient-Impact-and-Hospital-Capa/6xf2-c3ie).

### Resources for Accessing Hospitalization Data

We are working with our collaborators at the [Delphi Group at
CMU](https://delphi.cmu.edu/) to make these data available through
their [Delphi Epidata
API](https://cmu-delphi.github.io/delphi-epidata/api/README.html).
The current weekly timeseries of the hospitalization data as well as
prior versions of the data are available as the [`covid_hosp`
endpoint of the
API](https://cmu-delphi.github.io/delphi-epidata/api/covid_hosp.html).
This endpoint is also available through the [COVIDcast
Epidata API](https://cmu-delphi.github.io/delphi-epidata/api/covidcast-signals/hhs.html).

### Data processing

The hospitalization truth data is computed based on the `previous_day_admission_influenza_confirmed`
field which provides the new daily admissions with a confirmed diagnosis of influenza.

Since these admission data are listed as “previous day” admissions in
the raw data, the truth data shifts values in the `date` column one day
earlier so that `inc hosp` align with the date the admissions occurred.

As an example, the following data from HealthData.gov

       date    | previous_day_admission_influenza_confirmed 
    -----------|--------------------------------------------
    2020-10-30 |                  5                         

would turn into the following observed data for *daily* incident
hospitalizations

       date    | incident_hospitalizations
    -----------|----------------------------
    2020-10-29 |          5               

National hospitalization, i.e. US, data are constructed from these data
by summing the data across all 50 states, Washington DC (DC), Puerto
Rico(PR), and the US Virgin Islands (VI). The HHS data do not include
admissions for additional territories.

Daily admission counts are then aggregated into epidemiological weeks. 

For week-ahead forecasts, we will use the specification of
epidemiological weeks (EWs) [defined by the US
CDC](https://wwwn.cdc.gov/nndss/document/MMWR_Week_overview.pdf) which
run Sunday through Saturday. There are standard software packages to
convert from dates to epidemic weeks and vice versa. E.g.
[MMWRweek](https://cran.r-project.org/web/packages/MMWRweek/) for R and
[pymmwr](https://pypi.org/project/pymmwr/) and
[epiweeks](https://pypi.org/project/epiweeks/) for python.

### Additional resources

Here are a few additional resources that describe these hospitalization
data:

-   [data dictionary for the
    dataset](https://healthdata.gov/Hospital/COVID-19-Reported-Patient-Impact-and-Hospital-Capa/g62h-syeh)
-   the [official document describing the “guidance for hospital
    reporting”](https://www.hhs.gov/sites/default/files/covid-19-faqs-hospitals-hospital-laboratory-acute-care-facility-data-reporting.pdf)


Accessing truth data
----------
While we go to some pains to create accurate, verified, clean versions of the truth data, these should be seen as secondary sources to the original data at the HHS Protect site.

### CSV files
A set of comma-separated plain text files are automatically updated every week with the latest observed values for incident hospitalizations. A corresponding CSV file is created in `data-truth/truth-Incident Hospitalizations.csv`.

