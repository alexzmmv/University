#include "UserPlanner.h"
#include <stdexcept>


void UserPlanner::addActivity(Activity& activity)
{
    auto it = std::find(this->activities.begin(), this->activities.end(), &activity);
    if (it != this->activities.end())
        std::throw_with_nested(std::invalid_argument("Activity already exists"));
    activity.incPeopleGoing();
    this->activities.push_back(&activity);}

void UserPlanner::removeActivity(Activity& activity)
{
    auto it = std::find(this->activities.begin(), this->activities.end(), &activity);
    if (it == this->activities.end())
        std::throw_with_nested(std::invalid_argument("Activity does not exist"));
    activity.decPeopleGoing();
    this->activities.erase(it);}

std::vector<Activity> UserPlanner::getActivities()
{
    std::vector<Activity> activitiesr;
    for (auto activity : this->activities)
        activitiesr.push_back(*activity);
    return activitiesr;
}

UserPlanner::UserPlanner():activities(std::vector<Activity*> {}) {}
UserPlanner::~UserPlanner() {
    for (auto activity : this->activities)
        delete activity;
}

void UserPlanner::saveActivities(const std::string filePath) {
    throw std::runtime_error("Preety printing not available");
}