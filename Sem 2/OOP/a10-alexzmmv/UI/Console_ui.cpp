#include "Console_ui.h"

[[maybe_unused]] Console_ui::Console_ui(Controller* controller) {
    this->controller = controller;
}

Console_ui::~Console_ui() {
    delete this->controller;
}

void Console_ui::printWelcome() {
    std::cout << "Welcome to the activity planner!\n";
}

void Console_ui::printMenu() {
    std::cout << "1. Admin mode\n";
    std::cout << "2. User mode\n";
    std::cout << "0. Exit\n";
}



void Console_ui::printAMenu() {
    std::cout << "1. Add activity\n";
    std::cout << "2. Remove activity\n";
    std::cout << "3. Update activity\n";
    std::cout << "4. Print all activities\n";
    std::cout << "5. Undo\n";
    std::cout << "6. Redo\n";
    std::cout << "0. Exit\n";
}

void Console_ui::run() {
    printWelcome();
    printMenu();

    int command;
    std::cin >> command;
    std::cin.ignore();
    while (command != 0) {
        if (command == 1) {
            adminMode();
        }
        else if (command == 2) {
            userMode();
        }
        else {
            std::cout << "Invalid command\n";
        }
        printMenu();
        std::cin >> command;
        std::cin.ignore();
    }
}

void Console_ui::adminMode() {
    printAMenu();
    int command;
    std::cin >> command;
    std::cin.ignore();
    while (command != 0) {
        if (command == 1) {
            addAdminActivity();
        }
        else if (command == 2) {
            removeAdminActivity();
        }
        else if (command == 3) {
            updateAdminActivity();
        }
        else if (command == 4) {
            printAdminActivities();
        }
        else if (command == 5){
            try {
                this->controller->undoAdmin();
            }
            catch (std::exception& e) {
                std::cout << e.what() << std::endl;
            }
        }
        else if (command == 6){
            try {
                this->controller->redoAdmin();
            }
            catch (std::exception& e) {
                std::cout << e.what() << std::endl;
            }
        }
        else {
            std::cout << "Invalid command\n";
        }
        printAMenu();
        std::cin >> command;
        std::cin.ignore();
    }
}
void Console_ui::printUMenu() {
    std::cout << "1. Add activity\n";
    std::cout << "2. Remove activity\n";
    std::cout << "3. Print all user activities\n";
    std::cout << "4. Print all user activities but fancy\n";
    std::cout << "0. Exit\n";
}
void Console_ui::userMode() {
    std::cout << "User mode\n";
    printUMenu();
    int command;
    std::cin >> command;
    std::cin.ignore();
    while (command != 0) {
        if (command == 1) {
            userAddActivity();
        }
        else if (command == 2) {
            std::string title;
            std::cout << "Enter title: ";
            std::getline(std::cin, title);
            try{
            this->controller->removeActivityFromUser(title);
            std::cout<<"Activity removed\n";
            }
            catch(std::exception& e){
                std::cout<<e.what()<<std::endl;
            }
        }
        else if (command == 3) {
            auto activities = controller->getUserActivities();
            for (auto activity : activities) {
                std::cout << activity.toString() << std::endl;
            }
        }
        else if(command==4){
            auto s=std::string();
            try{
                s=controller->saveUserActivities(std::string ("../userActivities"));
            }
            catch(std::exception& e){
                std::cout<<e.what()<<std::endl;
            }
            s="start "+s;
            system(s.c_str());
        }
        else {
            std::cout << "Invalid command\n";
        }
        printUMenu();
        std::cin >> command;
        std::cin.ignore();
    }
}

void Console_ui::userAddActivity() {
    int command;
    std::cout << "1. Show all activities\n";
    std::cout << "2. Show month activities\n";
    std::cin >> command;
    std::cin.ignore();
    std::string com;
    std::vector<Activity> activities;
    while(true) {
        if (command == 1) {
            activities = this->controller->getActivities();
            break;
        }
        if (command == 2) {
            int month, year;
            std::cout << "Enter month and year\n";
            std::cin >> month >> year;
            activities = this->controller->getMonthActivities(month, year);
            break;
        }
        std::cout << "Try again\n";
        std::cin >> command;
        std::cin.ignore();
    }
    if(activities.empty()){
        std::cout<<"No activities\n";
        return;
    }

    auto it=activities.begin();
    while(com.c_str()!="exit"){
        if(it==activities.end()){
            it=activities.begin();
        }
        std::cout<<(*it).toString()<<std::endl;
        std::cout<<"Do you want to add this activity to your list? (yes/no/exit)";
        std::cin>>com;
        if(com=="yes"){
            auto act=*it;
            try {
                this->controller->addActivityToUser(act.getTitle());
                std::cout<<"Activity added\n";
            }
            catch (std::exception& e) {
                std::cout << e.what() << std::endl;
            }
        }
        if(com=="exit"){
            break;
        }
        it++;
    }
}

void Console_ui::addAdminActivity(){
    std::string title, description, link;
    DateTime dateTime;
    int peopleNumber, duration;
    std::cout << "Enter title: ";
    std::getline(std::cin, title);
    std::cout << "Enter description: ";
    std::getline(std::cin, description);
    std::cout << "Enter link: ";
    std::getline(std::cin, link);
    std::cout << "Enter date and time:yyyy mm dd hh mm\n";
    std::cin >> dateTime;
    std::cout << "Enter number of people: ";
    std::cin >> peopleNumber;
    std::cout << "Enter duration in minutes: ";
    std::cin >> duration;
    try {
        this->controller->addAdminActivity(title, description, link, dateTime, duration, peopleNumber);
    }
    catch (std::exception& e) {
        std::cout << e.what() << std::endl;
    }
}

void Console_ui::removeAdminActivity() {
    std::string title;
    std::cout << "Enter title: ";
    std::getline(std::cin, title);
    try {
        this->controller->removeAdminActivity(title);
    }
    catch (std::exception& e) {
        std::cout << e.what() << std::endl;
    }
}

void Console_ui::updateAdminActivity() {
    std::string title, description, link;
    DateTime dateTime;
    int peopleNumber, duration;
    std::cout << "Enter title: ";
    std::getline(std::cin, title);
    std::cout << "Enter description: ";
    std::getline(std::cin, description);
    std::cout << "Enter link: ";
    std::getline(std::cin, link);
    std::cout << "Enter date and time: ";
    std::cin >> dateTime;
    std::cout << "Enter number of people: ";
    std::cin >> peopleNumber;
    std::cout << "Enter duration: ";
    std::cin >> duration;
    try {
        this->controller->updateAdminActivity(title, description, link, dateTime, duration, peopleNumber);
    }
    catch (std::exception& e) {
        std::cout << e.what() << std::endl;
    }
}

void Console_ui::printAdminActivities() {
    auto activities = controller->getAdminActivities();
    for (auto activity : activities) {
        std::cout << activity.toString() << std::endl;
    }
}