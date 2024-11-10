#include <map>
#include "Controller.h"

Controller::Controller(Repository* repository, UserPlannerModel* userPlanner) {
    this->repository = repository;
    this->userPlanner = userPlanner;
    this->undoStack = std::vector<std::unique_ptr<command>>();
    this->redoStack = std::vector<std::unique_ptr<command>>();
    this->index=0;
}

Activity Controller::getActivityByTitle(std::string title) {
    return this->repository->getActivityByTitle(title);
}

Controller::~Controller() {
    delete this->repository;
    delete this->userPlanner;
    undoStack.clear();
    redoStack.clear();
}


void Controller::addAdminActivity(std::string& title, std::string& description,  std::string& link, DateTime& dateTime, int duration, int peopleGoing) {
    auto act=Activity(title, description, link, dateTime, duration, peopleGoing);
    auto commandi=new addCommand(*this->repository, act);
    commandi->execute();
    //create unique pointer
    this->undoStack.push_back(std::unique_ptr<command>(commandi));
    redoStack.clear();
}

void Controller::removeAdminActivity(std::string& title) {
    auto act=this->repository->getActivityByTitle(title);
    auto *commandi=new removeCommand(*this->repository, act);
    commandi->execute();
    this->undoStack.push_back(std::unique_ptr<command>(commandi));
    redoStack.clear();
}

void Controller::updateAdminActivity(std::string& title, std::string& description,  std::string& link, DateTime& dateTime, int duration, int peopleGoing) {
    auto act=Activity(title, description, link, dateTime, duration, peopleGoing);
    auto *commandi=new updateCommand(*this->repository, act);
    commandi->execute();
    this->undoStack.push_back(std::unique_ptr<command>(commandi));
    redoStack.clear();
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

void Controller::undoAdmin() {
    if(undoStack.empty()) {
        throw RepositoryException("No more undos!");
        return;
    }
    auto action=std::move(undoStack.back());
    undoStack.pop_back();
    action->undo();
    redoStack.push_back(std::move(action));
    index++;
}

void Controller::redoAdmin() {
    if(redoStack.empty()) {
        throw RepositoryException("No more redos!");
        return;
    }
    auto action=std::move(redoStack.back());
    redoStack.pop_back();
    action->redo();
    undoStack.push_back(std::move(action));
    index--;
}