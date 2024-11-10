#pragma once
#include "courierWindow.h"
#include <QLabel>

class CourierCompany: public QWidget, public Observer{
    Q_OBJECT

private:


    Repository& repo;
    QVBoxLayout* mainLayout;
    QListWidget* packageList;
    //add package layout
    QVBoxLayout* addPackageLayout;

    //recipient
    QLabel* recipientLabel;
    QLineEdit* recipientEdit;
    //Street
    QLabel* streetLabel;
    QLineEdit* streetEdit;
    //number
    QLabel* numberLabel;
    QLineEdit* numberEdit;
    //x coordinate
    QLabel* coordXLabel;
    QLineEdit* coordXEdit;
    //y coordinate
    QLabel* coordYLabel;
    QLineEdit* coordYEdit;
    //add package button
    QPushButton* addPackageButton;
    void connectSignals();


    void populateList();
    void update() override;
    void addPackage();;
public:
    CourierCompany(Repository &repo, QWidget *parent=nullptr);

};
