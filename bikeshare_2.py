import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


months = ['january', 'february', 'march', 'april', 'may', 'june']

days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for chicago, new york, or washington? \n')
        city = city.lower()
        if city in CITY_DATA:
            break
        else:
            print('That\'s not a valid city')


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Would you like to filter the data by month, ? Type "month name like march" or "all" \n')
        month = month.lower()
        if month in months or month == 'all':
            break
        else:
            print('That\'s not a valid month')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Would you like to filter the data by day, ? Type "day name like friday" or "all" \n')
        day = day.lower()
        if day in days or day == 'all':
            break
        else:
            print('That\'s not a valid day')


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('the most common month : {}'.format(popular_month))

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('the most common day of week : {}'.format(popular_day_of_week))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('the most common start hour : {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('the most common used start station : {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('the most common used end station : {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_frequent_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('the most common frequent combination of start station and end station trip : {}'.format(popular_frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('the total travel time : {} seconds'.format(total_travel_time))

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('the average time : {} seconds'.format(average_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of user types : \n{}'.format(user_types))

    # Display counts of gender
    if city != 'washington':
        counts_of_gender = df['Gender'].value_counts()
        print('The counts of gender : \n{}'.format(counts_of_gender))

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        earliest_year_of_birth = df['Birth Year'].max()
        most_recent_year_of_birth = df['Birth Year'].min()
        most_common_year_of_birth = df['Birth Year'].mode()[0]

        print('The earliest year of birth : {}'.format(earliest_year_of_birth))
        print('The most recent year of birth : {}'.format(most_recent_year_of_birth))
        print('The most common year of birth : {}'.format(most_common_year_of_birth))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_five_row_of_data(df):
    """we will show the first 5 data in the first attempt, then second 5 data for the second "yes"."""

    print('\nCalculating Loading data...\n')

    start_loc = 0

    while (True):
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        if(view_data == 'yes'):
            print(df.iloc[start_loc: start_loc+5])
            start_loc += 5
        else:
            break

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print('Loading data...')
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_five_row_of_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
