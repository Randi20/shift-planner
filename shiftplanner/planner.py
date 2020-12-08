import json
import random
import sys
import datetime
from datetime import date

def days_in_month(year, month):
    """
    Find a list of a ll days in a month
    :param year:
    :param month:
    :return:
    """
    return []

# Read the data from the json filee
def read_wishes(filepath, dates):
    data = { d : [] for d in dates}
    with open(filepath) as f:
        for line in f:
            line = json.loads(line)
            for thedate in line["Dates"]:
                parsed_date = date.fromisoformat(thedate)
                data[parsed_date].append(line["User"])

    return data

def assigning_shifts(prefereces, dates, users):
    """

    :return:
    """
    # selection : date -> user
    selection = {}

    def check_if_allowed(user, date):
        # TODO: check if user is used more than his or hers share
        yesterday = date - datetime.timedelta(days=1)
        if yesterday in selection:
            return selection[yesterday] != user
        else:
            return True

    def find_valid_users(people):
        return [user for user in people if check_if_allowed(user, date)]

    for date in dates:
        valid_users = find_valid_users(prefereces.get(date, []))
        if not valid_users:
            valid_users = find_valid_users(users)
        if not valid_users:
            return None
        selection[date] = random.choice(valid_users)

    return selection


def date_range(start, end):
    """
    :param start: the start date
    :param end: the end date (non-inclusive)
    :return: a list of dates between start and end
    """
    dates = []
    while start != end:
        dates.append(start)
        start = start + datetime.timedelta(days=1)
    return dates


def print_shifts(shifts, dates):
    """
    :param shifts: the dictionary of choices of shifts
    :param dates: the dates to print
    """
    for date in dates:
        print(date, shifts[date])


def find_shifts(preferences, dates):
    # print("Yes")
    # print(dates)
    #preferences = {StartDay: ["Randi"]}

    while True:
        # Try to assing shifts.
        shifts = assigning_shifts(preferences, dates, ["Randi", "Christian"])

        if shifts is not None:
            return shifts
        else:
            # If it does not, delte a preference and try again.
            key = random.choice(list(preferences))
            del preferences[key]



if __name__ == "__main__":
    today = date(2021, 2, 1)
    checkPeriod = 30  # Tne amount of the days that must be checked
    StartDay = today  # The start day
    endDay = StartDay + datetime.timedelta(days=checkPeriod)  # Calculate the end day for check
    dates = date_range(StartDay, endDay)
    data = read_wishes(sys.argv[1], dates)
    shifts = find_shifts(data, dates)
    print_shifts(shifts, dates)