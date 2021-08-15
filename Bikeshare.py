import time
import pandas as pd
import numpy as np
from InquirerPy import prompt
import sys
import calendar
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['Janauary', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'	]
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]
# python script will be read until this part

def get_filters():
    city = ""
    while city not in CITY_DATA:
        if city == 'exit':
            sys.exit()
        if city == "":
            message = "\nWhich city would you like to explore? (Available cities: Chicago, Washington, New York City).\nN.B. You can enter 'exit' to interrupt program\n"
        else:
            if city.isalpha() == False:
                message = "You can only enter alphabet letters; please try again.\nN.B. You can enter 'exit' to interrupt program\n"
            else:
                message = "\nI can't recognise this entry, please choose one of the available cities: Chicago, Washington, New York City.\nN.B. You can enter 'exit' to interrupt program\n"
        
        questions = [
            {"type": "input", "message": message, "name": "city"},
        ]
        answers = prompt(questions)
        city = answers['city'].lower()
        
    df = pd.read_csv(CITY_DATA[city]) # df have all csv data with format, thus columns and rows
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['user_type'] = df['User Type']
    df['avg_trip'] = df['Trip Duration']
    exist_months = sorted(df['month'].unique().tolist()) #get unique months from chicago.csv file
    exist_months = [ MONTHS[i-1] for i in exist_months]
    exist_months.append('All')
    
    q = [
        {
            "type": "list",
            "message": "Filter by month, day, or nofilter?",
            "choices": ["Month", "Day", "nofilter"],
            "name": "option"
        },
    ]
    answers = prompt(q)
    filter_option = answers['option']
    if filter_option == "Month":
        q = [
            {
                "type": "list",
                "message": "Which Month?",
                "choices": exist_months,
                "name": "month"
            },
        ]
        answers = prompt(q)
        sel_val = answers['month']
        if sel_val.lower() != 'all':
            month =  MONTHS.index(sel_val) + 1
            df = df[ df['month'] == month ] # Filter dataframe will by month, f.e if you select Jan, then df have only Jan data
    elif filter_option == "Day":
        q = [
            {
                "type": "list",
                "message": "Which Day?",
                "choices": DAYS,
                "name": "day"
            },
        ]
        answers = prompt(q)
        sel_val = answers['day']
        if sel_val.lower() != 'all':
            # filter by day of week to create the new dataframe
            df = df[ df['day_of_week'] == sel_val.title()]
    else:
        sel_val = ""
    return df, filter_option, sel_val

def show_raw_data(df):
    q = [
        {
            "type": "confirm",
            "message": "Do you want to see raw data?",
        },
    ]
    result = prompt(q)
    can_view = result[0]
    i = 0
    df = df.sort_values('Trip Duration', ascending=False)
    while can_view and len(df.index) > i * 5:
        print(df[i*5 : 5*(i+1)])
        q = [
            {
                "type": "confirm",
                "message": "Would you like to see 5 more rows of the data?",
            },
        ]
        result = prompt(q)
        can_view = result[0]
        i += 1

def time_stats(df, mode, sel_val):
    # display the month with most frequent travel
    most_common_month = calendar.month_name[df['month'].value_counts().idxmax()]
    print("Month with most frequent travel {}:".format(sel_val), most_common_month)

    # display the day with most frequent travel
    most_common_day = df['day_of_week'].value_counts().idxmax()
    print("Day with most frequent travel {}:".format(sel_val), most_common_day)

    # display the hour with most frequent travel
    most_common_hour = df['hour'].value_counts().idxmax()
    print("Hour with most frequent travel {}:".format(sel_val), most_common_hour)

def station_stats(df, mode, sel_val):
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station {}:".format(sel_val), most_common_start_station)
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station {}:".format(sel_val), most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station {} : {}, {}"\
            .format(sel_val, most_common_start_end_station[0], most_common_start_end_station[1]))

def trip_duration_stats(df, mean, sel_val):
    average_trip_duration = df['Trip Duration'].mean()
    print("The average trip duration {}:".format(sel_val), average_trip_duration)

def user_stats(df, mode, sel_val):
    most_common_user_type = df['User Type'].value_counts().idxmax() 
    print("The most common user type {}:".format(sel_val), most_common_user_type)

def main(): # Call defined functions.
    df, mode, sel_val = get_filters()
    show_raw_data(df)
    time_stats(df, mode, sel_val)
    station_stats(df, mode, sel_val)
    trip_duration_stats(df, mode, sel_val)
    user_stats(df, mode, sel_val) 

if __name__ == "__main__":
	main()
