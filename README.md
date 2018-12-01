# tf-keras-demo
A simple neural network example using TensorFlow Keras.

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