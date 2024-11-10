//
//
// Created by Lenovo on 08/05/2024.

#include <QVBoxLayout>
#include <QLineEdit>
#include <QMessageBox>
#include <QLabel>
#include <QTextStream>
#include <QFileDialog>
#include <QListWidget>
#include <QtChartsVersion>

#include "graphical_ui.h"


Graphical_ui::Graphical_ui(Controller *controller): controller(controller){
    this->buildGUI();
    this->buttonConnect();
    this->populateList();
}

void Graphical_ui::buttonConnect() {
    QObject::connect(this->addButton, &QPushButton::clicked, this, &Graphical_ui::addAdminButtonHandler);
    QObject::connect(this->deleteButton, &QPushButton::clicked, this, &Graphical_ui::deleteAdminButtonHandler);
    QObject::connect(this->updateButton, &QPushButton::clicked, this, &Graphical_ui::updateAdminButtonHandler);
    QObject::connect(this->activityListWidget, &QListWidget::itemSelectionChanged, this, [this]() {
        auto name = this->activityListWidget->currentItem()->text().toStdString();
        name = name.substr(0, name.find(' '));
        try {
            auto activity = this->controller->getActivityByTitle(name);
            this->nameEdit->setText(QString::fromStdString(activity.getTitle()));
            this->descriptionEdit->setText(QString::fromStdString(activity.getDescription()));
            this->linkEdit->setText(QString::fromStdString(activity.getLink()));
            this->dateTimeEdit->setText(QString::fromStdString(activity.getDateTime().toString()));
            this->durationEdit->setText(QString::number(activity.getDuration()));
            this->participantsEdit->setText(QString::number(activity.getPeopleGoing()));
        }
        catch (std::exception &e) {
            return ;
        }
    });
    QObject::connect(this->clearButton, &QPushButton::clicked, this, &Graphical_ui::clearFields);
    QObject::connect(this->userModeButton, &QPushButton::clicked, this, &Graphical_ui::userModeButtonHandler);
    QObject::connect(this->openStatisticsButton, &QPushButton::clicked, this, &Graphical_ui::openStatisticsButtonHandler);
}


void Graphical_ui::populateList() {
    this->activityListWidget->clear();
    for (const auto &activity: this->controller->getActivities()) {
        this->activityListWidget->addItem(QString::fromStdString(activity.toString()));
    }
}

void Graphical_ui::buildGUI() {
    auto *mainLayout = new QVBoxLayout{this};
    this->activityListWidget = new QListWidget{};
    mainLayout->addWidget(activityListWidget, 2, Qt::AlignTop);
    this->activityListWidget->setMinimumWidth(500);
    this->clearButton = new QPushButton{"Clear"};
    mainLayout->addWidget(this->clearButton);
    auto *inputLayout = new QGridLayout{};
    auto *nameLabel = new QLabel{"Name"};
    this->nameEdit = new QLineEdit{};
    auto *descriptionLabel = new QLabel{"Description"};
    this->descriptionEdit = new QLineEdit{};
    auto *linkLabel = new QLabel{"Link"};
    this->linkEdit = new QLineEdit{};
    auto *dateTimeLabel = new QLabel{"Date and Time"};
    this->dateTimeEdit = new QLineEdit{};
    auto *durationLabel = new QLabel{"Duration"};
    this->durationEdit = new QLineEdit{};
    auto *participantsLabel = new QLabel{"Participants"};
    this->participantsEdit = new QLineEdit{};
    this->addButton = new QPushButton{"Add"};
    this->deleteButton = new QPushButton{"Delete"};
    this->updateButton = new QPushButton{"Update"};
    this->openStatisticsButton=new QPushButton{"Statistics"};

    inputLayout->addWidget(nameLabel, 0, 0);
    inputLayout->addWidget(this->nameEdit, 0, 1);
    inputLayout->addWidget(descriptionLabel, 1, 0);
    inputLayout->addWidget(this->descriptionEdit, 1, 1);
    inputLayout->addWidget(linkLabel, 2, 0);
    inputLayout->addWidget(this->linkEdit, 2, 1);
    inputLayout->addWidget(dateTimeLabel, 3, 0);
    inputLayout->addWidget(this->dateTimeEdit, 3, 1);
    inputLayout->addWidget(durationLabel, 4, 0);
    inputLayout->addWidget(this->durationEdit, 4, 1);
    inputLayout->addWidget(participantsLabel, 5, 0);
    inputLayout->addWidget(this->participantsEdit, 5, 1);
    inputLayout->addWidget(this->addButton, 6, 0);
    inputLayout->addWidget(this->deleteButton, 6, 2);
    inputLayout->addWidget(this->updateButton, 6, 1);
    this->userModeButton = new QPushButton{"User mode"};
    inputLayout->addWidget(this->userModeButton, 7, 1);
    inputLayout->addWidget(this->openStatisticsButton,8,1);
    mainLayout->addLayout(inputLayout);
}

void Graphical_ui::clearFields() {
    this->nameEdit->clear();
    this->descriptionEdit->clear();
    this->linkEdit->clear();
    this->dateTimeEdit->clear();
    this->durationEdit->clear();
    this->participantsEdit->clear();
}

void Graphical_ui::addAdminButtonHandler() {
    auto name = this->nameEdit->text().toStdString();
    auto description = this->descriptionEdit->text().toStdString();
    auto link = this->linkEdit->text().toStdString();
    auto date = this->dateTimeEdit->text().toStdString();
    auto participants = this->participantsEdit->text().toStdString();
    auto duration = this->durationEdit->text().toStdString();
    try {
        DateTime dateTime{std::stoi(date.substr(0, 4)), std::stoi(date.substr(5, 2)), std::stoi(date.substr(8, 2)),
                          std::stoi(date.substr(11, 2)), std::stoi(date.substr(14, 2))};
        this->controller->addAdminActivity(name, description, link, dateTime, std::stoi(duration),
                                           std::stoi(participants));
        this->clearFields();
        this->populateList();
    }
    catch (std::exception &e) {
        QMessageBox::critical(this, "Error", "Invalid data");
    }
}

void Graphical_ui::deleteAdminButtonHandler() {
    auto name= this->nameEdit->text().toStdString();
    try {
        this->controller->removeAdminActivity(name);
        this->clearFields();
        this->populateList();
    }
    catch (std::exception &e) {
        QMessageBox::critical(this, "Error", e.what());
    }
}

void Graphical_ui::updateAdminButtonHandler() {
    auto name = this->nameEdit->text().toStdString();
    auto description = this->descriptionEdit->text().toStdString();
    auto link = this->linkEdit->text().toStdString();
    auto date = this->dateTimeEdit->text().toStdString();
    auto participants = this->participantsEdit->text().toStdString();
    auto duration = this->durationEdit->text().toStdString();
    try {
        DateTime dateTime{std::stoi(date.substr(0, 4)), std::stoi(date.substr(5, 2)), std::stoi(date.substr(8, 2)),
                          std::stoi(date.substr(11, 2)), std::stoi(date.substr(14, 2))};
        this->controller->updateAdminActivity(name, description, link, dateTime, std::stoi(duration),
                                              std::stoi(participants));
        this->clearFields();
        this->populateList();
    }
    catch (std::exception &e) {
        QMessageBox::critical(this, "Error", "Invalid data");
    }
}

Graphical_ui::~Graphical_ui() = default;

void Graphical_ui::userModeButtonHandler() {
    try {
        userModeWidget = new QWidget{this, Qt::Window};
        auto *userModeLayout = new QGridLayout{userModeWidget};
        auto *userModeList = new QListWidget{};
        userModeLayout->addWidget(userModeList, 0, 0);
        this->populateUserList();
        auto *monthLabel = new QLabel{"Month"};
        auto *yearLabel = new QLabel{"Year"};
        auto *monthEdit = new QLineEdit{userModeWidget};
        auto *yearEdit = new QLineEdit{userModeWidget};
        monthEdit->setObjectName("month");
        yearEdit->setObjectName("year");
        auto buttonLabelGrid = new QGridLayout{};
        buttonLabelGrid->addWidget(monthLabel, 1, 0);
        buttonLabelGrid->addWidget(monthEdit, 1, 1);
        buttonLabelGrid->addWidget(yearLabel, 2, 0);
        buttonLabelGrid->addWidget(yearEdit, 2, 1);
        auto *deleteButtonUser = new QPushButton{"Delete"};
        deleteButtonUser->setStyleSheet("background-color: red");
        connect(deleteButtonUser, &QPushButton::clicked, this, [this, userModeList]() {
            if(userModeList->currentItem()== nullptr)
                return;
            auto name = userModeList->currentItem()->text().toStdString();
            name = name.substr(0, name.find(' '));
            this->controller->removeActivityFromUser(name);
            userModeList->takeItem(userModeList->currentRow());
        });
        userModeLayout->addWidget(deleteButtonUser, 4, 0);
        auto *saveButton = new QPushButton{"Save"};
        saveButton->setStyleSheet("background-color: green");
        auto *showButton = new QPushButton{"Show"};
        showButton->setStyleSheet("background-color: blue");
        userModeLayout->addLayout(buttonLabelGrid, 1, 0);
        userModeLayout->addWidget(showButton, 2, 0);
        userModeLayout->addWidget(saveButton, 3, 0);
        connect(showButton, &QPushButton::clicked, this,&Graphical_ui::addActivityModeButtonHandler);
        connect(saveButton, &QPushButton::clicked, this, [this, userModeList]() {
            auto filePath = QFileDialog::getSaveFileName(this, "Save user activities", "", "Site (*.html)");
            if (filePath.isEmpty())
                return;
            try {
                //open a box with the file path
                auto path = this->controller->saveUserActivities(filePath.toStdString());
                //open a dialog with 2 buttons: open file, open file and delete
                auto *dialog = new QDialog{this, Qt::Window};
                auto *dialogLayout = new QVBoxLayout{dialog};
                auto *openButton = new QPushButton{"Open and save"};
                auto *openDeleteButton = new QPushButton{"Open"};
                auto *saveButton =new QPushButton{"Save"};
                dialogLayout->addWidget(openButton);
                dialogLayout->addWidget(openDeleteButton);
                dialogLayout->addWidget(saveButton);
                connect(openButton, &QPushButton::clicked, dialog, [dialog, path]() {
                    system(std::string("start " + path).c_str());
                    dialog->close();
                });
                connect(openDeleteButton, &QPushButton::clicked, [dialog, path]() {
                    system(std::string("start " + path).c_str());
                    dialog->close();
                    system(std::string("timeout 1 >nul").c_str());
                    std::remove(path.c_str());
                });
                connect(saveButton,&QPushButton::clicked,[dialog](){
                    dialog->close();
                });
                dialog->show();
            }
            catch (std::exception &e) {
                QMessageBox::critical(this, "Error", e.what());
            }
        });
        userModeWidget->show();

    }
    catch (std::exception &e) {
        QMessageBox::critical(this, "Error", e.what());
    }
}

void Graphical_ui::addActivityModeButtonHandler() {
    auto monthEdit = userModeWidget->findChild<QLineEdit *>("month");
    auto yearEdit = userModeWidget->findChild<QLineEdit *>("year");
    if (monthEdit == nullptr || yearEdit == nullptr) {
        QMessageBox::critical(this, "Error", "Can't find month or year edit");
        return;
    }
    int month, year;
    if(monthEdit->text().isEmpty() && yearEdit->text().isEmpty()){
        //get all activities
        this->activities = this->controller->getActivities();
    }
    else {
        try {
            month = monthEdit->text().toInt();
            year = yearEdit->text().toInt();
            if(month<1 || month>12 || year<0)
                throw std::exception();
        }
        catch (std::exception &e) {
            QMessageBox::critical(this, "Error", "Invalid month or year");
            return;
        }
        this->activities = this->controller->getMonthActivities(month, year);
    }
    if (activities.empty()) {
        QMessageBox::critical(this, "Error", "No activities");
        return;
    }
    this->currentActivity = activities.begin();

    auto *addActivityWidget = new QWidget{this, Qt::Window};
    auto *addActivityLayout = new QVBoxLayout{addActivityWidget};

    auto *activityLabel = new QLabel{QString::fromStdString(currentActivity->toString())};
    addActivityLayout->addWidget(activityLabel);

    auto *addButton = new QPushButton{"Add"};
    auto *skipButton = new QPushButton{"Skip"};
    auto *stopButton = new QPushButton{"Stop"};

    addButton->setStyleSheet("background-color: green");
    skipButton->setStyleSheet("background-color: blue");
    stopButton->setStyleSheet("background-color: red");

    addActivityLayout->addWidget(addButton);
    addActivityLayout->addWidget(skipButton);
    addActivityLayout->addWidget(stopButton);

    connect(addButton, &QPushButton::clicked, this, [this, skipButton]() {
        try {
            this->controller->addActivityToUser(this->currentActivity->getTitle());
            //update the list
            this->populateUserList();
            skipButton->click();
        }
        catch (std::exception &e) {
            QMessageBox::critical(this, "Error", e.what());
        }
    });
    connect(skipButton, &QPushButton::clicked, this, [this, activityLabel]() {
        this->currentActivity++;
        if (this->currentActivity == this->activities.end())
            this->currentActivity = this->activities.begin();
        activityLabel->setText(QString::fromStdString(this->currentActivity->toString()));
        this->userModeWidget->show();
    });
    connect(stopButton, &QPushButton::clicked, addActivityWidget, &QWidget::close);
    addActivityWidget->show();
}

void Graphical_ui::populateUserList() {
    //get the user activities list from userwidget
    auto *userModeList = userModeWidget->findChild<QListWidget *>();
    userModeList->clear();
    for (const auto &activity: this->controller->getUserActivities()) {
        userModeList->addItem(QString::fromStdString(activity.toString()));
    }

}

void Graphical_ui::openStatisticsButtonHandler() {
    try{
        auto statistics = this->controller->statistics();
        auto *statisticsWidget = new QWidget{this, Qt::Window};
        statisticsWidget->setWindowTitle("Statistics");
        statisticsWidget->setMinimumWidth(300);
        statisticsWidget->setMinimumHeight(300);
        statisticsWidget->show();
    }
    catch (std::exception &e) {
        QMessageBox::critical(this, "Error", e.what());
    }
}