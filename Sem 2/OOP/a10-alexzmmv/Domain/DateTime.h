#pragma once

#include <iostream>

class DateTime {
private:
    int year;
    int month;
    int day;
    int hour;
    int minute;
public:
    DateTime();
    DateTime(int year, int month, int day, int hour, int minute);
    DateTime(const DateTime &dateTime);
    DateTime &operator=(const DateTime &dateTime);
    int getYear() const;
    int getMonth() const;
    int getDay() const;
    int getHour() const;
    int getMinute() const;

    void setYear(int year);
    void setMonth(int month);
    void setDay(int day);
    void setHour(int hour);
    void setMinute(int minute);

    std::string toString() const;

    bool operator<(const DateTime &dateTime) const;
    bool operator>(const DateTime &dateTime) const;
    bool operator==(const DateTime &dateTime) const;


    friend std::ostream &operator<<(std::ostream &out, const DateTime &dateTime);
    friend std::istream &operator>>(std::istream &in, DateTime &dateTime);
};