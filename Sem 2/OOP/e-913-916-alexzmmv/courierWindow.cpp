
#include "courierWindow.h"
#include <QLabel>
courierWindow::courierWindow(Courier courier,Repository& r, QWidget *parrent) : courier{courier}, QWidget(parrent),repo{r} {
    this->setWindowTitle(QString::fromStdString(courier.getName()));
    this->setMinimumSize(400,400);
    this->setMaximumSize(400,400);
    //a label that show zone x,y,radius
    auto a=new QLabel{QString::fromStdString("Zone: "+to_string(courier.getZone().center_x)+" "+to_string(courier.getZone().center_y)+" "+to_string(courier.getZone().radius))};
    a->setAlignment(Qt::AlignCenter);
    a->setStyleSheet("QLabel { background-color : white; color : black; }");
    a->setFixedSize(400,20);
    deliverButton = new QPushButton{"Deliver"};
    packageList = new QListWidget{};
    streetCombo = new QComboBox{};
    streetCombo->addItem("All");
    for(auto s:courier.getStreets()){
        streetCombo->addItem(QString::fromStdString(s));
    }
    streetCombo->setCurrentIndex(0);
    populateList();
    connectSignals();
    mainLayout = new QVBoxLayout{};
    mainLayout->addWidget(a);
    mainLayout->addWidget(packageList);
    mainLayout->addWidget(streetCombo);
    mainLayout->addWidget(deliverButton);
    this->setLayout(mainLayout);
    this->show();
}

courierWindow::~courierWindow() {
}

void courierWindow::populateList(string street) {
    packageList->clear();
    auto lis=repo.getPackages();
    if(street=="All")
    for(auto p:repo.getIndexPackagesForCourier(courier)){

        auto* item = new QListWidgetItem();
        item->setData(Qt::UserRole,p);
        item->setText(QString::fromStdString(lis[p].toString()));
        packageList->addItem(item);
    }
    else
    for(auto p:repo.getIndexPackagesForCourier(courier)){
        if(lis[p].getAdress().street==street){
            auto* item = new QListWidgetItem();
            item->setData(Qt::UserRole,p);
            item->setText(QString::fromStdString(lis[p].toString()));
            packageList->addItem(item);
        }
    }
}

void courierWindow::update() {
    this->populateList();
    this->show();
}

void courierWindow::connectSignals() {
    QObject::connect(streetCombo, QOverload<int>::of(&QComboBox::currentIndexChanged), [this](){
        string street=streetCombo->currentText().toStdString();
        populateList(street);
    });
    QObject::connect(deliverButton,&QPushButton::clicked,[this](){
        auto items=packageList->selectedItems();
        if(items.empty())
            return;
        auto item=items[0];
        auto index=item->data(Qt::UserRole).toInt();
        repo.deliverPackage(index);
        populateList();
    });

}