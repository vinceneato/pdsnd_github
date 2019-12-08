"""
Interactive bikeshare data program by Vincent M Nieto created on November 17th, 2019
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hi. Let\'s explore some US bikeshare data.')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please choose a city: Chicago, New York City, or Washington: ").lower()
    # Adding while loop to account for a case when user input doesn't match the available cities.
    while city not in ["chicago", "new york city", "washington"]:
        city = input("\nInput invalid.  Please try again: ").lower()

    # Get user input for month (all, january, february, ... , june)
    month = input("Choose a month from January to June (e.g. \"January\") or choose \"all\": ").lower()
    # Adding while loop to account for a case when user input doesn't match the available months.
    while month not in ["all", "january", "february", "march", "april", "may", "june"]:
        month = input("\nInput invalid.  Please try again: ").lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please choose a day (e.g. \"Sunday\") or choose \"all\"): ").lower()
    # Adding while loop to account for a case when user input doesn't match the available cities.
    while day not in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        day = input("\nInput invalid. Please try again: ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

	# Where the csv file is loaded.
    file_name = city.replace(' ', '_') + '.csv'
    df = pd.read_csv(file_name)

    # Converting start and end time to "datetime"
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #Extracting month and day of week from "Start Time"
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] = pd.DatetimeIndex(df['Start Time']).dayofweek

    # Creating a list so that the index of each element can be matched to the user-input (month).
    if month != 'all':
        months = ["january", "february", "march", "april", "may", "june"]
        month_int = months.index(month) + 1
        df = df[df['month'] == month_int]

    # Creating a list so that the index of each element can be meatched to the user-input (day).
    if day != 'all':
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        days_int = days.index(day)
        df = df[df['day_of_week'] == days_int]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ["january", "february", "march", "april", "may", "june"]
    print("The most common month is ", months[df['month'].mode().values[0] - 1])

    # Display the most common day of week
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    print("The most common day of the week is ", days[df['day_of_week'].mode().values[0]])

    # Display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print("The most common start hour is ", df['start_hour'].mode().values[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('The most common start station is', df['Start Station'].mode().values[0])

    # Display most commonly used end station
    print('The most common end station is ', df['End Station'].mode().values[0])

    # Display most frequent combination of start station and end station trip
    df['start_end'] = df['Start Station'] + " " + df['End Station']
    print("The most frequent combination of start station and end station is", df["start_end"].mode().values[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print("The total trip duration is {0} seconds".format(str(df['Trip Duration'].sum())))

    # Display mean travel time
    print("The mean trip duration is {0} seconds".format(str(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The counts of user types are as follows:")
    print(df.groupby('User Type').count()['Start Time'])


    # Display counts of gender
    try:
        test = df['Gender'][0]
        print("The counts of genders are as follows:")
        print(df.groupby('Gender').count()['Start Time'])
    except:
        pass

    # Display earliest, most recent, and most common year of birth
    try:
        print("The earliest birth year is {0}".format(str(int(df['Birth Year'].min()))))
        print("The most recent birth year is {0}".format(str(int(df['Birth Year'].max()))))
        print("The most common birth year is {0}".format(str(int(df['Birth Year'].mode().values[0]))))
    except:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    Display contents of the CSV file 5 rows at a time.
    """

    start_loc = 0
    end_loc = 5

    display_active = input("Do you want to see the raw data? (\"Yes\" or \"No\"): ").lower()
# Begins displaying the raw data 5 rows at a time.
    if display_active == 'yes':
        while end_loc <= df.shape[0] - 1:
            print(df.iloc[start_loc:end_loc, :])
            start_loc += 5
            end_loc += 5
# Limits the answer to "yes" or "no," and handles typos.
            end_display = input("Do you wish to continue? (\"yes\" or \"no\"): ").lower()
            while end_display.lower() not in ('yes', 'no'):
                print("Please type \"yes\" or \"no\"" )
                end_display = input("Do you wish to continue? (\"yes\" or \"no\"): ").lower()
            if end_display == 'no':
                break


def main():
    """
    Main function for running the whole script.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
