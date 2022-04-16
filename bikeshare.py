import time
import pandas as pd
import numpy as np
import pprint as pp

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

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
        city = str(input('Would you like to see data for \'Chicago\', \'New York City\', or \'Washington\': \n'))
        if city.lower().strip() in CITY_DATA:
            city = city.lower().strip()
            break

    FILTER = ['none', 'month', 'day']
    month, day = 'all', 'all'
    # get user input for filter (none, month, day)
    while True:
        print()
        filter = str(input('Would you like to filter the data by \'month\', \'day\' or not at all? Type \'none\' for no time filter \n'))
        if filter.lower().strip() in FILTER:
            filter = filter.lower().strip()
            break

    if filter != 'none':
        if filter == 'month':
            # get user input for month (january, february, ... , june)
            while True:
                print()
                month = str(input('Which month? (January, February, March, April, May, June): \n'))
                if month.lower().strip() in MONTHS:
                    month = month.lower().strip()
                    break

        if filter == 'day':
            # get user input for day of week (monday, tuesday, ... sunday)
            while True:
                print()
                day = str(input('Which day? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): \n'))
                if day.lower().strip() in DAYS:
                    day = day.lower().strip()
                    break

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
    # df['Start Time'] = pd.to_datetime(df['Start Time'])
    df.insert(2, 'Start Time Datetime', pd.to_datetime(df['Start Time']))

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time Datetime'].dt.month
    #df['day_of_week'] = df['Start Time Datetime'].dt.weekday_name
    df['day_of_week'] = df['Start Time Datetime'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        # months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = MONTHS.index(month) + 1

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
    if len(df['month'].unique()) > 1:
        print('Most common month: ', MONTHS[df['month'].mode()[0] - 1].title())

    # display the most common day of week
    if len(df['day_of_week'].unique()) > 1:
        print('Most common day of week: ', df['day_of_week'].mode()[0])

    # display the most common start hour
    df['hour'] = df['Start Time Datetime'].dt.hour
    df.pop('Start Time Datetime')
    print('Most common hour of day:', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most common end station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    # https://stackoverflow.com/questions/55719762/how-to-calculate-mode-over-two-columns-in-a-python-dataframe
    print('Most frequent combination of start station and end station:', ('\n' + df['Start Station'] + ' --> ' + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: ', float(df['Trip Duration'].sum()))

    # display mean travel time
    print('Average travel time: ', float(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of each user type:\n' + 'Subscribers: ' + str(df['User Type'].value_counts()[0])  + '\nCustomers: ' + str(df['User Type'].value_counts()[1]))

    if city.lower() == 'chicago' or city.lower() == 'new york city':
        # Display counts of gender
        print('Counts of each gender:\n' + 'Males: ' + str(df['Gender'].value_counts()[0])  + '\nFemales: ' + str(df['Gender'].value_counts()[1]))

        # Display earliest, most recent, and most common year of birth
        print('Earliest year of birth:', int(df['Birth Year'].min()))
        print('Most recent year of birth:', int(df['Birth Year'].max()))
        print('Most common year of birth: ', int(df['Birth Year'].mode()[0]))
    else:
        print('No gender data to share.')
        print('No birth year data to share')

    print("\nThis took %s seconds." % (time.time() - start_time))


def display_raw_data(df):
    """Displays raw data based on user filter selection 5 records at a time."""

    df_clean = df.drop(['month' ,'day_of_week', 'hour'], axis = 1)
    df_5_records = df_clean.head(5)
    for i in range(5):
        df_tmp = df_5_records.iloc[i]
        pp.pprint(df_tmp.to_dict(), sort_dicts=False)
        separator()


def separator():
    print('-'*40)


def main():
    while True:
        print()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        separator()
        print()
        print('Bike Share Data:')
        print('City: ', city.title())
        print('Month: ', month.title())
        print('Day: ', day.title())
        print()
        separator()
        time_stats(df)
        separator()
        station_stats(df)
        separator()
        trip_duration_stats(df)
        separator()
        user_stats(df, city)
        separator()

        # get user input for action (stats, raw data)
        while True:
            print()
            action = str(input('Would you like to view individual trip data? Type \'yes\' or \'no\'.\n'))
            if action.lower().strip() != 'yes':
                break
            else:
                display_raw_data(df)
                df.drop(index=df.index[:5], axis=0, inplace=True)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower().strip() != 'yes':
            break

if __name__ == "__main__":
	main()
