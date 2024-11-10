#pragma once
#include "building.h"
#include <vector>

using namespace std;

class Service {
private:
    vector<building*>buildings;
public:
    Service();
    void addBuilding(building* b);
    vector<building*> getBuildings();
    vector<building*> getDemolishable();
    vector<building*> getReparable(int year);
    vector<building*>getallReparable();
    void writeToFile(string filename, vector<building*> buildings);
};

