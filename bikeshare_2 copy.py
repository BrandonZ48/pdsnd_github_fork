import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months_list = ["all","january","february",
"march","april","may","june"]

weekdays_list = ["all","monday","tuesday","wednesday",
"thursday","friday","saturday","sunday"]

cities_list = list(CITY_DATA.keys())

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
    city = get_input(cities_list,"choose a city to get data from:")

    # get user input for month (all, january, february, ... , june)
    month = get_input(months_list,"now choose a month(Jan to June, 'all' for no filter):")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_input(weekdays_list,"now choose a day of the week('all' for no filter): ")

    print('-'*40)
    return city, month, day

def get_input(list_of_valid,prompt = "give input: "):
    """
    prompts user for input until an acceptable input is given based on the list provided,
    must be a string

    Args:
        (list) list_of_valid - list of str values that the user can input that is considered valid
        (str)  printed message to communicate with the user
    Returns:
        user_input - string given by the user from list_of_valid
    """
    #lowercase everything to remove case sensitivity
    list_of_valid = [elem.lower() for elem in list_of_valid]

    #prompt the user for input
    print(prompt,list_of_valid)

    #loop until the user inputs a valid string
    while(True):
        user_input = input()
        if type(user_input) != str:
            print("\ninvalid input, please choose from the following: ",list_of_valid,"\n")
            continue
        if (not (user_input.lower() in list_of_valid)):
            print("\ninvalid input, please choose from the following: ",list_of_valid,"\n")
        else:
            print("\naccepted input: ",user_input,"\n")
            break
    return user_input.lower()

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.day_name()

    #extract hour (0 to 23) for later use
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month.lower() != 'all':

        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':

        # filter by day of week to create the new dataframe
        df = df.loc[df['day of week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""


    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("most popular month for travel: ",df['month'].mode()[0])


    # display the most common day of week
    print("most popular day of the week for travel: ",df['day of week'].mode()[0])


    # display the most common start hour
    print("most popular starting hour: ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("most popular starting station: ",df['Start Station'].mode()[0])

    # display most commonly used end station
    print("most popular ending station: ",df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip(lambda for formatting)
    print("most popular trip: ",(df['Start Station'].apply(lambda elem: elem + " - ")
     + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = pd.to_datetime(df['Trip Duration'].sum(),unit='s')
    print("Total travel time: ",(total_time.day*24)+total_time.hour,
    "hours",total_time.minute,"minutes",total_time.second,"seconds")

    # display mean travel time
    average_time = pd.to_datetime(df['Trip Duration'].mean(),unit='s')
    print("Average travel time: ",average_time.hour,
    "hours",average_time.minute,"minutes",average_time.second,"seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("showing user types: \n",df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print("showing genders: \n",df['Gender'].value_counts())
    else:
        print("no available data on gender")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("earliest year of birth: ",df['Birth Year'].min())
        print("most recent year of birth: ",df['Birth Year'].max())
        print("most common year of birth: ",df['Birth Year'].mode()[0])
    else:
        print("no available data on birth years")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    #ask user if they want raw data
    print("would you like to see some raw data? 'yes' for data, any input for no")

    #display requested data, 5 lines at a time if possible
    row_index = 0
    while(True):
        if(input().lower() != 'yes'):
            break
        else:
            print(df.iloc[row_index:row_index + 5])
            row_index += 5
            if row_index >= df.shape[0]:
                print("end of data reached!")
                break
            else:
                print("do you want to see more?")

    #loop if the user wants to try new input
    restart = input('\nWould you like to restart? Enter yes to restart or any other input for no.\n')
    if restart.lower() != 'yes':
        break


def main():
    while True:
        #create data based on input
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #display stats
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #offer to show user raw data
        display_raw_data(df)


if __name__ == "__main__":
	main()
