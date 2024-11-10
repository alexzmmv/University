#include "CourierCompany.h"
#include <QMessageBox>
CourierCompany::CourierCompany(Repository &repo, QWidget *parent) : repo{repo} {
    this->setWindowTitle(QString::fromStdString("Courier Company"));
    this->setMinimumSize(400,400);
    this->setMaximumSize(400,400);
    this->addPackageButton = new QPushButton{"Add Package"};
    this->packageList = new QListWidget{};
    this->recipientLabel = new QLabel{"Recipient"};
    this->recipientEdit = new QLineEdit{};
    this->streetLabel = new QLabel{"Street"};
    this->streetEdit = new QLineEdit{};
    this->numberLabel = new QLabel{"Number"};
    this->numberEdit = new QLineEdit{};
    this->coordXLabel = new QLabel{"X Coordinate"};
    this->coordXEdit = new QLineEdit{};
    this->coordYLabel = new QLabel{"Y Coordinate"};
    this->coordYEdit = new QLineEdit{};
    this->mainLayout = new QVBoxLayout{};
    this->addPackageLayout = new QVBoxLayout{};
    this->addPackageLayout->addWidget(this->recipientLabel);
    this->addPackageLayout->addWidget(this->recipientEdit);
    this->addPackageLayout->addWidget(this->streetLabel);
    this->addPackageLayout->addWidget(this->streetEdit);
    this->addPackageLayout->addWidget(this->numberLabel);
    this->addPackageLayout->addWidget(this->numberEdit);
    this->addPackageLayout->addWidget(this->coordXLabel);
    this->addPackageLayout->addWidget(this->coordXEdit);
    this->addPackageLayout->addWidget(this->coordYLabel);
    this->addPackageLayout->addWidget(this->coordYEdit);
    this->addPackageLayout->addWidget(this->addPackageButton);
    this->mainLayout->addWidget(this->packageList);
    this->mainLayout->addLayout(this->addPackageLayout);
    this->setLayout(this->mainLayout);
    this->connectSignals();
    this->populateList();
}

void CourierCompany::connectSignals() {
    QObject::connect(this->addPackageButton, &QPushButton::clicked, this, &CourierCompany::addPackage);
}

void CourierCompany::populateList() {
    this->packageList->clear();
    int i=0;
    for (auto p: this->repo.getPackages()) {
        auto *item = new QListWidgetItem{};
        item->setData(Qt::UserRole, i++);
        item->setText(QString::fromStdString(p.toString()));
        if(p.getDeliveryStatus())
            item->setBackground(Qt::green);
        this->packageList->addItem(item);
    }
}

void CourierCompany::update() {
    this->populateList();
}

void CourierCompany::addPackage() {
    string recipient = this->recipientEdit->text().toStdString();
    string street = this->streetEdit->text().toStdString();
    int number;
    double x;
    double y;
    try {
        number = this->numberEdit->text().toInt();
        x = this->coordXEdit->text().toDouble();
        y = this->coordYEdit->text().toDouble();
    }
    catch (std::exception &e) {
        QMessageBox::critical(nullptr, "Error", "Invalid input");
        return;
    }
    if(recipient.empty() || street.empty() || number<0 || x<0 || y<0){
        QMessageBox::critical(nullptr, "Error", "Invalid input");
        return;
    }
    this->repo.addPackage(Package{recipient, Adress{street, number},x,y,false});
    repo.notify();
}