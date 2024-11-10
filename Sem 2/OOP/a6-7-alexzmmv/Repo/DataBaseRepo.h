#pragma once
#include <Repository.h>
#include <sqlite3.h>

class DataBaseRepo : public Repository {
private:
    sqlite3* db;
    std::string dbPath;
    void loadActivities();
public:
    DataBaseRepo(std::string dbPath);
    ~DataBaseRepo();
    void addActivity(std::string title, std::string description, std::string link, DateTime dateTime, int peopleNumber, int duration) override;
    void removeActivity(std::string title) override;
    void updateActivity(std::string title, std::string description, std::string link, DateTime dateTime, int peopleNumber, int duration)override;
};