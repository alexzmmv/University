#include "Activity.h"
#include <iostream>

Activity::Activity()
        : title(""), description(""), link(""), peopleGoing(0), dateTime(DateTime()), duration(0) {
    // Initialize Activity members with default values
}

Activity::Activity(const std::string& title, const std::string& description, const std::string& link,
                   const DateTime& dateTime, int duration, int peopleGoing)
        : title(title), description(description), link(link), peopleGoing(peopleGoing),
          dateTime(dateTime), duration(duration) {}

Activity::Activity(const char* title, const char* description, const char* link,
                   const DateTime& dateTime, int duration, int peopleGoing)
        : title(std::string(title)), description(std::string(description)), link(std::string(link)),
          peopleGoing(peopleGoing), dateTime(dateTime), duration(duration) {}


std::string Activity::getTitle() {return this->title;}
std::string Activity::getDescription() {return this->description;}
std::string Activity::getLink() {return this->link;}
int Activity::getPeopleGoing() {return this->peopleGoing;}
DateTime Activity::getDateTime() {return this->dateTime;}

void Activity::setTitle(std::string title) {this->title = title;}
void Activity::setDescription(std::string description) {this->description = description;}
void Activity::setLink(std::string link) {this->link = link;}
void Activity::setPeopleGoing(int peopleGoing) {this->peopleGoing = peopleGoing;}
void Activity::setDateTime(DateTime dateTime) {this->dateTime = dateTime;}
void Activity::setDuration(int duration) {this->duration = duration;}
void Activity::incPeopleGoing() {this->peopleGoing++;}
void Activity::decPeopleGoing() {if (this->peopleGoing <= 0) return;this->peopleGoing--;}
bool Activity::operator==(const Activity& other) {return this->title == other.title;}

std::string Activity::toString() const{return this->title + "  " + this->description + "  " + this->link + "  " + std::to_string(this->peopleGoing) + "  " + this->dateTime.toString() + "  " + std::to_string(this->duration) ;}
std::string Activity::toPreetyString() const{return this->title + "  " + this->description + "  " + this->link + "  " + this->dateTime.toString() + "  duration:" + std::to_string(this->duration) + " minutes || "+"Participant:"+std::to_string(this->peopleGoing);}
int Activity::getDuration() {return this->duration;}
Activity::~Activity() {}

Activity& Activity::operator=(const Activity &other) {
    setTitle(other.title);
    setDescription(other.description);
    setLink(other.link);
    setPeopleGoing(other.peopleGoing);
    setDateTime(other.dateTime);
    setDuration(other.duration);
    return *this;
}

std::ostream &operator<<(std::ostream &out, const Activity &activity) {
    out << activity.title << " " << activity.description << " " << activity.link << " " << activity.peopleGoing << " " << activity.dateTime << " " << activity.duration;
    return out;
}

std::istream &operator>>(std::istream &in, Activity &activity) {
    std::string title, description, link;
    int peopleGoing, duration;
    DateTime dateTime;
    in >> title >> description >> link >> peopleGoing >> dateTime >> duration;
    activity.setTitle(title);
    activity.setDescription(description);
    activity.setLink(link);
    activity.setPeopleGoing(peopleGoing);
    activity.setDateTime(dateTime);
    activity.setDuration(duration);
    return in;
}