import datetime

'''Utility providing conversions, validation and other useful functions for dates'''
class Date():

    '''Formats a datetime to a String'''
    def toString(date):
        return date.strftime("%Y-%m-%d %H:%M")

    '''Formats a String to a datetime'''
    def toDate(string):
        dateStr, timeStr = Date.getDateAndTime(string)
        dateSplit = dateStr.split("-")
        timeSplit = timeStr.split(":")
        y, m, d = int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2])
        H, M, S = int(timeSplit[0]), int(timeSplit[1]), int(timeSplit[2])
        return datetime.datetime(y, m, d, H, M, S)

    def formatDate(string):
        return Date.toString(Date.toDate(string))

    '''Returns "now" as a datetime'''
    def now():
        return datetime.datetime.now()

    '''Returns the date and time part of a String'''
    def getDateAndTime(dateTimeString):
        # Split date part and time part
        split = dateTimeString.split(" ")

        # Add time part if missing
        if len(split) < 2:
            split.append("00:00:00")

        # Split time part
        time = split[1].split(":")

        # Validate time part
        if(len(time)) > 3:
            raise DateFormatError("Incorrectly formatted time")

        # Pad time part as needed
        for i in range(3-len(time)):
             split[1] += ":00"

        # Validate time part 2
        time = split[1].split(":")
        if int(time[0]) > 59 or int(time[1]) > 59 or int(time[2]) > 99:
            raise DateFormatError("Incorrectly formatted time")

        # Splite date part
        date = split[0].split("-")

        # Validate date part
        if len(date) > 3 or len(date) < 2:
            raise DateFormatError("Incorrectly formatted date")

        # Pad date part as needed
        if len(date) == 2:
            split[0] = Date.now().strftime("%Y-") + split[0]

        # Validate date part 2
        date = split[0].split("-")
        if (not len(date[1]) == 2) or (not len(date[2]) == 2) or int(date[1]) > 12 or int(date[2]) > 31:
            raise DateFormatError("Incorrectly formatted date")

        return split[0], split[1]

    def before(date1, date2):
        return date1 <= date2

    def after(date1, date2):
        return date1 >= date2

    def overlap(start1, end1, start2, end2):
        return Date.between(start2, start1, end1) or Date.between(end2, start1, end1)

    def beteen(date, start, end):
        return start <= date <= end

    def lengthDays(date1, date2):
        return (date1 - date2).days

    def roundDaysToMonths(days):
        return days // 30 + 1 if days % 30 > 15 else days // 30

'''Error raise when given an improperly formatted String'''
class DateFormatError(Exception):
    pass
