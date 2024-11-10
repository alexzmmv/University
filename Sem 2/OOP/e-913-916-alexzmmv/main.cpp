#include <QApplication>
#include <QPushButton>
#include "Repository.h"
#include "courierWindow.h"
#include "CourierCompany.h"
int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    Repository repo{};
    std::vector<Courier> couriers = repo.getCouriers();
    for(auto c:couriers){
        auto w= new courierWindow{c,repo};
        repo.subscribe(w);
        w->show();
    }
    auto w=new CourierCompany{repo};
    repo.subscribe(w);
    w->show();
    return a.exec();
}
