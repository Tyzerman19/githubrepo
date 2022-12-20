#import modules

import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

# pandas slice warning silence
pd.options.mode.chained_assignment = None  # default='warn'


#establish classes

class Linegraph:
    def __init__(self, x_axis, y_axis, var, std_high, std_low):
        self.x = x_axis
        self.y = y_axis
        self.var = var
        self.std_high = std_high
        self.std_low = std_low

    #function to draw the graph
    def draw_linegraph(self):
        x = self.x
        y = self.y
        var = self.var
        std_high = self.std_high
        std_low = self.std_low
        graph, plot1 = plt.subplots()
        plt.plot(x, y)
        plt.plot(x, std_low, linestyle='--')
        plt.plot(x, std_high, linestyle='--')
        plt.title(f"{var} Forecast Error by Day")
        plt.xlabel("Days Before Forecast")
        plt.ylabel("Absolute Difference Between Predicted Daily Mean and True Value")
        plot1.invert_xaxis()
        plt.show()

# create dataframe from csv

data = pd.read_csv('weather_data.csv')

#create dataframe for current weather dataset
current_all = data[['pull_time',
                    'current_temp',
                    'current_windspeed',
                    'current_wind_direction']]

# get rid of rows without current temperature data - acts to keep the current batch
current = current_all[(current_all['current_temp'].notnull())].reset_index()

#change pull_time string to datetime object
current['pull_time'] = current['pull_time'].apply(lambda x:pd.to_datetime(x, format='%Y-%m-%dT%H:%M'))

#drop old index column
current = current.drop(['index'], axis=1)

#create dataframe for forecast weather dataset
forecast_all = data[['pull_time',
                     'forecast_date',
                     'hourly_temperature',
                     'hourly_humidity',
                     'hourly_precipitation',
                     'hourly_rain',
                     'hourly_showers',
                     'hourly_snow',
                     'hourly_snow_depth',
                     'hourly_surface_pressure',
                     'hourly_visibility',
                     'hourly_windspeed',
                     'hourly_wind_dir',
                     'hourly_wind_gusts']]

#drop rows with no hourly_temperature data - acts to keep the 'hourly' batch
forecast = forecast_all[(forecast_all['hourly_temperature'].notnull())].reset_index()

#convert pull_time and forecast_date strings to datetime
forecast[['pull_time','forecast_date']] = forecast[['pull_time','forecast_date']].apply(lambda x:pd.to_datetime(x, format='%Y-%m-%dT%H:%M'))

#drop old index column
forecast = forecast.drop(['index'],axis=1)

#
# we now have both a "current" dataframe and a "forecast" dataframe
#

# create a function to analyze the change in average forecasted variable over time for days before forecast date
def grouped_by_day_column_stats(variable):
    #edit df so that ANY column/variable from the raw data can be specified
    cumulative_df = pd.DataFrame(columns=['Forecast_Time', 'Days_Before', 'True_Value', 'min', 'max', 'mean',
                                                'std'])
    var = variable

    for time in forecast['forecast_date'].unique():
        if len(forecast[forecast['forecast_date'] == time]) == 168:

            #pull data for only one "pull_date" value
            time_slice = forecast[forecast['forecast_date'] == time].sort_values('pull_time').reset_index(drop=True)
            time_slice = time_slice[['pull_time', 'forecast_date', var]]

            # measure the difference between the true variable value and the forecasted variable value
            true_value = time_slice[var].iloc[-1]

            # add column to measure difference between forecasted temp and true temp
            time_slice['value_difference'] = time_slice[var] - (true_value)

            # add column to track "day"
            time_slice['pull_day'] = time_slice['pull_time'].dt.date

            # group data by day
            day_grouped = time_slice.groupby('pull_day')

            # create an aggregate table
            agg_table = day_grouped[['value_difference']].aggregate([min, max, 'mean', 'std']).reset_index()

            # create and clean a final table with the columns of interest
            final_table = agg_table[[('value_difference', 'min'),
                                   ('value_difference', 'max'),
                                   ('value_difference', 'mean'),
                                   ('value_difference', 'std')]]
            final_table.insert(0, ('', 'Days_Before'), range(6, -1, -1))
            final_table.insert(0, ('', 'Forecast_Time'), time)
            final_table.insert(2, ('', 'True_Value'), true_value)
            final_table.columns = final_table.columns.droplevel()

            # add to dataframe outside of the function
            cumulative_df = pd.concat([cumulative_df, final_table])

    #tidy cumulative table to finalize
    cumulative_df = cumulative_df.reset_index(drop=True)
    number_of_slices = len(cumulative_df['Forecast_Time'].unique())

    #prep days before
    mean_std_by_day = cumulative_df[['Days_Before', 'mean', 'std']]
    mean_std_by_day['mean'] = mean_std_by_day['mean'].abs()
    mean_std_by_day['std_high'] = mean_std_by_day['mean'] + mean_std_by_day['std']
    mean_std_by_day['std_low'] = mean_std_by_day['mean'] - mean_std_by_day['std']
    mean_std_by_day = mean_std_by_day.groupby('Days_Before').aggregate('mean').reset_index()

    #print info to console
    print(f"Number of Time Slices: {number_of_slices}")
    print(f"Number of Days: {int(number_of_slices / 24)}")
    print(mean_std_by_day)
    print(f"Drawing graph for: {var}")
    x = mean_std_by_day['Days_Before']
    y = mean_std_by_day['mean']
    std_high = mean_std_by_day['std_high']
    std_low = mean_std_by_day['std_low']

    graph = Linegraph(x,y,var,std_high,std_low)
    graph.draw_linegraph()

#function to see the change in forecasted variable for a particular day
def forecast_evoloution(forecast_slice, variable):
    #create dataframe with only unique forecast_date and variable, sort by pull time
    table = forecast[['forecast_date','pull_time',variable]]
    # print(table.head(30))
    # print(len(table))
    time_slice = table[table['forecast_date'] == forecast_slice].reset_index(drop=True).sort_values('pull_time')
    print(time_slice)
    grouped = table.groupby('forecast_date').aggregate('mean')
    print(grouped)



    x = time_slice['pull_time']
    y = time_slice[variable]
    graph, plot1 = plt.subplots()
    plt.plot(x, y)
    # plt.show()




forecast_evoloution('2022-12-17 23:00:00','hourly_temperature')

# grouped_by_day_column_stats('hourly_temperature')

# for column in forecast_all.columns[2:]:
#     grouped_by_day_column_stats(column)

