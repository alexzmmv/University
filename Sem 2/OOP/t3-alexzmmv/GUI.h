#pragma once


#include <QWidget>
#include <QGridLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QLabel>
#include <QListWidget>
#include "Services.h"

class GUI: public QWidget{

private:
    Services service;
    QWidget *window;
    QGridLayout *layout;
    QListWidget *list;

    QLabel *calculate_label;
    QPushButton *calculate_button;

    QLabel *labela;
    QLineEdit *add_eq_a;

    QLabel *labelb;
    QLineEdit *add_eq_b;

    QLabel *labelc;
    QLineEdit *add_eq_c;

    QPushButton *add_eq_button;

    void populate_list();
    void connect_signals();

public:
    GUI(Services& service);
    void show();
    ~GUI();

};
