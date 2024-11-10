#pragma once
#include "../Repo/Repository.h"
#include "../UserPlanner/UserPlanner.h"
#include "../UserPlanner/htmlUserPlanner.h"
#include "../UserPlanner/csvUserPlanner.h"





class Controller {
private:
    Repository* repository;
    UserPlanner* userPlanner;
public:
    Controller(Repository* repository, UserPlanner* userPlanner);
    ~Controller();
    void addAdminActivity(std::string& title, std::string& description,  std::string& link, DateTime& dateTime, int duration, int peopleGoing);
    void removeAdminActivity(std::string& title);
    void updateAdminActivity(std::string& title, std::string& description,  std::string& link, DateTime& dateTime, int duration, int peopleGoing);
    std::vector<Activity> getAdminActivities();
    void addActivityToUser(std::string title);
    void removeActivityFromUser(std::string title);
    std::vector<Activity> getUserActivities();
    std::vector<Activity>getActivities();
    std::vector<Activity> getMonthActivities(int month, int year);
    std::string saveUserActivities(std::string filePath);
};
