#include <fstream>
#include "htmlUserPlanner.h"

htmlUserPlanner::htmlUserPlanner() {
}

htmlUserPlanner::~htmlUserPlanner() {
}

void htmlUserPlanner::addActivity(Activity& activity) {
    this->activities.push_back(&activity);
}

void htmlUserPlanner::removeActivity(Activity& activity) {
    auto it = std::find(this->activities.begin(), this->activities.end(), &activity);
    if (it == this->activities.end())
        std::throw_with_nested(std::invalid_argument("Activity does not exist"));
    activity.decPeopleGoing();
    this->activities.erase(it);
}

void htmlUserPlanner::saveActivities(const std::string filePath) {
    std::ofstream file(filePath.c_str());
    if (!file.is_open()) {
        throw std::runtime_error("Could not open file: " + filePath);
    }
    file<< "<!DOCTYPE html>\n";
    file << "<html>\n";
    file << "<head>\n";
    file << "<title>Activities</title>\n";
    file << "</head>\n";
    file << "<body>\n";
    file << "<table border=\"1\">\n";
    file << "<tr>\n";
    file << "<td>Title</td>\n";
    file << "<td>Description</td>\n";
    file << "<td>People going</td>\n";
    file << "<td>Date and time</td>\n";
    file << "<td>Duration</td>\n";
    file << "<td a=>Link</td>\n";
    file << "</tr>\n";
    for (auto activity : this->activities) {
        file << "<tr>\n";
        file << "<td>" << activity->getTitle() << "</td>\n";
        file << "<td>" << activity->getDescription() << "</td>\n";
        file << "<td>" << activity->getPeopleGoing() << "</td>\n";
        auto dateTime = activity->getDateTime();
        file << "<td>" << dateTime.getYear() << "-" << dateTime.getMonth() << "-" << dateTime.getDay()
             << " " << dateTime.getHour() << ":" << dateTime.getMinute() << "</td>\n";
        file << "<td>" << activity->getDuration() << " seconds </td>\n";
        file << "<td><a href=\"" << activity->getLink() << "\">Link</a></td>\n";
        file << "</tr>\n";

    }
    file << "</table>\n";
    file << "</body>\n";
    file << "</html>\n";
    file.close();
}
