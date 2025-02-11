#include <iostream>
#include "UI/Console_ui.h"
#include "DataBaseRepo.h"
#include "FileRepo.h"
#include "test/test.h"
using namespace std;

int main()
{
    test test;
    test.testall();
    /*
    auto repository=new Repository();
    cout<<"1. File Repo\n"
          "2. Database Repo\n"
          "Choose the repository: "
          <<endl;
    int choice;
    cin>>choice;
    if(choice == 1) {
        cout << "Enter filename(\"default\" for default one):";
        string filename;
        cin >> filename;
        filename = string("../") + filename+".txt";
        repository = new FileRepo(filename);
    }
    if(choice == 2) {
        cout << "Enter database name(\"default\" for default one):";
        string dbName;
        cin >> dbName;
        dbName = string("../") + dbName+".db";
        repository = new DataBaseRepo(dbName);
    }
    auto userPlanner = new UserPlanner();
    cout<<"Choose the user planner: \n";
    cout<<"1. CSV User Planner\n"
          "2. HTML User Planner\n"
          "Choose the user planner: "
          <<endl;
    cin>>choice;
    if(choice == 1) {
        userPlanner = new csvUserPlanner();
    }

    if(choice == 2) {
        userPlanner = new htmlUserPlanner();
    }
    auto controller = new Controller(repository, userPlanner);
    auto  console_ui = Console_ui(controller);
    console_ui.run();
    */
    return 0;
}