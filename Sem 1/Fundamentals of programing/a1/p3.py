# 12

class Calendaristic_date:
    def __init__(self, date: str):
        date = date.split()
        y, m, d = date
        self.year = int(y)
        self.month = int(m)
        self.day = int(d)


def is_leap_year (year: int) -> bool:
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False


def distance_in_days_between_2_calendaristic_dates( Date1, Date2) -> int:

    total_days_between_dates = 0

######################

    for year in range(Date1.year, Date2.year):
        if is_leap_year(year) == True:
            total_days_between_dates += 366
        else:
            total_days_between_dates += 365

######################

    days_in_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for month in range(1, Date1.month):
        total_days_between_dates -= days_in_months[month]
    total_days_between_dates -= Date1.day

    for month in range(1, Date2.month):
        total_days_between_dates += days_in_months[month]
    total_days_between_dates += Date2.day

######################

    return total_days_between_dates


print("This is a days between dates calculator, format of dates is yyyy mm dd,first date is smaller than the second date:\n")

Date1 = Calendaristic_date(input("Please enter the first date here: "))
Date2 = Calendaristic_date(input("Please enter the second date here: "))

print("Distance between first and second date is: ",distance_in_days_between_2_calendaristic_dates(Date1,Date2),"days ")