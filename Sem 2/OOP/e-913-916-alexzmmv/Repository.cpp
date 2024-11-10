
#include "Repository.h"
#include <sstream>
#include <fstream>

Repository::Repository() {
    this->loadCouriers();
    this->loadPackages();
}

void Repository::loadCouriers() {
    /*Couriers.txt format Name|x_coordinate|y_coordinate|radius|street1|stret2...
     * Fanu Curieru|20|20|10|Bucuresti|Ploiesti
     */
    std::string line;
    std::ifstream fin("../couriers.txt");
    while (std::getline(fin, line)) {
        std::istringstream iss(line);
        std::string name;
        double x, y, radius;
        std::vector<std::string> streets;
        std::getline(iss, name, '|');
        iss >> x;
        iss.ignore();
        iss >> y;
        iss.ignore();
        iss >> radius;
        std::string street;
        while (std::getline(iss, street, '|')) {
            streets.push_back(street);
        }
        this->couriers.emplace_back(name, streets, Zone{x, y, radius});
    }
}

void Repository::loadPackages() {
    std::string line;
    std::ifstream fin("../packages.txt");
    while (std::getline(fin, line)) {
        std::istringstream iss(line);
        std::string recipient, street;
        int number;
        double x, y;
        bool delivered;
        std::getline(iss, recipient, '|');
        std::getline(iss, street, '|');
        iss >> number;
        iss.ignore();
        iss >> x;
        iss.ignore();
        iss >> y;
        iss.ignore();
        iss >> delivered;
        this->packages.emplace_back(recipient, Adress{street, number}, x, y, delivered);
    }
}

Repository::~Repository() {
    ofstream fout("../packages.txt");
    for(auto pac:packages){
        fout<<pac.getRecipient()<<"|"<<pac.getAdress().street<<"|"<<pac.getAdress().number<<"|"<<pac.getLocX()<<"|"<<pac.getLocY()<<"|"<<pac.getDeliveryStatus()<<endl;
    }
}

void Repository::addPackage(Package p) {
    this->packages.push_back(p);
}

std::vector<Courier> Repository::getCouriers() {
    return this->couriers;
}

std::vector<Package> Repository::getPackages() {
    return this->packages;
}

std::vector<int> Repository::getIndexPackagesForCourier(Courier c) {
    std::vector<int> index;
    for (int i = 0; i < this->packages.size(); i++) {
        if (!packages[i].getDeliveryStatus() and c.isInCourierZone(this->packages[i])) {
            index.push_back(i);
        }
    }
    return index;
}

void Repository::deliverPackage(int index) {
    this->packages[index].setDeliveryStatus(true);
    notify();
}


