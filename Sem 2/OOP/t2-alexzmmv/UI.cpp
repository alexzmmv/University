#include "UI.h"
#include <iostream>
#include <fstream>

using namespace std;
UI::UI() {
    service = Service();
    service.addBuilding(new house(1900, false));
    service.addBuilding(new house(1900, true));
    service.addBuilding(new block(1900, 10, 5));
    service.addBuilding(new block(1900, 1000, 2));
}

void UI::add() {
    int type;
    cout << "Enter the type of building(1-house,2-block): ";
    cin >> type;
    int constructionYear;
    cout << "Enter the construction year: ";
    cin >> constructionYear;
    if (type == 1) {
        bool isHistorical;
        cout << "Is the house historical?(1-yes,0-no): ";
        cin >> isHistorical;
        service.addBuilding(new house(constructionYear, isHistorical));
        return;
    }
    else {
        int totalApartaments, ocupiedApartaments;
        cout << "Enter the total number of apartaments: ";
        cin >> totalApartaments;
        cout << "Enter the number of ocupied apartaments: ";
        cin >> ocupiedApartaments;
        service.addBuilding(new block(constructionYear, totalApartaments, ocupiedApartaments));
        return;
    }
    cout<<"Invalid type!"<<endl;
}

void UI::showall() {
    cout<<"All buildings:"<<endl;
    vector<building*> buildings = service.getBuildings();
    for (auto b : buildings) {
        cout << b->toString() << endl;
    }
    cout<<endl<<endl;
}

void UI::demolishable_and_repairable_to_file() {
    ofstream file1("../file/demolishable.txt");
    ofstream file2("../file/reparable.txt");
    vector<building*> demolishable = service.getDemolishable();
    vector<building*> reparable = service.getallReparable();
    for(auto b:demolishable){
        file1<<b->toString()<<"\n";
    }
    for(auto b:reparable){
        file2<<b->toString()<<"\n";
    }
    file1.close();
    file2.close();
}

void UI::run() {
    while (true) {
        cout << "1.Add building" << endl;
        cout << "2.Show all buildings" << endl;
        cout << "3.Show demolishable and reparable buildings to file" << endl;
        cout << "4.Show all buildings that must be repaired in a certain year" << endl;
        cout << "0.Exit" << endl;
        int command;
        cout << "Enter command: ";
        cin >> command;
        if (command == 1) {
            add();
        }
        else if (command == 2) {
            showall();
        }
        else if (command == 3) {
            demolishable_and_repairable_to_file();
        }
        else if(command == 4){
            int year;
            cout<<"Enter the year: ";
            cin>>year;
            vector<building*> buildings=service.getReparable(year);
            for(auto b:buildings){
                cout<<b->toString()<<"\n";
            }
        }
        else if (command == 0) {
            break;
        }
        else {
            cout << "Invalid command!" << endl;
        }
    }
}

