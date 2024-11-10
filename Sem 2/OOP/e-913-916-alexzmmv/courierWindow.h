#pragma once

#include <QWidget>
#include <QGridLayout>
#include <QPushButton>
#include <QLineEdit>
#include <QListWidget>
#include <QComboBox>
#include "Observer.h"
#include "Domain.h"
#include "Repository.h"

class courierWindow : public QWidget, public Observer{
    Q_OBJECT
private:
    Courier courier;
    Repository& repo;
    QVBoxLayout* mainLayout{};

    QListWidget* packageList;
    QPushButton* deliverButton;
    QComboBox* streetCombo;
    void connectSignals();
    void populateList(string street="All");
    void update();

public:
    courierWindow(Courier courier,Repository& r,QWidget* parrent= nullptr);

    ~courierWindow();
};
