#include "Service.h"
#include <fstream>
using namespace std;

Service::Service() {
    buildings = vector<building*>();
}


void Service::addBuilding(building* b) {
    buildings.push_back(b);
}

vector<building*> Service::getBuildings() {
    return buildings;
}

vector<building*> Service::getDemolishable() {
    vector<building*> result;
    for (auto b : buildings) {
        if (b->canbedemolished()) {
            result.push_back(b);
        }
    }
    return result;
}

vector<building*> Service::getReparable(int year) {
    vector<building*> result;
    for (auto b : buildings) {
        if (b->mustberepaired() and b->getConstructionYear() == year) {
            result.push_back(b);
        }
    }
    return result;
}

vector<building*> Service::getallReparable() {
    vector<building*> result;
    for (auto b : buildings) {
        if (b->mustberepaired()) {
            result.push_back(b);
        }
    }
    return result;
}

void Service::writeToFile(std::string filename, vector<building*> buildings) {
    ofstream file(filename.c_str());
    for (auto b : buildings) {
        file << b->toString() << endl;
    }
    file.close();
}

