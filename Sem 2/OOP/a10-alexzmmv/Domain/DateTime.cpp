#include "DateTime.h"
#include <cstdio>

DateTime::DateTime() {year = 0; month = 0; day = 0; hour = 0; minute = 0;}
DateTime::DateTime(int year, int month, int day, int hour, int minute) {
    if(month>12 or day>31 or hour>24 or minute>60)
        throw std::runtime_error("Enter a valid datetime");
    this->year = year;
    this->month = month;
    this->day = day;
    this->hour = hour;
    this->minute = minute;
}
DateTime::DateTime(const DateTime& dateTime) {
    this->year = dateTime.year;
    this->month = dateTime.month;
    this->day = dateTime.day;
    this->hour = dateTime.hour;
    this->minute = dateTime.minute;
}

DateTime& DateTime::operator=(const DateTime& dateTime) {
    if (this == &dateTime)
        return *this;
    year = dateTime.year;
    month = dateTime.month;
    day = dateTime.day;
    hour = dateTime.hour;
    minute = dateTime.minute;
    return *this;
}

std::string DateTime::toString() const {
    std::string buffer;
    buffer= std::to_string(year) + "-" + std::to_string(month) + "-" + std::to_string(day) + " " + std::to_string(hour) + ":" + std::to_string(minute);
    return std::string(buffer);
}

int DateTime::getYear() const {return year;}
int DateTime::getMonth() const {return month;}
int DateTime::getDay() const {return day;}
int DateTime::getHour() const {return hour;}
int DateTime::getMinute() const {return minute;}

void DateTime::setYear(int year) {this->year = year;}
void DateTime::setMonth(int month) {this->month = month;}
void DateTime::setDay(int day) {this->day = day;}
void DateTime::setHour(int hour) {this->hour = hour;}
void DateTime::setMinute(int minute) {this->minute = minute;}

std::ostream& operator<<(std::ostream& out, const DateTime& dateTime) {
    out << dateTime.year << " " << dateTime.month << " " << dateTime.day << " " << dateTime.hour << " " << dateTime.minute;
    return out;
}

std::istream &operator>>(std::istream &in, DateTime &dateTime) {
    int year, month, day, hour, minute;
    in >> year >> month >> day >> hour >> minute;
    dateTime.setYear(year);
    dateTime.setMonth(month);
    dateTime.setDay(day);
    dateTime.setHour(hour);
    dateTime.setMinute(minute);
    return in;
}

bool DateTime::operator<(const DateTime& dateTime) const {
    if (year < dateTime.year)return true;
    if (year > dateTime.year)return false;
    if (month < dateTime.month)return true;
    if (month > dateTime.month)return false;
    if (day < dateTime.day)return true;
    if (day > dateTime.day)return false;
    if (hour < dateTime.hour)return true;
    if (hour > dateTime.hour)return false;
    return minute < dateTime.minute;
}

bool DateTime::operator>(const DateTime& dateTime) const {
    return dateTime < *this;
}

bool DateTime::operator==(const DateTime& dateTime) const {
    return year == dateTime.year && month == dateTime.month && day == dateTime.day && hour == dateTime.hour && minute == dateTime.minute;
}