import os
from calendar import monthrange

script_dir = os.path.dirname(os.path.realpath(__file__))
data_location = '../../Data/Weather/Ottawa 4327/Hourly/2012To2018OttawaGatineau/'

# helper method for parsing meta data from top of file
def get_next_meta(meta_name,lines):
  if len(lines) == 0:
    return ""
  line = lines.pop(0)
  if meta_name not in line:
    return get_next_meta(meta_name,lines)
  return line.split(",")[1].strip('\n')

# Over all the files
for year in range(2012,2019):
  for month in range(1,13):
    days_in_month = monthrange(year, month)[1]

    # Get all lines from the original data file
    original_filename = 'eng-hourly-{1:02d}01{0:02d}-{1:02d}{2:02d}{0:04d}.csv'.format(year, month, days_in_month)
    rel_path = data_location + original_filename
    abs_file_path = os.path.join(script_dir, rel_path)
    original_file = open(abs_file_path, 'r')
    original_file_lines = original_file.readlines()

    # Collect all the meta data from the top of the file
    meta_station = get_next_meta("Station Name", original_file_lines)
    meta_province = get_next_meta("Province", original_file_lines)
    meta_lat = get_next_meta("Latitude", original_file_lines)
    meta_long = get_next_meta("Longitude", original_file_lines)
    meta_elev = get_next_meta("Elevation", original_file_lines)
    meta_climate_id = get_next_meta("Climate Identifier", original_file_lines)

    get_next_meta("Date/Time", original_file_lines)

    # Format the meta data into a CSV string
    seperator = ','
    meta_columns = [meta_station, meta_province, meta_lat, meta_long, meta_elev, meta_climate_id ]
    meta_columns = [meta_station, meta_province, meta_lat, meta_long, meta_elev, meta_climate_id ]
    meta_columns_string = seperator.join(meta_columns)
    
    if len(original_file_lines) > 0:
      # Put the CSV from the original data file (along with the meta data) into a CSV file
      output_filename = 'weather_data/OttawaGatineau_hourly_{0:04d}{1:02d}.csv'.format(year, month)
      output_file = open(output_filename,"w")
      output_file.write('"Station Name","Province","Latitude","Longitude","Elevation","Climate Identifier","Date/Time","Year","Month","Day","Time","Temp (C)","Temp Flag","Dew Point Temp (C)","Dew Point Temp Flag","Rel Hum (%)","Rel Hum Flag","Wind Dir (10s deg)","Wind Dir Flag","Wind Spd (km/h)","Wind Spd Flag","Visibility (km)","Visibility Flag","Stn Press (kPa)","Stn Press Flag","Hmdx","Hmdx Flag","Wind Chill","Wind Chill Flag","Weather"\n') 
      for data_line in original_file_lines:
        data = data_line.split(",")
        if (len(data) >= 24): # quick filter to remove lines that only have the date and time
          output_file.write(meta_columns_string + ',' + data_line) 

          
      output_file.close()
