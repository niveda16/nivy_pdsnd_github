import time
import pandas as pd
import numpy as np

pd.options.display.width = 0

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters_for_dataframe():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data for Chicago, New York City, Washington!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city would you like to see first? Enter Chicago,New York City,Washington or 'e' to exit- ").lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            break
        elif city == 'e':
            exit()
        else:
            print("You entered an invalid city, please choose from the above 3 options. ")
            continue

    # fetching user input for month (all, january, february, ... , june)
    while True:
        try:
            month = int(input("Which month? Enter 1 for January, 2 for February...6 for June , 0 for 'All' or 7 to exit - "))
            if month in range(0, 7):
                break
            elif month == 7:
                exit()
            else:
                raise ValueError
        except ValueError:
            print("You entered an invalid month, please choose from the above options. ")

    # fetching user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = int(input("Which day? Enter 0 for Monday....6 for Sunday, 7 for 'All' or 8 to exit - "))
            if day in range(0, 8):
                break
            elif day == 8:
                exit()
            else:
                raise ValueError
        except ValueError:
            print("You entered an invalid day, please choose from the above options. ")

    print('-' * 40)
    return city, month, day


def load_data_in_dataframe(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city], index_col=[0])
    # converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracting month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filtering by month if applicable
    if month != 0:
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filtering by day of week if applicable
    if day != 7:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    return df


def time_statistics(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # displaying the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].mode()[0]
    print("The most popular month of commute is {}".format(popular_month))

    # displaying the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_day = df['day_of_week'].mode()[0]
    print("The most popular day of commute is {}".format(popular_day))

    # displaying the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular hour of commute is {}".format(popular_hour))

    # displaying 5 rows of data a time
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start = 0
    question = True
    if view_data != 'yes':
        question = False

    while question:
        print(df.iloc[start:start + 5])
        start += 5
        view_more = input("Do you wish to continue?yes or no : ").lower()
        if view_more != 'yes':
            question = False

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_statistics(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displaying most commonly used start station
    print("Most common origin is ", df['Start Station'].mode()[0])

    # displaying most commonly used end station
    print("Most common destination is ", df['End Station'].mode()[0])

    # displaying most frequent combination of start station and end station trip
    popular_trip = df[['Start Station', 'End Station']].value_counts().index.tolist()[0]
    print("Popular trip ", popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_statistics(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displaying total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total time is {} seconds ".format(total_travel_time))
    # displaying mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The average trip duration is {} seconds ".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_statistics(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displaying counts of user types
    print("Types of users...\n", df['User Type'].value_counts())

    if city == 'chicago' or city == 'new york city':
        # Displaying counts of gender for only Chicago and new york city
        print(df['Gender'].value_counts())

        # Displaying earliest, most recent, and most common year of birth
        print("Most common Birth year is ", df['Birth Year'].mode()[0])
        print("Most earliest Birth year is ", df['Birth Year'].min())
        print("Most recent Birth year is ", df['Birth Year'].max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters_for_dataframe()
        df = load_data_in_dataframe(city, month, day)
        time_statistics()(df)
        station_statistics()(df)
        trip_duration_statistics()(df)
        user_statistics()(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("See you again soon!")
            break


if __name__ == "__main__":
    main()
