#pragma once
#include "Repository.h"
class FileRepo : public Repository{
private:
    std::string filePath;
    void loadActivities();
    void saveActivities();
public:
    FileRepo(std::string filePath);
    ~FileRepo();
    void addActivity(std::string title, std::string description, std::string link, DateTime dateTime, int peopleNumber, int duration) override;
    void removeActivity(std::string title) override;
    void updateActivity(std::string title, std::string description, std::string link, DateTime dateTime, int peopleNumber, int duration)override;
};