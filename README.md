# tf-keras-demo
A simple neural network example using TensorFlow Keras.

## Getting started

### Prerequisites

This project was compiled with Python 2.7.13 ([downloadable from python.org](https://www.python.org/downloads/release/python-2713/))

### Installing

This project uses 
1. TensorFlow version 1.12.0 `pip install tensorflow`
2. Keras version 2.1.6-tf `pip install keras`


## Fetching data

Data for this demonstration was retrieved from the Government of Canada's [historical data portal](http://climate.weather.gc.ca/historical_data/search_historic_data_e.html)

Specifically, the following command was used to download the 2012-2018 weather data from an Ottawa-Gatineau weather station:
```
for year in `seq 2012 2018`;do for month in `seq 1 12`;do wget --content-disposition "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=50719&Year=${year}&Month=${month}&Day=14&timeframe=1&submit= Download+Data" ;done;done
```

### Data cleaning

The data comes with several lines of meta data at the top of each file like the sample below.

```
"Station Name","OTTAWA GATINEAU A"
"Province","QUEBEC"
"Latitude","45.52"
"Longitude","-75.56"
"Elevation","64.30"
"Climate Identifier","7032682"
"WMO Identifier",""
"TC Identifier","YND"
"All times are specified in Local Standard Time (LST). Add 1 hour to adjust for Daylight Saving Time where and when it is observed."

"Legend"
"E","Estimated"
"M","Missing"
"NA","Not Available"
```

`unify_data.py` iterates through all the files and integrates this data into the CSV format with all the other data. The script also removes lines with no weather data (many instances include only the date and time).

You should update the `data_location` variable at the top of the script to point to the location where you downloaded the files from the historical data portal.

### Data investigation

The `examine_data.py` script iterates through the unified data and outputs the number of records for each feature/column. This helps us identify which fields are most often present or missing. 

## Models

A very simple model is created to effectively perform a linear regression. 

## Authors

* Rachel Hartviksen

## Motivation

This project was create for a neural networks [lecture and demonsation](https://www.meetup.com/Ottawa-Ladies-Code-Club/events/256395335/) for the [Ottawa Ladies Code Club](https://www.meetup.com/Ottawa-Ladies-Code-Club/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Official TensorFlow Keras documentation](https://www.tensorflow.org/guide/keras)
* [Official Keras documentation](https://keras.io/)