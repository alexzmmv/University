#pragma once
#include <string>
#include "DateTime.h"

#define NULL_LINK "https://www.youtube.com/watch?v=dQw4w9WgXcQ/"

class Activity {
private:
    std::string title;
    std::string description;
    std::string link;
    int peopleGoing;
    DateTime dateTime;
    int duration;
public:
    Activity();
    Activity(const std::string& title, const std::string& description, const std::string& link,const DateTime& dateTime, int duration, int peopleGoing);
    Activity(const char* title, const char* description, const char* link,const DateTime& dateTime, int duration, int peopleGoing);
    ~Activity();
    std::string getTitle();
    std::string getDescription();
    std::string getLink();
    int getPeopleGoing();
    DateTime getDateTime();
    int getDuration();


    void setTitle(std::string title);
    void setDescription(std::string description);
    void setLink(std::string link);
    void setPeopleGoing(int peopleGoing);
    void setDateTime(DateTime dateTime);
    void setDuration(int duration);

    void incPeopleGoing();
    void decPeopleGoing();

    bool operator==(const Activity& other);
    Activity& operator=(const Activity& other);

    std::string toString() const;
    std::string toPreetyString() const;
    friend std::ostream &operator<<(std::ostream &out, const Activity& activity);
    friend std::istream &operator>>(std::istream &in, Activity& activity);
};
