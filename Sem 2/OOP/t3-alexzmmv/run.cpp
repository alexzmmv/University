#include <QApplication>
#include <QWindow>
#include <QLabel>
#include "GUI.h"


int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    Services service;
    GUI gui(service);
    gui.show();
    return a.exec();
}
