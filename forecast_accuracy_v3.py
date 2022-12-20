# a script that will compare the forecasted weather to the true weather after it occurs
import requests
import psycopg2
from datetime import datetime
import time
import csv

#using API from https://open-meteo.com/

def get_weather():
    #get data from url
    timestamp = datetime.now()
    print("Starting at: " + str(timestamp))

    #gathers data for St. Catharines, Ontario every hour
    url = 'https://api.open-meteo.com/v1/forecast?latitude=43.14&longitude=-79.20&hourly=temperature_2m,relativehumidit\
y_2m,dewpoint_2m,apparent_temperature,precipitation,rain,showers,snowfall,snow_depth,pressure_msl,surface_pressure,\
cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,visibility,windspeed_10m,winddirection_10m,windgusts_10m,s\
oil_temperature_0cm,soil_temperature_6cm,soil_temperature_18cm,soil_temperature_54cm,soil_moisture_0_1cm,soil_moist\
ure_1_3cm,soil_moisture_3_9cm,soil_moisture_9_27cm,soil_moisture_27_81cm&daily=temperature_2m_max,temperature_2m_mi\
n,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,precipitation_sum,rain_sum,showers_sum,snowfall_\
sum,precipitation_hours,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,shortwave_radiation_sum,et0_\
fao_evapotranspiration&current_weather=true&timezone=America%2FNew_York'
    webpage = requests.get(url)
    data = webpage.json()
    #main data sets
    current_weather = data["current_weather"]
    current_time = current_weather["time"]
    daily_forecast = data["daily"]
    daily_time = daily_forecast["time"]
    current_slice = []
    daily_slice = []
    hourly_slice = []
    def get_current_weather():
        #puts the data from the current weather section into a single list/row to be written later
        print("Processing current weather..")
        current_temp = current_weather["temperature"]
        current_windspeed = current_weather['windspeed']
        current_wind_dir = current_weather['winddirection']
        current_slice.append(current_time)
        current_slice.append(daily_time[1])
        current_slice.append(current_temp)
        current_slice.append(current_windspeed)
        current_slice.append(current_wind_dir)
        current_slice.append("Current")
        print("Processing complete.")
        print("Current weather: " + str(current_slice))
    def get_daily_forecast():
        #parses out the daily forecast time segments into lists/rows to be written later
        print("Processing daily forecast..")
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
            daily_slice.append(days_forecast)
        print("Processing complete.")
        print("Example row of daily forecast data: " + str(daily_slice[0]))
    def get_hourly_forecast():
        #parses out the hourly forecast time segments into lists/rows to be written later
        hourly_forecast = data['hourly']
        hourly_time = hourly_forecast['time']
        print("Processing hourly forecast..")
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
            hourly_slice.append(hours_forecast)
        print("Processing complete.")
        print("Example row of hourly forecast data: " + str(hourly_slice[0]))
    def write_to_database():
        #connects to the postgresql database and enters information
        conn = psycopg2.connect(
            database="Weather",
            user='postgres',
            password='Bandit1(',
            host='localhost',
            port='5432')
        cursor = conn.cursor()
        cursor.execute("INSERT into weather(pull_time,\
forecast_date,\
current_temp,\
current_windspeed,\
current_wind_direction,\
batch) VALUES (%s, %s, %s, %s, %s, %s)", current_slice)
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
        print("Committing...")
        conn.commit()
        print("Closing connection.")
        conn.close()
    def write_to_csv():
        print("Writing to csv.")

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
        headers = cursor.fetchall()
        header_list = []
        for i in headers:
            header_list.append(i[0])

        # extract data from table
        cursor.execute("select * from weather;")
        # save all data to variable
        data = cursor.fetchall()
        datarows = []
        for i in data:
            datarows.append(i)

        # close connection
        cursor.close()
        conn.close()

        print(f"Number of rows: {len(data)}")
        print(f"Number of columns: {len(header_list)}")

        # write to csv
        filepath = (r'C:\Users\TPC19\Dropbox\Coding\TEST\weather_data.csv')
        with open(filepath, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header_list)
            for i in datarows:
                writer.writerow(i)
    def closing_summary():
        #prints a simple time stampt and run time to console
        timestamp2 = datetime.now()
        print("Ending at: " + str(timestamp2))
        run_time = timestamp2 - timestamp
        print("Run time: " + str(run_time))
    def run_subtasks():
        #called each of the functions above
        get_current_weather()
        get_daily_forecast()
        get_hourly_forecast()
        write_to_database()
        write_to_csv()
        closing_summary()
    run_subtasks()

def timer():
    #timer will cycle and when one or both of the trigger dates below are True the functions will be called
    #unsure of when the data is updated. Running on 50th minute arbitrarily to avoid on the hour issues
    current_time = datetime.now()
    minute = current_time.strftime("%M")
    trigger_time = (minute == "10")
    if trigger_time is True:
        print("Fetching current weather and forecast at: " + str(current_time))
        try:
            get_weather()
        except:
            print("An error occurred when gathering weather data at: " + str(current_time))
            time.sleep(5)
            try:
                get_weather()
            except:
                print("A second error occurred when gathering weather data at: " + str(current_time))
                print("No data for this hour. :(")
        print("Sleeping for 60 seconds.")
        time.sleep(60)
        print("Waking.")
    time.sleep(15)

def run():
    x = True
    while (x):
        timer()

run()