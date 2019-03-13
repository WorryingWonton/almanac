from datetime import datetime
import sys

"""
This program will take several command line arguments:
    -Start Date
    -End Date
    -Calculation Interval
    -Body to be observed.

It will output observed GHA values onto the command line, where the number of outputs is determined as the product
of the time window and the calculation interval.

The first testable milestone is to get a program which can read date_time strings from the command line, and convert them into 
DateTime objects.  If the program receives a string which can be parsed as a DateTime object, it will return a DateTime object.
Otherwise, it will return None.  [Done]

The second milestone is output of GHA at an arbitrarily specifiable time and date. [High difficulty, the milestones after this are a lot simpler]

The third milestone is the output of declination at an arbitrarily specifiable time and date.

The fourth is the output of the little-v correction

The fifth is the output the little-m correction

the sixth is the output of the little-d correction.

The seventh is the output of the SD correction (for moon tabulations)

The eighth, and non testable output, will be calling the GHA generator function an arbitrary number of times.
"""

def convert_to_date_time(date_string):
    try:
        date = datetime.strptime(date_string, '%m/%d/%Y %H')
        return date
    except ValueError:
        return None

if __name__ == '__main__':
    if sys.argv[1]:
        print(convert_to_date_time(sys.argv[1]))
