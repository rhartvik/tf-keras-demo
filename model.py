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
  filtered_frame = data[["Month","Day","Time","Temp (C)","Dew Point Temp (C)","Rel Hum (%)","Wind Dir (10s deg)","Wind Spd (km/h)"]]
  filtered_frame['Time'] = filtered_frame['Time'].map(lambda time: int(time[:-3])) #convert time to hour as int
  x = filtered_frame.values

  temperature = data[["Temp (C)","Hmdx","Wind Chill"]]
  y = temperature.apply(lambda row: row["Hmdx"] if not_empty(row["Hmdx"]) else row["Wind Chill"] if not_empty(row["Wind Chill"]) else row["Temp (C)"], axis=1).values
  return DataSet(x,y)


def get_all_data(start_year, start_month, end_year, end_month):
  year = start_year
  month = start_month
  monthly_data = get_data(year, month)
  x = monthly_data.x
  y = monthly_data.y
  month += 1
  if (month == 13):
    month = 1
    year += 1
  while (year <= end_year and month <= end_month):
    monthly_data = get_data(year, month)
    x = np.append(x,monthly_data.x, axis=0)
    y = np.append(y,monthly_data.y, axis=0)
    month += 1
    if (month == 13):
      month = 1
      year += 1
  return DataSet(x,y)

# Get training, test, validation data
training_data = get_data(2018,6)
training_data_large = get_all_data(2016,4,2018,6)
test_data = get_data(2017,6)
validation_data = get_data(2016,6)


# Create models
models = []

# Reduce the learning rate
sgd = tf.keras.optimizers.SGD(lr=0.001, momentum=0.0, decay=0.0001, nesterov=False)

# Model 1
model1 = tf.keras.Sequential()
model1.add(layers.BatchNormalization())
model1.add(layers.Dense(30, activation='hard_sigmoid', kernel_initializer='random_uniform'))
model1.add(layers.Dense(1))
model1.compile(loss='mean_squared_error', optimizer=sgd)
models.append(model1)

for model in models:
  print '********************************** Model evaluation **********************************'
  # more epochs
  model.fit(training_data.x, training_data.y, epochs=200, batch_size=10, verbose=1,validation_data=(validation_data.x, validation_data.y))
  print len(model.layers)

  for layer in model.layers:
    print ('weights', layer.get_weights()[0])
    print ('biases', layer.get_weights()[1])
  predictions = model.predict(test_data.x)

  print('Examples:')
  for i in range(0,10):
    index = i * 10
    #print('Example ',i, test_data.x[index])
    print('Prediction', index, predictions[index][0], ' actual ', test_data.y[index])

  score = model.evaluate(test_data.x,test_data.y, verbose=1) #bah
  print('Test loss:', score)
