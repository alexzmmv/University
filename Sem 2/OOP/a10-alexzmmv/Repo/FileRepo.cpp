#include "FileRepo.h"
#include <fstream>

FileRepo::FileRepo(std::string filePath) {
    this->filePath = std::move(filePath);
    this->loadActivities();
}

void FileRepo::loadActivities() {
    std::ifstream file(this->filePath);
    if (!file.is_open()) {
        throw RepositoryException("Could not open file: " + this->filePath);
    }
    Activity activity;
    while (file >> activity) {
        this->activities.push_back(new Activity(activity));
    }
    file.close();
}

void FileRepo::saveActivities() {
    std::ofstream file(this->filePath);
    if (!file.is_open()) {
        throw RepositoryException("Could not open file: " + this->filePath);
    }
    for (auto activity : this->activities) {
        file << *activity << '\n';
    }
    file.close();
}

void FileRepo::addActivity(std::string title, std::string description, std::string link, DateTime dateTime, int peopleNumber, int duration) {
    Repository::addActivity(title, description, link, dateTime, peopleNumber, duration);
    this->saveActivities();
}

void FileRepo::removeActivity(std::string title) {
    Repository::removeActivity(title);
    this->saveActivities();
}

void FileRepo::updateActivity(std::string title, std::string description, std::string link, DateTime dateTime, int peopleNumber, int duration) {
    Repository::updateActivity(title, description, link, dateTime, peopleNumber, duration);
    this->saveActivities();
}

FileRepo::~FileRepo() {
    this->saveActivities();
}
