#include "csvUserPlanner.h"
#include <fstream>
#include <stdexcept>
csvUserPlanner::csvUserPlanner() {
}

csvUserPlanner::~csvUserPlanner() {
}

void csvUserPlanner::addActivity(Activity &activity) {
    UserPlannerModel::addActivity(activity);
}

void csvUserPlanner::removeActivity(Activity &activity) {
    UserPlannerModel::removeActivity(activity);
}

void csvUserPlanner::saveActivities(const std::string filePath) {
    std::ofstream file(filePath.c_str());
    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + filePath);
    }
    for (auto activity : this->activities) {
        file<<activity->getTitle()<<','<<activity->getDescription()<<','<<activity->getLink()<<','<<activity->getDateTime().getYear()<<'-';
        file<<activity->getDateTime().getMonth()<<'-'<<activity->getDateTime().getDay()<<' '<<activity->getDateTime().getHour()<<':'<<activity->getDateTime().getMinute()<<':'<<activity->getPeopleGoing()<<" people,"<<activity->getDuration()<<"s\n";
    }
    file.close();
}