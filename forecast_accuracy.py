# collect online local weather data every hour
# store the data 
# analyze the data to compare accuracy of forecasted data to the real weather on that day

# import libraries 
import requests
import psycopg2
from datetime import datetime
import time
import csv


def get_weather():
    # this function will collect weather data through a free API

    timestamp = datetime.now()

    print("Starting at: " + str(timestamp))

    # using API from https://open-meteo.com/
    # the below url will gather data for St. Catharines, Ontario once per hour

    url = 'https://api.open-meteo.com/v1/forecast?latitude=43.14&longitude=-79.20&hourly=temperature_2m,relativehumidit\
y_2m,dewpoint_2m,apparent_temperature,precipitation,rain,showers,snowfall,snow_depth,pressure_msl,surface_pressure,\
cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,visibility,windspeed_10m,winddirection_10m,windgusts_10m,s\
oil_temperature_0cm,soil_temperature_6cm,soil_temperature_18cm,soil_temperature_54cm,soil_moisture_0_1cm,soil_moist\
ure_1_3cm,soil_moisture_3_9cm,soil_moisture_9_27cm,soil_moisture_27_81cm&daily=temperature_2m_max,temperature_2m_mi\
n,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,precipitation_sum,rain_sum,showers_sum,snowfall_\
sum,precipitation_hours,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,shortwave_radiation_sum,et0_\
fao_evapotranspiration&current_weather=true&timezone=America%2FNew_York'
    
    # get the data from web as a json

    webpage = requests.get(url)
    data = webpage.json()
    
    # divide the data into a few main data sets

    current_weather = data["current_weather"]
    current_time = current_weather["time"]
    daily_forecast = data["daily"]
    daily_time = daily_forecast["time"]
    
    # create an empty list for each 'slice' of data that we will retain
    
    current_slice = []
    daily_slice = []
    hourly_slice = []

    def get_current_weather():
        
        # this function will create a single slice of data from the current weather set
        # this slice represents the current weather conditions

        print("Processing current weather..")

        # find current weather data

        current_temp = current_weather["temperature"]
        current_windspeed = current_weather['windspeed']
        current_wind_dir = current_weather['winddirection']

        # append the current data to a list

        current_slice.append(current_time)
        current_slice.append(daily_time[1])
        current_slice.append(current_temp)
        current_slice.append(current_windspeed)
        current_slice.append(current_wind_dir)
        current_slice.append("Current")

        print("get_current_weather function end.")    
    
    def get_daily_forecast():
        
        # this function will create a single slice of data from the daily forecast set
        # this slice represents daily forecast variables 

        # find daily forecast data sets

        daily_temp_max = daily_forecast["temperature_2m_max"]
        daily_temp_min = daily_forecast["temperature_2m_min"]
        daily_apptemp_max = daily_forecast["apparent_temperature_max"]
        daily_apptemp_min = daily_forecast["apparent_temperature_min"]
        daily_precip = daily_forecast["precipitation_sum"]
        daily_rain = daily_forecast["rain_sum"]
        daily_showers = daily_forecast["showers_sum"]
        daily_snow = daily_forecast["snowfall_sum"]
        daily_precip_hours = daily_forecast["precipitation_hours"]
        daily_wind_max = daily_forecast["windspeed_10m_max"]
        daily_wind_gust_max = daily_forecast["windgusts_10m_max"]
        daily_wind_dir = daily_forecast["winddirection_10m_dominant"]
        daily_shortwave_rad_sum = daily_forecast["shortwave_radiation_sum"]
        daily_evapotranspiration =daily_forecast["et0_fao_evapotranspiration"]

        for day in range(len(daily_time)):
            
            # for each day in the forecast isolate that day's variables
            # append those variables to a list for each timepoint

            days_forecast = []

            days_forecast.append(current_time)
            days_forecast.append(daily_time[day])
            days_forecast.append(daily_temp_min[day])
            days_forecast.append(daily_temp_max[day])
            days_forecast.append(daily_apptemp_max[day])
            days_forecast.append(daily_apptemp_min[day])
            days_forecast.append(daily_precip[day])
            days_forecast.append(daily_rain[day])
            days_forecast.append(daily_showers[day])
            days_forecast.append(daily_snow[day])
            days_forecast.append(daily_precip_hours[day])
            days_forecast.append(daily_wind_max[day])
            days_forecast.append(daily_wind_gust_max[day])
            days_forecast.append(daily_wind_dir[day])
            days_forecast.append(daily_shortwave_rad_sum[day])
            days_forecast.append(daily_evapotranspiration[day])
            days_forecast.append("Daily")

            # append this list for each do to the dataset for all daily forecasts 

            daily_slice.append(days_forecast)
        
        print("get_daily_forecast function end.")
    
    def get_hourly_forecast():

        # this function will create a single slice of data from the hourly forecast set
        # this slice represents hourly forecast variables 
        
        hourly_forecast = data['hourly']
        hourly_time = hourly_forecast['time']
        
        hourly_temp = hourly_forecast["temperature_2m"]
        hourly_humidity = hourly_forecast["relativehumidity_2m"]
        hourly_dewpoint = hourly_forecast["dewpoint_2m"]
        hourly_app_temp = hourly_forecast["apparent_temperature"]
        hourly_precip = hourly_forecast["precipitation"]
        hourly_rain = hourly_forecast["rain"]
        hourly_showers = hourly_forecast["showers"]
        hourly_snow = hourly_forecast["snowfall"]
        hourly_snow_depth = hourly_forecast["snow_depth"]
        hourly_msl_pressure = hourly_forecast["pressure_msl"]
        hourly_surface_pressure = hourly_forecast["surface_pressure"]
        hourly_cloud_cover = hourly_forecast["cloudcover"]
        hourly_visibility = hourly_forecast["visibility"]
        hourly_windspeed = hourly_forecast["windspeed_10m"]
        hourly_wind_dir = hourly_forecast["winddirection_10m"]
        hourly_wind_gusts = hourly_forecast["windgusts_10m"]
        hourly_soil_temp_0cm = hourly_forecast["soil_temperature_0cm"]
        hourly_soil_temp_6cm = hourly_forecast["soil_temperature_6cm"]
        hourly_soil_temp_18cm = hourly_forecast["soil_temperature_18cm"]
        hourly_soil_temp_54cm = hourly_forecast["soil_temperature_54cm"]
        hourly_soil_moisture_0_1cm = hourly_forecast["soil_moisture_0_1cm"]
        hourly_soil_moisture_1_3cm = hourly_forecast["soil_moisture_1_3cm"]
        hourly_soil_moisture_3_9cm = hourly_forecast["soil_moisture_3_9cm"]
        hourly_soil_moisture_9_27cm = hourly_forecast["soil_moisture_9_27cm"]
        hourly_soil_moisture_27_81cm = hourly_forecast["soil_moisture_27_81cm"]
        
        for hour in range(len(hourly_time)):

            # for each hour in the hourly forecast isolate that hour's variables
            # append those variables to a list for each timepoint

            hours_forecast = []

            hours_forecast.append(current_time)
            hours_forecast.append(hourly_time[hour])
            hours_forecast.append(hourly_temp[hour])
            hours_forecast.append(hourly_humidity[hour])
            hours_forecast.append(hourly_dewpoint[hour])
            hours_forecast.append(hourly_app_temp[hour])
            hours_forecast.append(hourly_precip[hour])
            hours_forecast.append(hourly_rain[hour])
            hours_forecast.append(hourly_showers[hour])
            hours_forecast.append(hourly_snow[hour])
            hours_forecast.append(hourly_snow_depth[hour])
            hours_forecast.append(hourly_msl_pressure[hour])
            hours_forecast.append(hourly_surface_pressure[hour])
            hours_forecast.append(hourly_cloud_cover[hour])
            hours_forecast.append(hourly_visibility[hour])
            hours_forecast.append(hourly_windspeed[hour])
            hours_forecast.append(hourly_wind_dir[hour])
            hours_forecast.append(hourly_wind_gusts[hour])
            hours_forecast.append(hourly_soil_temp_0cm[hour])
            hours_forecast.append(hourly_soil_temp_6cm[hour])
            hours_forecast.append(hourly_soil_temp_18cm[hour])
            hours_forecast.append(hourly_soil_temp_54cm[hour])
            hours_forecast.append(hourly_soil_moisture_0_1cm[hour])
            hours_forecast.append(hourly_soil_moisture_1_3cm[hour])
            hours_forecast.append(hourly_soil_moisture_3_9cm[hour])
            hours_forecast.append(hourly_soil_moisture_9_27cm[hour])
            hours_forecast.append(hourly_soil_moisture_27_81cm[hour])
            hours_forecast.append("Hourly")

            # append this list for each do to the dataset for all hourly forecasts 

            hourly_slice.append(hours_forecast)
        
        print("get_hourly_forecast function end.")

    def write_to_database():
        
        # a function to write the data slices into a database

        #connect to local postgresql database
        
        conn = psycopg2.connect(
            database="Weather",
            user='postgres',
            password='Bandit1(',
            host='localhost',
            port='5432')
        
        # create cursor object
        
        cursor = conn.cursor()
        
        # insert data from current slice
        
        cursor.execute("INSERT into weather(pull_time,\
                        forecast_date,\
                        current_temp,\
                        current_windspeed,\
                        current_wind_direction,\
                        batch) VALUES (%s, %s, %s, %s, %s, %s)", current_slice)
        
        # insert each day's data from daily slice
        
        for day in daily_slice:
            
            cursor.execute("INSERT into weather(pull_time,\
                            forecast_date,\
                            daily_temp_min,\
                            daily_temp_max,\
                            daily_app_temp_max,\
                            daily_app_temp_min,\
                            daily_precipitation,\
                            daily_rain,\
                            daily_showers,\
                            daily_snow,\
                            daily_precip_hours,\
                            daily_wind_max,\
                            daily_wind_gust,\
                            daily_wind_direction,\
                            daily_shortwave_rad_sum,\
                            daily_evapotranspiration,\
                            batch) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s)", day)
        
        # insert data for each hour in hourly slice

        for hour in hourly_slice:
            
            cursor.execute("INSERT into weather(pull_time,\
                            forecast_date,\
                            hourly_temperature,\
                            hourly_humidity,\
                            hourly_dew_point,\
                            hourly_apparent_temperature,\
                            hourly_precipitation,\
                            hourly_rain,\
                            hourly_showers,\
                            hourly_snow,\
                            hourly_snow_depth,\
                            hourly_msl_pressure,\
                            hourly_surface_pressure,\
                            hourly_cloud_cover,\
                            hourly_visibility,\
                            hourly_windspeed,\
                            hourly_wind_dir,\
                            hourly_wind_gusts,\
                            hourly_soil_temp_0cm,\
                            hourly_soil_temp_6cm,\
                            hourly_soil_temp_18cm,\
                            hourly_soil_temp_54cm,\
                            hourly_soil_moisture_0_1cm,\
                            hourly_soil_moisture_1_3cm,\
                            hourly_soil_moisture_3_9cm,\
                            hourly_soil_moisture_9_27cm,\
                            hourly_soil_moisture_27_81cm,\
                            batch) VALUES (%s, %s, %s, %s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", hour)
        
        # commit and close the connection

        conn.commit()
        
        conn.close()

        print("write_to_database function end.")
    
    def write_to_csv():
        
        # function to read all data from database and write data to csv file

        # connect to database

        conn = psycopg2.connect(
            database="Weather",
            user='postgres',
            password='Bandit1(',
            host='localhost',
            port='5432')

        # create cursor instance

        cursor = conn.cursor()

        # extract column names from table

        cursor.execute("""SELECT 
            column_name 
            FROM 
            information_schema.columns 
            where 
            table_name = 'weather' 
            order by 
            ordinal_position;""")
        
        # create a list of column names

        headers = cursor.fetchall()
        header_list = []

        for i in headers:
            header_list.append(i[0])

        # extract data from table

        cursor.execute("select * from weather;")
        data = cursor.fetchall()
        
        # save data to a list

        datarows = []

        for i in data:
            datarows.append(i)

        # close connection

        cursor.close()
        conn.close()

        # identify filepath to write to

        filepath = (r'C:\Users\TPC19\Dropbox\Coding\Python Folder\weather_data.csv')
        
        # write all data to csv, overwrite old file

        with open(filepath, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header_list)
            for i in datarows:
                writer.writerow(i)

        print("write_to_csv function end.")

    def closing_summary():

        #prints a simple time stamp and run time to console

        timestamp2 = datetime.now()
        run_time = timestamp2 - timestamp

        print("Ending at: " + str(timestamp2))
        print("Run time: " + str(run_time))

    def run_subtasks():

        # runs a cycle through each function above 

        # gathering functions
        get_current_weather()
        get_daily_forecast()
        get_hourly_forecast()

        #writing functions
        write_to_database()
        write_to_csv()

        # summary function
        closing_summary()

    run_subtasks()

def timer():

    # the timer continuously ticks at a specified interval and executes the get_weather function when the trigger time is met
    # unsure of when the data is updated so the data is gathered on 10th minute of the hour to avoid on the hour issues

    # indentify time

    current_time = datetime.now()
    minute = current_time.strftime("%M")

    # identify when to run the get_weather function

    trigger_time = (minute == "10")

    if trigger_time is True:
        print("Fetching current weather and forecast at: " + str(current_time))

        try:
            get_weather()

        except:

            # if get_weather fails wait some time and try again

            print("An error occurred when gathering weather data at: " + str(current_time))
            
            time.sleep(30)
            
            try:
                get_weather()

            except:

                # will not try again for this hour

                print("A second error occurred when gathering weather data at: " + str(current_time))
                print("No data for this hour. :(")

        # sleep for a full minute to ensure that we won't pull the same data for this hour

        time.sleep(60)

    time.sleep(15)

def run():

    # a basic function to run indefinitely 

    x = True
    
    while (x):
        timer()

run()
