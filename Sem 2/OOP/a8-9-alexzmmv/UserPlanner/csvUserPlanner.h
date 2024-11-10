#pragma once
#include "UserPlanner.h"

class csvUserPlanner: public UserPlanner{
public:
    csvUserPlanner();
    ~csvUserPlanner();
    void addActivity(Activity& activity) override;
    void removeActivity(Activity& activity) override;
    void saveActivities(const std::string filePath)override;
};