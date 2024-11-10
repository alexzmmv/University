#pragma once
#include "../Controller/Controller.h"
#include <iostream>

class Console_ui {
private:
    Controller* controller;
public:
    [[maybe_unused]] explicit Console_ui(Controller* controller);
    ~Console_ui();
    void run();
private:
    static void printAMenu();
    static void printUMenu();
    static void printMenu();
    void printWelcome();
    void addAdminActivity();
    void removeAdminActivity();
    void updateAdminActivity();
    void printAdminActivities();
    void userMode();
    void  userAddActivity();
    void adminMode();

};
