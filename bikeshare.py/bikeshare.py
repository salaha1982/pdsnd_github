### Bike-Sharing Data Analysis  
### Date : 21 Dec,2022

### Loading Libraries

import os
import time
import datetime
import pandas as pd
import numpy as np

# Multiple print statments in a single cell
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# Adjust the Display options for number of rows and columns 
pd.set_option("display.max_columns", 500)
pd.set_option("display.min_rows", 500)

# Check the current directory
os.getcwd()


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv' }


# In[8]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Initiliaze an empty city
    city = ''
    
    # Run a while loop to ensure that correct city name is chosen
    while city not in CITY_DATA.keys():
        print("=============================================")
        print("Please choose your city:")
        print("\n 1.Chicago 2. New York City 3. Washington")
        print("\n Valid Input: \n Complete name of city (It is not case sensitive) (Example: chicago or CHICAGO)")
        print("=============================================")
        
        #User will input the city name in wither lowercase or uppercase or a mix. 
        # We will convert everything into lowercase
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\n Error!! Please check your input. \n It should be either of 1.Chicago 2. New York City 3. Washington")
            
    # Print what city they have chosen
    print(f"\n Selected City: {city.title()}")
    
    # Make a dictionary of all the months. We will include the "all" option as well
    MONTH_DATA = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,'all': 13}
    
    # Initiliaze an empty month
    month = ''
    
    # Run a while loop to ensure that correct month name is chosen
    while month not in MONTH_DATA.keys():
        
        print("=============================================")
        print("\n Please enter the month for which you want to see the data.")
        print("\n Valid Input: Shorthand Month name. (It is not case sensitive)(e.g. jan or Jan).")
        print("\n If you want to see for all month then enter 'all'. ")
        print("=============================================")
        
        #User will input the month name in wither lowercase or uppercase or a mix. 
        # We will convert everything into lowercase
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\n Error!! Please check your input. \n It should be a valid month name.")

    print(f"\n Selected Month: {month.title()}")
    
    # Make a dictionary of all the months. We will include the "all" option as well
    DAY_LIST = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat','all']
    day = ''
    while day not in DAY_LIST:
        print("=============================================")
        print("\n Please enter the day of the week for which you want to see the data.")
        print("\n Valid Input: shorthand name of the day of the week. (It is not case sensitive) (e.g. sun or Sun).")
        print("\n If you want to see for all days then enter 'all'. ")
        print("=============================================")
        day = input().lower()

        if day not in DAY_LIST:
            print("\n Error!! Please check your input. \n It should be a valid day of the week name.")
            
    print(f"\n Selected Day of the week: {day.title()}")
    
    print(f"\n User selection: City: {city.upper()}, Month: {month.upper()} and Day: {day.upper()}.")
    

    print('-'*40)
    return city, month, day


# In[9]:


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
    # Load the given csv file for the selected city
    print("\n Load the data.")
    df = pd.read_csv(str(CITY_DATA[city]))
    
    # We need to convert the Time columns (Start Time and End Time) into proper datetime format columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # Get the hour from the Start Time column and then create an hour column
    df['start_hour'] = df['Start Time'].dt.hour
    
    # We need to extract the month and day of week from Start Time and save them as new columns
    # Month : Shorthand notation and converted into lowercase
    # Day of week : Shorthand notation and converted into lowercase
    df['month'] = df['Start Time'].dt.strftime('%b').str.lower()
    df['day_of_week'] = df['Start Time'].dt.strftime('%a').str.lower()

    # Month Filter : Filter the data based on month name
    if month != 'all':
        df = df[df['month'] == month]

    # Day of week Filter : Filter the data based on day of the week name
    if day != 'all':
        df = df[df['day_of_week'] == day]
        
    print("=====")
    print(df.head(2))
    print(df.shape)
    print("=====")

    return df


# In[10]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    # We can use the mode to get the most popular month
    popular_month = df['month'].mode()[0]

    # display the most common day of week

    # We can use the mode to get the most popular day of the week
    popular_day = df['day_of_week'].mode()[0]

    # display the most common start hour

    # We can use the mode to get the most popular start hour
    popular_hour = df['start_hour'].mode()[0]
    
    print(f'Popular Month: {popular_month}')
    print('\n')
    print(f'Popular Day : {popular_day}')
    print('\n')
    print(f'Popular Hour : {popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[11]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['Start_to_End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    common_start_to_end = df['Start_to_End'].mode()[0]

    print(f'Common Start Station : {common_start_station}')
    print('\n')
    print(f'Common End Station : {common_end_station}')
    print('\n')
    print(f'Common Start to End Station combination : {common_start_to_end}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[12]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()


    # display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    
    print(f'Total Duration : {total_duration}')
    print('\n')
    print(f'Average Duration : {average_duration}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(f"User type count:\n\n{user_type}")


    # Display counts of gender
    # Not all the given data frames have the gender column
    try:
        gender = df['Gender'].value_counts()
        print(f"Gender count:\n\n{gender}")
    except:
        print("\n There is no 'Gender' column.")

    # Display earliest, most recent, and most common year of birth
    # Not all the given data frames have the birth year column
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\n Earliest birth year: {earliest}")
        print(f"\n Most recent birth year: {recent}")
        print(f"\n Most common birth year: {common_year}")
    except:
        print("Birth year details is not present.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# If the user wishes to see a sample of data
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param (df): The data frame you wish to work with.
    Returns:
        None.
    """
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\n Would you like to view the raw data?")
        print("\n Valid responses: \n Yes(yes) \n No(no)")
        rdata = input().lower()
        
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\n Error! Invalid input.")
            print("Please check your response.")

    # If the user wihses to see the data many times
    while rdata == 'yes':
        print("Would you like to view the raw data again?")
        counter += 5
        rdata = input().lower()
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
    main()

    
