import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
dayofweek={'monday':0, 'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5,'sunday':6}
month_2_number={'january':1,'february':2,'march':3,'april':4,'may':5,'june':6}
num_2_week=dict([(i[1], i[0]) for i in dayofweek.items()])
num_2_month=dict([(i[1], i[0]) for i in month_2_number.items()])

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
    city=input('\nWhich city? chicago, new york city, washington\n').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        print("\n plase Enter chicago, new york city or washington" )
        # get user reenter the message for correct inputs
        city=input('\nWhich city? chicago, new york city, washington\n').lower()

    # get user input for month (all, january, february, ... , june)
    month=input('\nWhich month? \nall, january, february, march, april, may, june\n').lower()
    while month not in list(month_2_number.keys())+['all']:
        print("\n plase only Enter the correct month" )
        # get user reenter the message for correct inputs
        month=input('\nWhich month? \nall, january, february, march, april, may, june\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=input('\nWhich day of the week? \nall, monday, tuesday, ... sunday\n').lower()
    while day not in list(dayofweek.keys())+['all']:
        print("\n plase only Enter the correct day of the week, such as monday, tuesday, etc.")
        # get user reenter the message for correct inputs
        day=input('\nWhich day of the week? \nall, monday, tuesday, ... sunday\n').lower()

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

    df=pd.read_csv(CITY_DATA[city],infer_datetime_format = True)

    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])


    df['month']=pd.DatetimeIndex(df['Start Time']).month
    df['day of week']=df['Start Time'].dt.dayofweek

    if month!='all':
        df=df[df['month']==month_2_number[month.lower()]]
    if day !='all':
        df=df[df['day of week']==dayofweek[day.lower()]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('the most common month is %s \n' %num_2_month[df['month'].value_counts().index[0]])

    # display the most common day of week
    print('the most common day of week is %s \n' %num_2_week[df['day of week'].value_counts().index[0]])

    # display the most common start hour
    print('the most common start hour is %s \n' %df['Start Time'].dt.hour.value_counts().index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('the most commonly used start station is %s \n' %df['Start Station'].value_counts().index[0])

    # display most commonly used end station
    print('the most commonly used end station is %s \n' %df['End Station'].value_counts().index[0])

    # display most frequent combination of start station and end station trip
    print('the most frequent combination of start station and end station trip is %s \n' %str(df.groupby(["Start Station", "End Station"]).size().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('total travel time is %s mins \n' % (df['Trip Duration'].sum()/60.0))

    # display mean travel time
    print('mean travel time is %s mins \n' % (df['Trip Duration'].mean()/60.0))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('counts of user types \n')
    print(df['User Type'].value_counts())
    print('\n')

    # Display counts of gender
    print('counts of gender \n')
    try:
        print(df['Gender'].value_counts())
    except:
        print('gender is not available')
    print('\n')

    # Display earliest, most recent, and most common year of birth
    try:
        print('earliest year is %s \n' %int(df['Birth Year'].min()))
        print('most recent year is %s \n' %int(df['Birth Year'].max()))
        print('most common year is %s \n' %int(df['Birth Year'].value_counts().index[0]))
    except:
        print('year of birth is not available \n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        CONTINUE='yes'
        while CONTINUE=='yes':
            for i in range(0, df.shape[0],5):
                print(df.iloc[i:i+5,:])
                CONTINUE = input('\nWould you like to view individual trip data? Enter yes or no.\n').lower()
                if CONTINUE=='no':
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
