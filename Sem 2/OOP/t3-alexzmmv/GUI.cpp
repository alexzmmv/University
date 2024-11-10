#include <QMessageBox>
#include "GUI.h"

void GUI::connect_signals() {
    QObject::connect(add_eq_button, &QPushButton::clicked, this, [this]() {
        double a = add_eq_a->text().toDouble();
        double b = add_eq_b->text().toDouble();
        double c = add_eq_c->text().toDouble();
        service.add_eq(a, b, c);
        populate_list();
    });
    //when calculate button is pressed take the selected item from list
    QObject::connect(calculate_button, &QPushButton::clicked, this, [this]() {
        auto *item = list->currentItem();
        if (item == nullptr) {
            return;
        }
        //get index of item
        int index = list->row(item);
        //get the equation from the service
        Eq eq = service.get_eq(index);
        //calculate the result
        auto res=eq.sol();
        string result;
        if(eq.is_real()){
            result="Real roots: \n";
            result=result+"x1="+to_string(res.first.first);
            result+="\n";
            result=result+"x2="+to_string(res.second.first);
            result+="\n";
        }
        else{
            result="Complex roots: \n";
            result=result+"x1="+to_string(res.first.first);
            if(res.first.second>0)
                result=result+"+"+to_string(res.first.second)+"i";
            if(res.first.second<0)
                result=result+to_string(res.first.second)+"i";
            result+="\n";
            result=result+"x2="+to_string(res.second.first);
            if(res.second.second>0)
                result=result+"+"+to_string(res.second.second)+"i";
            if(res.second.second<0)
                result=result+to_string(res.second.second)+"i";
            result+="\n";
        }
        //show the result
        QMessageBox::information(this, "Result", QString::fromStdString(result));

    });
}

void GUI::populate_list() {
    list->clear();
    for (auto& eq:service.get_eqs()) {
        auto* item = new QListWidgetItem();
        item->setText(QString::fromStdString(eq.to_string()));
        if(eq.is_real())
            item->setBackground(Qt::green);
        list->addItem(item);
    }
}

GUI::GUI(Services& service) : service(service) {
    window = new QWidget();
    window->setWindowTitle("Quadratic equations");
    window->setFixedSize(600, 400);
    layout = new QGridLayout();
    list = new QListWidget();
    calculate_label = new QLabel("Calculate");
    calculate_button = new QPushButton("Calculate");
    labela = new QLabel("a");
    add_eq_a = new QLineEdit();
    labelb = new QLabel("b");
    add_eq_b = new QLineEdit();
    labelc = new QLabel("c");
    add_eq_c = new QLineEdit();
    add_eq_button = new QPushButton("Add");
    layout->addWidget(list, 0, 0, 1, 2);
    layout->addWidget(calculate_label, 1, 0);
    layout->addWidget(calculate_button, 1, 1);
    layout->addWidget(labela, 2, 0);
    layout->addWidget(add_eq_a, 2, 1);
    layout->addWidget(labelb, 3, 0);
    layout->addWidget(add_eq_b, 3, 1);
    layout->addWidget(labelc, 4, 0);
    layout->addWidget(add_eq_c, 4, 1);
    layout->addWidget(add_eq_button, 5, 0, 1, 2);
    window->setLayout(layout);
    connect_signals();
    populate_list();
}

void GUI::show() {
    window->show();
}

GUI::~GUI() {

}

