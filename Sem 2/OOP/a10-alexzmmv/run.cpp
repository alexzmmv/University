#include <iostream>
#include "UI/Console_ui.h"
#include "DataBaseRepo.h"
#include "graphical_ui.h"
#include <QApplication>

using namespace std;

int main(int argc , char* argv[])
{
    /*
    auto repository=new Repository();

    repository = new DataBaseRepo("../default.db");

    auto userPlanner = new UserPlannerModelForGui();
    userPlanner = new htmlUserPlanner();
    auto controller = new Controller(repository, userPlanner);
    auto  console_ui = Console_ui(controller);
    console_ui.run();
     return 0;
     */
    //___________________________________
    auto* repository = new DataBaseRepo("../default.db");
    auto* userPlanner = new htmlUserPlanner();
    auto* controller = new Controller(repository, userPlanner);
    QApplication a(argc, argv);
    Graphical_ui gui{controller};
    gui.show();
    return a.exec();

}