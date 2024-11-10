#pragma once
#include "Service.h"
class UI {
private:
    Service service;
    void add();
    void demolishable_and_repairable_to_file();
    void showall();
public:
    UI();
    void run();
};