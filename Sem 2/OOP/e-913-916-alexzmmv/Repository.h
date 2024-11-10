#pragma once

#include "Observer.h"
#include "Domain.h"
class Repository:public Subject{
private:
   std::vector<Courier> couriers;
   std::vector<Package> packages;
   void loadCouriers();
   void loadPackages();
public:
    Repository();
    void addPackage(Package p);
    std::vector<Courier> getCouriers();
    void deliverPackage(int index);
    std::vector<int> getIndexPackagesForCourier(Courier c);

    std::vector<Package> getPackages();

    ~Repository();
};