import os

script_dir = os.path.dirname(os.path.realpath(__file__))

counts = [0] * 30
empty_string = '""'
# Over all the new csv files
for year in range(2012,2019):
  for month in range(1,13):

    # Get all lines from the csv
    csv_filename = 'weather_data/OttawaGatineau_hourly_{0:04d}{1:02d}.csv'.format(year, month)
    abs_file_path = os.path.join(script_dir, csv_filename)
    csv_file = open(abs_file_path, 'r')
    csv_file_lines = csv_file.readlines()
    headers = csv_file_lines.pop().split(",")

    # Count how many are non-empty
    for data_line in csv_file_lines:
      data = data_line.split(",")
      for col_index in range(0,30):
        if (data[col_index] != empty_string):
          counts[col_index] += 1
total = counts[0]

# Print the counts in an easy to read format
for col_index in range(0,len(headers)):
  prefix = "{0}  {1}:".format(col_index, headers[col_index])
  num_tabs = 4 - len(prefix) / 8
  nonzero_fraction = "{0} / {1}".format(counts[col_index], total).rjust(13)
  print "{0}{1}{2}".format(prefix, "\t"*num_tabs, nonzero_fraction) 

# Identify significant columns
threshold = 30000
sig_columns = ''
for col_index in range(0,len(headers)):
  if counts[col_index] > threshold:
    sig_columns += headers[col_index] + ","
print "Significant columns: {0}".format(sig_columns)