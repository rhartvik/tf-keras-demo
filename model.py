# Test the model with a small set of data 

import tensorflow as tf
import numpy as np
import tensorflow.keras.layers as layers
import pandas as pd # used for csv reading
import math # used to check for nan values while calculating the "feels like" temperature
import collections # Used to return x and y from data fetching helper function

pd.options.mode.chained_assignment = None

def not_empty(val):
  if math.isnan(val):
    return False
  if val == "":
    return False
  if val == "NaN":
    return False
  return True

DataSet = collections.namedtuple('DataSet', ['x', 'y'])

def get_data(year,month):
  file = open('weather_data/OttawaGatineau_hourly_{0:04d}{1:02d}.csv'.format(year,month),'r')
  data = pd.read_csv(file, delimiter=',',quotechar='"',quoting=1)
  filtered_frame = data[["Year","Month","Day","Time","Temp (C)","Dew Point Temp (C)","Rel Hum (%)","Wind Dir (10s deg)","Wind Spd (km/h)","Visibility (km)","Stn Press (kPa)"]]
  filtered_frame['Time'] = filtered_frame['Time'].map(lambda time: int(time[:-3])) #convert time to hour as int
  x = filtered_frame.values

  temperature = data[["Temp (C)","Hmdx","Wind Chill"]]
  y = temperature.apply(lambda row: row["Hmdx"] if not_empty(row["Hmdx"]) else row["Wind Chill"] if not_empty(row["Wind Chill"]) else row["Temp (C)"], axis=1).values
  output_file = open('y.txt',"w")
  for label in y:
    output_file.write('%s\n' % label)
  output_file.close()
  return DataSet(x,y)

# Get training, test, validation data
training_data = get_data(2018,6)
test_data = get_data(2017,6)
validation_data = get_data(2016,6)


# Create model
model = tf.keras.Sequential()
  # Hidden layer
model.add(layers.BatchNormalization())
model.add(layers.Dense(10, activation='hard_sigmoid', kernel_initializer='normal'))
  # Add an output layer:
model.add(layers.Dense(1))

sgd = tf.keras.optimizers.SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
model.compile(loss='mean_squared_error', optimizer=sgd)

model.fit(training_data.x, training_data.y, epochs=10, batch_size=10, verbose=1,validation_data=(validation_data.x, validation_data.y))

predictions = model.predict(test_data.x)

print('Examples:')
for i in range(0,10):
  index = i * 20
  #print('Example ', i, test_data.x[index])
  print('Prediction', index, predictions[index][0], ' actual ', test_data.y[index])
