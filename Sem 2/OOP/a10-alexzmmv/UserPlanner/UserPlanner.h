#pragma once
#include <vector>
#include <algorithm>
#include "Activity.h"

class UserPlannerModel {
protected:
    std::vector<Activity*> activities;

public:
    virtual void addActivity(Activity& activity);
    virtual void removeActivity(Activity& activity);
    std::vector<Activity> getActivities();
    virtual void saveActivities(const std::string filePath);
    UserPlannerModel();
    ~UserPlannerModel();
};
