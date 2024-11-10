#include "Repository.h"

RepositoryException::RepositoryException(std::string message) {
    this->message = message;
}

const char* RepositoryException::what() const noexcept {
    return this->message.c_str();
}


Repository::Repository() {
    this->activities = std::vector<Activity*>();
}

Repository::Repository(std::vector<Activity> a) {
    for (auto& activity : a) {
        this->activities.push_back(new Activity(activity));
    }
}

void Repository::addActivity(std::string title, std::string description, std::string link, DateTime dateTime, int peopleNumber, int duration) {
    auto activity = std::find_if(this->activities.begin(), this->activities.end(), [title](Activity* a) { return a->getTitle() == title; });
    if (activity != this->activities.end())
        throw RepositoryException("Activity already exists");
    this->activities.push_back(new Activity(title, description, link, dateTime, duration, peopleNumber));
}

void Repository::removeActivity(std::string title) {
    auto activity = std::find_if(this->activities.begin(), this->activities.end(), [title](Activity* a) { return a->getTitle() == title; });
    if (activity == this->activities.end())
        throw RepositoryException("Activity does not exist");
    this->activities.erase(activity);
}

void Repository::updateActivity(std::string title, std::string description, std::string link, DateTime dateTime, int peopleNumber, int duration) {
    auto activity = std::find_if(this->activities.begin(), this->activities.end(), [title](Activity* a) { return a->getTitle() == title; });
    if (activity == this->activities.end())
        throw RepositoryException("Activity does not exist");
    (*activity)->setTitle(title);
    (*activity)->setDescription(description);
    (*activity)->setLink(link);
    (*activity)->setDateTime(dateTime);
    (*activity)->setPeopleGoing(peopleNumber);
    (*activity)->setDuration(duration);
}

std::vector<Activity> Repository::getActivities() {
    std::vector<Activity> activitiesr;
    for (auto activity : this->activities) {
        activitiesr.push_back(*activity);
    }
    return activitiesr;
}

Activity& Repository::getActivityByTitle(const std::string& title) {
    auto activity = std::find_if(this->activities.begin(), this->activities.end(), [title](Activity* a) { return a->getTitle() == title; });
    if (activity == this->activities.end())
        throw RepositoryException("Activity does not exist");
    return **activity;
}