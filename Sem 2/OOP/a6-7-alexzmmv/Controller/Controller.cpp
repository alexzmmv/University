#include "Controller.h"

Controller::Controller(Repository* repository, UserPlanner* userPlanner) {
    this->repository = repository;
    this->userPlanner = userPlanner;
}

Controller::~Controller() {
    delete this->repository;
    delete this->userPlanner;
}


void Controller::addAdminActivity(std::string& title, std::string& description,  std::string& link, DateTime& dateTime, int duration, int peopleGoing) {
    this->repository->addActivity(title, description, link, dateTime, peopleGoing,duration );
}

void Controller::removeAdminActivity(std::string& title) {
    this->repository->removeActivity(title);
}

void Controller::updateAdminActivity(std::string& title, std::string& description,  std::string& link, DateTime& dateTime, int duration, int peopleGoing) {
    this->repository->updateActivity(title, description, link, dateTime, peopleGoing, duration);
}

std::vector<Activity> Controller::getAdminActivities() {
    return repository->getActivities();
}

void Controller::addActivityToUser(std::string title) {
    this->userPlanner->addActivity(this->repository->getActivityByTitle(title));
}

void Controller::removeActivityFromUser(std::string title) {
    this->userPlanner->removeActivity(this->repository->getActivityByTitle(title));
}

std::vector<Activity> Controller::getUserActivities() {
    return this->userPlanner->getActivities();
}

std::vector<Activity> Controller::getActivities() {
    return this->repository->getActivities();
}

std::vector<Activity> Controller::getMonthActivities(int month, int year) {
    std::vector<Activity> activities = this->repository->getActivities();
    std::vector<Activity> monthActivities;
    for (auto activity : activities) {
        if (activity.getDateTime().getMonth() == month && activity.getDateTime().getYear() == year)
            monthActivities.push_back(activity);
    }
    return monthActivities;
}

std::string Controller::saveUserActivities(std::string filePath) {
    //try cast to htmlUserPlanner
    try {
        dynamic_cast<htmlUserPlanner*>(this->userPlanner)->saveActivities(filePath+ ".html");
        return filePath + ".html";
    }
    catch (std::bad_cast& e) {
        //try cast to csvUserPlanner
        try {
            dynamic_cast<csvUserPlanner*>(this->userPlanner)->saveActivities(filePath+ ".csv");
            return filePath + ".csv";
        }
        catch (std::bad_cast& e) {
            throw std::runtime_error("Preety printing not available");
        }
    }
    return "";
}