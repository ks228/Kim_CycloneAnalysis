"""
COMP7230 - 2018 Assignment 1 code skeleton.

TODO: Replace this with your student id
Student ID: u1234567

In this assignment you will be writing some short pieces of code to process and
display data related to historical tropical cyclones in Australia.

The assignment will be marked out of 20 and is worth 20% of your final grade for COMP7230.

The assignment is structured as follows:

    Part 1 consists of Questions 1, 2 and 3 and deals with basic data cleaning,
    and preparation. It is worth a total of five (5) marks.

    Part 2 consists of Questions 4, 5 and 6 and deals with simple data visualisation
    including a histogram and the cyclone tracking. It is worth a total of seven (7)
    marks.

    Part 3 consists of Question 7 and deals with more complex data visualisation
    where you have to generate a heat-map. It is worth four (4) marks.
    Please be aware that this is a challenging question and make sure you have
    solved parts 1 and 2 before spending too much time on this question.

There will also be four (4) marks allocated to code quality, which includes such
aspects as:

    Appropriate commenting
    Variable naming
    Efficiency of computation
    Code structure and organisation

In addition to this file COMP7230_Assignment_1_Submission.py, we have also provided
a suite of unit tests COMP7230_Assignment_1_Submission_Tests.py which
will help you to test your work. These tests work in an identical fashion to the examples
we use in the Labs, so please familiarise yourself with those if you are not
sure how to make use of them. Please note that these tests are there to assist you,
but passing the tests is NOT a guarantee that your solution is correct.

Once you have completed questions 1-4, you should be able to run this file and
produce a histogram. Question 5 requires you to improve the histogram to make it
clearer and easier to understand.

Once you have completed questions 1, 2, 3 and 6, you should be able to run
COMP7230_Assignment_1_Animation.py and see the cyclone events animating on the map.

Once you have completed questions 1, 2, 3 and 7, you should be able to run
COMP7230_Assignment_1_Heatmap.py and produce the heat-map.

The assignment must be entirely your own work. Copying other students or sharing
solutions is a breach of the ANU Academic Honesty Policy and will be dealt with
accordingly. We reserve the right to ask any student to explain their code, and further
action may be taken if they are unable to do so.

The Assignment is due at 4pm, 7 September 2018. We will mark whatever is
uploaded into Wattle at that point, and late submissions will not be marked.

Once marks are released, you will have two weeks in which to question your mark.
After this period has elapsed, your mark will be considered final and no further
changes will be made.

If you ask for a re-mark, your assignment will be re-marked entirely, and your mark
may go UP or DOWN as a result.

The original data set was obtained from: http://www.bom.gov.au/cyclone/history/
The map was obtained from: https://www.google.com.au/maps
"""

import csv
from skimage import io 
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
from datetime import datetime
import time
import math
from collections import defaultdict
import sys

# Some constants you can make use of.

# The latitude and longitude extent of the provided map.
MAP_TOP = -6.2
MAP_BOTTOM = -36.82
MAP_LEFT = 106.8
MAP_RIGHT = 174.77

# Constant for Part 3.
EARTH_RADIUS = 6371  # Mean radius of the earth in kilometers.


########################################################################################################################
#                                   Part 1 - Data preparation and cleaning
#                                   Questions 1 - 3.        5 Marks total.
########################################################################################################################

#                                   Question 1.             1 Mark.
def is_valid_record(record):
    """
    This function tests whether a record has all the data that is required. Specifically, whether
    there is a non-empty value for central pressure and wind speed.
    :param record: A list containing a row of data in the file.
    format = [Name, ID, datetime, Type, Lat, Long, Central Pressure, Mean radius gf wind, Max wind speed, Comment]
    Each element in the list is a string.
    :return True if central pressure and wind speed have non-empty values, False otherwise.
    """
    centralPressure = record[6] # Get central Pressure element from the record
    maxWindSpeed = record[8] # Get maximum Wind Speed element from the record
    # Write a conditional to check if central pressure and wind speed are non-empty. Return True if non-empty, False otherwise.
    if centralPressure and maxWindSpeed:
        return True
    else:
        return False


#                                   Question 2.             2 Marks.
def parse_record(record):
    """
    This function converts a record in the data into a dictionary of key value pairs for each attribute/attribute value.
    :param record: A list containing a row of data in the file.
    format = [Name, ID, datetime, Type, Lat, Long, Central Pressure, Mean radius gf wind, Max wind speed, Comment]
    :return: A dictionary containing key value pairs for each attribute and value. It should contain the following
    attributes (of the corresponding types).
    "id" (string), "name" (string), "year" (int), "month" (int), "day" (int), "hour" (int), "central pressure" (float),
    "radius" (float), "speed" (float), "lat" (float), "long" (float)
    where "radius" is the Mean radius of gf wind, and "speed" is the Max wind speed.
    If a value is blank in the data, it should be left out of the dictionary.
    """
    # Initial the dictionary
    record_dictionary = dict()

    # Get the name from record and store it in dictioanry if found
    name = record[0]
    if name:
        record_dictionary["name"] = name
        
    # Get the ID from record and store it in dictioanry if found
    id = record[1]
    if id:
        record_dictionary["id"] = id
    
    """ Get the date and time from record and store it in dictioanry if found.
    Then convert datetime to year, month, day, and hour"""
    date_time = record[2]
    if date_time:
        datetime_object = datetime.strptime(date_time, '%m/%d/%Y %H:%M')
        record_dictionary["year"] = int(datetime_object.year)
        record_dictionary["month"] = int(datetime_object.month)
        record_dictionary["day"] = int(datetime_object.day)
        record_dictionary["hour"] = int(datetime_object.hour)
        
    # Get the type from record and store it in dictioanry if found
    type = record[3]
    if type:
        record_dictionary["type"] = type
        
    # Get the latitude from record and store it in dictioanry if found
    lat = record[4]
    if lat:
        record_dictionary["lat"] = float(lat)
    
    # Get the longitude from record and store it in dictioanry if found
    long = record[5]
    if long:
        record_dictionary["long"] = float(long)
        
    # Get the central pressure from record and store it in dictioanry if found
    central_pressure = record[6]
    if central_pressure:
        record_dictionary["central pressure"] = float(central_pressure)
        
    # Get the radius from record and store it in dictioanry if found
    radius = record[7]
    if radius:
        record_dictionary["radius"] = float(radius)
        
    # Get the speed from record and store it in dictioanry if found
    speed = record[8]
    if speed:
        record_dictionary["speed"] = float(speed)

    # Get the comment from record and store it in dictioanry if found
    comment = record[9]
    if comment:
        record_dictionary["comment"] = comment
        
    # return the dictionary to the caller
    return record_dictionary


#                                   Question 3.             2 Marks.
def convert_lat_long(lat, long):
    """
    This function converts latitude and longitude values into map coordinates.
    :param lat: a latitude value (float)
    :param long: a longitude value (float)
    :return: a tuple of x, y coordinates (x, y), where (0.0, 0.0) is the bottom left corner of the map
    and (1.0, 1.0) is the top right corner.
    You should make use of the constants described in the heading.
    """
    x, y = 0.0, 0.0

    # get the x coordinates
    x = EARTH_RADIUS * math.cos(lat) * math.cos(long)

    # get the y coordinates
    y = EARTH_RADIUS * math.cos(lat) * math.sin(long)

    #x = x / (762 - 1)
    x = x / (1546 - 1)
    #y = y / (1546 - 1)
    y = y / (762 - 1)
    
    return x, y

########################################################################################################################
#                                   Part 2 - Basic Data Visualisation
#                                   Questions 4 - 6.        7 Marks total.
########################################################################################################################

#                                   Question 4.             2 Marks
def pressure_distribution(records):
    """
    For this question you need to aggregate the data we will use to build the histogram of central pressure.
    :param records: A list of dictionaries, each element of the list is a dictionary containing the data for a single
    record, as produced by Question 2.
    :return: A dictionary, of {central pressure measurement : frequency count} pairs.
    """

	# create simple dictionary from collections package so that we can modify
    distribution_dictionary = defaultdict(float)
	
	# create a list and add the records. We create a list so that we can only work on central pressure
    mlist = list()
    for record in records:
        central_pressure = record["central pressure"]
        mlist.append(central_pressure)

    # iterate over the list and create frequencies of individual central pressure values
    for value in mlist:
        distribution_dictionary[value] += 1
    return distribution_dictionary


#                                   Question 5.             3 Marks
def pressure_histogram(distribution_dictionary):
    """
    Once you have completed Questions 1, 2 and 4, this function will create a histogram of the
    central pressure measurements.
    However, the histogram is not a particularly good one:
        It is hard to interpret.
        It is very cluttered.
        It is missing some important features - axis labels, a title, etc.
    Your task is to improve the histogram in whatever way you see fit.

    Marks will be awarded based on how well your new histogram conveys information,
    how easy it is to interpret, and whether it is formatted appropriately.

    You are free to modify the code below, or even delete it and replace it with your own if you wish.
    Please make sure you explain what you are doing (and why) in the comments.

    If you make use of external resources, please don't forget to reference them in the comments.

    :param distribution_dictionary: The dictionary of {central pressure : frequency count} key, value pairs, as
    produced by Question 4.
    :return: None
    """

    # Here to ensure there isn't an error if Q4 is not completed.
    if not distribution_dictionary:
        return None

    # Order the data based on the central pressure value.
    frequency_data = sorted(distribution_dictionary.items())

    # Generate the lists of x values and y values.
    x_list = [frequency_data[i][0] for i in range(len(frequency_data))]
    y_list = [frequency_data[i][1] for i in range(len(frequency_data))]

    # Get the mean and standard deviation of the central pressure data
    (mu, sigma) = norm.fit(x_list)
    # Display the histogram
    plt.bar(x_list, y_list, width=1)
    # Set the y-axis label of the plot
    plt.ylabel("Frequency")
    # Set the x-axis label of the plot
    plt.xlabel("Central Pressure")
    # Set the main title of the plot
    plt.title(r'$\mathrm{Histogram\ of\ Central\ Pressure:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
    # Form a grid on the plot
    plt.grid(True)
    # Create increments of 10 on the x-axis and increments of 100 on the y-axis
    plt.xticks(np.arange(min(x_list), max(x_list),10))
    plt.yticks(np.arange(min(y_list), max(y_list),100))
    # Graphically show the output of the histogram
    plt.show()

    return None


#                                   Question 6.             2 Marks
def animation_data(cyclone_records):
    """
    You need to prepare the track data for each cyclone, so they can be animated on the map.
    :param cyclone_records: A list of dictionaries, each element of the list is a dictionary containing the data
    for a single record, as produced by Question 2.
    :return: A list of (year, month, day, hour, latitude, longitude, wind_speed, name) tuples, in CHRONOLOGICAL order.
    The first four elements in each tuple should be integers, the next 3 should be floats, name should be a string.
    """
    cyclone_track = list()

    # get intermediate records with year, month, day, and hour converted to timestamps to sort in CHRONOLOGICAL order later.
    mrecords = []
    for record in cyclone_records:
        mdatetime = datetime(year=record["year"],
                                      month=record["month"],
                                      day=record["day"],
                                      hour=record["hour"])
        mtimestamp = time.mktime(mdatetime.timetuple())
        mtuple = (record, mdatetime)
        mrecords.append(mtuple)
    
    # now sort in CHRONOLOGICAL ORDER from the timestamps
    mrecords.sort(key=lambda x:x[1])
    
    # now get the record from the intermediate record list and get relevant data to be returned
    for mrecord in mrecords:
        record = mrecord[0]
        mtuple = (int(record["year"]),
                  int(record["month"]),
                  int(record["day"]),
                  int(record["hour"]),
                  float(record["lat"]),
                  float(record["long"]),
                  float(record["speed"]),
                  record["name"]
                  )
        cyclone_track.append(mtuple)
    
    return cyclone_track


########################################################################################################################
#                                   Part 3 - Advanced Data Visualisation
#                                   Question 7.             4 Marks total.
########################################################################################################################


#                                   Question 7.             4 Marks
def generate_heat_map(records):
    """
    Please be aware that this is a challenging question and it may take considerable
    effort to solve.
    Make sure you have completed the rest of the assignment to a high standard before
    spending a lot of time on this question.

    This question requires you to generate a heat-map of the data.

    A heat-map is essentially a two dimensional histogram of the data, where high frequencies are represented by
    bright colours (red, orange, etc), and low frequencies are represented by dark colours (green, blue, etc.)
    The data is stored as a two dimensional array of integers, where the integers represent the frequency counts
    for that part of the map. For example:

    [[10, 5],
    [[0, 12]]

    means that 10 cyclones were recorded in the top left quarter of the map, 5 in the top right quarter, etc.

    The default array size is 50 by 50, but you can increase this if you wish.

    For records that do not have a mean gf (gale-force) wind radius measurement, you should just include the grid cell
    that the eye is located in (as given by the latitude and longitude values).

    For records with a mean gf (gale-force) wind radius measurement, you should include any cell that is within
    the radius of the gale force winds (even if only part of the cell is inside the radius).
    The units for the mean gf wind radius attribute are kilometers.

    You should make use of the constants in the heading, as well as any functions you have previously written
    that are relevant.

    Once you have completed the code, you should also write a short comment (~200 words) that describes the
    heat-map, along with any reasons why the heat-map produced might not reflect actual cyclone activity.

    You will be marked on the correctness of your heat-map, as well as the efficiency of the code
    you use to generate the data. One (1) mark will also be allocated to your explanation. Please note that
    you must get the heat-map largely correct in order to receive the mark for the explanation.
    Partial marks may be awarded for partial solutions, as long as the code makes progress towards a
    full solution to the problem.

    :param records: A list of dictionaries, each element of the list is a dictionary containing the data for a single
    record, as produced by Question 2.
    :return: a 2d numpy array of integers.
    """
    array_size = 2500  # y, x dimensions of the heat-map
    heat_map_data = np.zeros(shape=(array_size, array_size))

    #### we will create our own bins based on the top,bottom,left, and right extents given
    # get total number of bins - 2500 in our case
    mdivider = 50*50

    # get bound of coordinates among which cyclone count should be recorded
    mapboundone = abs(MAP_BOTTOM) - abs(MAP_TOP)
    mapboundtwo = MAP_RIGHT - MAP_LEFT

    # get the increment so that we can go through the data 2500 records at a time
    diffboundone = mapboundone/array_size
    diffboundtwo = mapboundtwo/array_size

    # create a list of tuples to store lat-long bounds among which cyclone count will be binned
    mboundtuple = []

    # initialize the runners to bin lat-long values first (then count at later stage)
    latrunner = MAP_TOP
    longrunner = MAP_LEFT

    # run the runners and make list of lat,long bound tuples 
    for i in range(0, mdivider):
        latrunner = latrunner + diffboundone
        longrunner = longrunner + diffboundtwo
        x, y = convert_lat_long(latrunner,longrunner)
        mboundtuple.append((x, y))


    # create a list of tuples (lat,long) from the actual data now
    latlongtuples = [] 
    for record in records:
        mlat = record["lat"]
        mlong = record["long"]
        x,y = convert_lat_long(mlat,mlong)
        latlongtuples.append((x,y))
    

    # now we have the lat-long tuples with bounds and the actual lat-long tupples from the file - its time to count cyclones by comparing them
    # now we need an algorithm to do a single pass from the actual tupple data? but we have a problem of n-squared complexity?
    ## INCOMPLETE CODE ##
    for j in range(0, len(mboundtuple)-1):
        for k in range(len(latlongtuples)-1):
            if ((latlongtuples[k][0] >= mboundtuple[j][0] and latlongtuples[k][0] <= mboundtuple[j+1][0])
                    and (latlongtuples[k][1] >= mboundtuple[j][1] and latlongtuples[k][1] <= mboundtuple[j+1][1])):
                    heat_map_data[j][k] = heat_map_data[j][k] + 1
    return heat_map_data


########################################################################################################################
#                                   Do not modify the code below this point.
########################################################################################################################

def read_data_set(file_name):
    """
    Reads in and processes a csv file of the given name.
    :param file_name: The name of the file (string) to process.
    :return: A list of records.
    """

    # Read in the data set
    input_data = open(file_name, mode="r")
    input_reader = csv.reader(input_data)
    next(input_reader)  # Remove the header

    data_set = []

    for record in input_reader:
        if record[1] and record[2] and record[4] and record[5] and is_valid_record(record):
            data_set.append(record)

    input_data.close()

    return data_set


# Once you have finished questions 1, 2 and 4, running this file should produce a histogram.
# Your task for question 5 is to improve the quality and understandability of the histogram.
if __name__ == "__main__":

    data_set = read_data_set("Cyclones.csv")

    parsed_data = []

    for record in data_set:
        parsed_record = parse_record(record)
        if parsed_record:
            parsed_data.append(parsed_record)

    if parsed_data:
        histogram_data = pressure_distribution(parsed_data)
        pressure_histogram(histogram_data)
    else:
        print("You need to complete questions 1, 2 and 4 in order to produce the histogram")
