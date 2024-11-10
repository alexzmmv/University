#pragma once

#include <vector>
#include <algorithm>

#include "../Domain/Activity.h"

class Repository{
protected:
    std::vector<Activity*> activities;
public:
    Repository();
    Repository(std::vector<Activity> a);
    ~Repository()=default;

    virtual void addActivity(std::string title, std::string description, std::string link, DateTime dateTime, int peopleNumber, int duration);

    virtual void removeActivity(std::string title);

    virtual void updateActivity(std::string title, std::string description, std::string link, DateTime dateTime, int peopleNumber, int duration);
    std::vector<Activity> getActivities();
    Activity& getActivityByTitle(const std::string& title);
};

class RepositoryException : public std::exception {
private:
    std::string message;
public:
    explicit RepositoryException(std::string message);
    const char* what() const noexcept override;
};