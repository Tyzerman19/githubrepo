# write a script to take my weather data and send email to myself every morning with the forecast

# import libraries
import pandas as pd
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

print("Weather data collected at: " + str(timestamp))

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

# create main partition
hourly_forecast = data['hourly']

# extract individual variables
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

df = pd.DataFrame(
    {'Date': hourly_time,
     'Temperature': hourly_temp,
     'Humidity': hourly_humidity,
     'Feels Like': hourly_app_temp,
     'Precipitation': hourly_precip,
     'Cloud Cover': hourly_cloud_cover,
     'Wind Speed': hourly_windspeed,
     'Gusts': hourly_wind_gusts})

df['Date'] = pd.to_datetime(df['Date'])
max_temp = df['Temperature'].max()
min_temp = df['Temperature'].min()

print(df)
print(df.dtypes)
print(df.info())

# one day's data

today_stamp = datetime.now() + timedelta(days=1)
today_stamp = today_stamp.strftime('%Y-%m-%d 00:00:00')
today_stamp = datetime.strptime(today_stamp, '%Y-%m-%d %H:%M:%S')
print(today_stamp)

today = df.loc[df['Date'] < today_stamp]



print(today)


# temp = today.plot.line(
#     x='Date',
#     xlabel='Time',
#     y='Temperature',
#     ylim=[-20,40]
#     )
# zero_line = plt.axhline(y=0, color='b', linestyle='--')
# precip = today.plot.line(x='Date', y='Precipitation')
# plt.show()

fig, axes = plt.subplots(2,1)

temp = axes[0]
today.plot(x='Date',y='Temperature',ylim=[min_temp, max_temp],ax=temp)
temp.axhline(0, color='b',linestyle='--')


precip = axes[1]
today.plot(x='Date',y='Precipitation',ylim=[0,5],ax=precip, kind='bar')
precip.axhline(0.5, color='b',linestyle='--',label='Light')
precip.axhline(4, color='b',linestyle='--')

plt.show()