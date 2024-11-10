#pragma once
#include <QWidget>
#include <QTableView>
#include "Planner_gui_things/UserPlannerModelForGui.h"
#include <QWidget>
#include <QListWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QRadioButton>

#include <QShortcut>

#include "../Controller/Controller.h"

class Graphical_ui : public QWidget {
Q_OBJECT
private:
    // Controller
    Controller *controller;
    std::vector<Activity> activities;
    std::vector<Activity>::iterator currentActivity;
    //build/initialize the GUI
    void buildGUI();
    void populateList();
    void buttonConnect();
    void clearFields();
    //button handlers
    void addAdminButtonHandler();
    void deleteAdminButtonHandler();
    void updateAdminButtonHandler();
    void userModeButtonHandler();
    void openStatisticsButtonHandler();
    void addActivityModeButtonHandler();
    void undoHandler();
    void redoHandler();
    void populateUserList();
    void showViewButtonHandler();
    // GUI elements
    QWidget *userModeWidget;
    QWidget *statisticsWidget;
    //buttons
    QPushButton *addButton;
    QPushButton *deleteButton;
    QPushButton *updateButton;
    QPushButton *clearButton;
    QPushButton *userModeButton;
    QPushButton *openStatisticsButton;
    QPushButton *undoButton;
    QPushButton *redoButton;
    QPushButton *showViewButton;
    //shortcuts

    QShortcut* undoShortcut;
    QShortcut* redoShortcut1;
    QShortcut* redoShortcut2;
    QShortcut* deleteShortcut;
    //list
    QListWidget *activityListWidget;
    //input fields
    QLineEdit *nameEdit;
    QLineEdit *descriptionEdit;
    QLineEdit *linkEdit;
    QLineEdit *dateTimeEdit;
    QLineEdit *durationEdit;
    QLineEdit *participantsEdit;
public:
    explicit Graphical_ui(Controller *controller);

    ~Graphical_ui() override;
};

class UserPlannerView : public QWidget {
Q_OBJECT

public:
    explicit UserPlannerView(QWidget *parent = nullptr);

    void setActivities(const std::vector<Activity>& activities);

private:
    QTableView *tableView;
    UserPlannerModelForGui *model;
};
