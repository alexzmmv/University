#include <map>
#include "Controller.h"

Controller::Controller(Repository* repository, UserPlanner* userPlanner) {
    this->repository = repository;
    this->userPlanner = userPlanner;
}

Activity Controller::getActivityByTitle(std::string title) {
    return this->repository->getActivityByTitle(title);
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
    //try cast to htmlUserPlanner first
    try {
        auto* htmlUserPlanner = dynamic_cast<class htmlUserPlanner*>(this->userPlanner);
        if (htmlUserPlanner != nullptr) {
            htmlUserPlanner->saveActivities(filePath);
            return filePath;
        }
        try {
            auto* csvUserPlanner = dynamic_cast<class csvUserPlanner*>(this->userPlanner);
            if (csvUserPlanner != nullptr) {
                csvUserPlanner->saveActivities(filePath);
                return filePath;
            }
        }
        catch (std::exception& e) {
            std::cerr << "Preety printing not available\n";
        }
    }
    catch (std::exception& e) {
        std::cerr << "Preety printing not available\n";
    }
    return "";
}

std::vector<std::pair<std::string, int>> Controller::statistics() {
std::map<int, int> stats;//year, number of activities
    std::vector<Activity> activities = this->repository->getActivities();
    std::vector<int> years;
    for (auto activity : activities) {
        //number of activities per year
        auto year = activity.getDateTime().getYear();
        if (std::find(years.begin(), years.end(), year) == years.end()) {
            years.push_back(year);
            stats[year] = 1;
        }
        else {
            stats[year]++;
        }
    }
    std::vector<std::pair<std::string, int>> result;
    for (auto stat : stats) {
        result.emplace_back(std::to_string(stat.first), stat.second);
    }
    return result;
}
