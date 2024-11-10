#pragma once

#include <stack>
#include "../Repo/Repository.h"
#include "../UserPlanner/UserPlanner.h"
#include "../UserPlanner/htmlUserPlanner.h"
#include "../UserPlanner/csvUserPlanner.h"
#include "CrudeCommands.h"
#include <memory>



class Controller {
private:
    Repository* repository;
    UserPlannerModel* userPlanner;
    std::vector<std::unique_ptr<command>> undoStack;
    std::vector<std::unique_ptr<command>> redoStack;
    int index;
public:
    Controller(Repository* repository, UserPlannerModel* userPlanner);
    ~Controller();
    void addAdminActivity(std::string& title, std::string& description,  std::string& link, DateTime& dateTime, int duration, int peopleGoing);
    void removeAdminActivity(std::string& title);
    void updateAdminActivity(std::string& title, std::string& description,  std::string& link, DateTime& dateTime, int duration, int peopleGoing);
    void undoAdmin();
    void redoAdmin();
    std::vector<std::pair<std::string, int>> statistics();
    std::vector<Activity> getAdminActivities();
    void addActivityToUser(std::string title);
    void removeActivityFromUser(std::string title);
    Activity getActivityByTitle(std::string title);
    std::vector<Activity> getUserActivities();
    std::vector<Activity>getActivities();
    std::vector<Activity> getMonthActivities(int month, int year);
    std::string saveUserActivities(std::string filePath);

};
