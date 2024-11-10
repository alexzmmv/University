#include <fstream>
#include "Services.h"

std::vector<Eq> Services::get_eqs() {
    return this->eqs;
}

void Services::add_eq(double a, double b, double c) {
    Eq eq(a, b, c);
    this->eqs.push_back(eq);
}

Services::Services() {
    ifstream fin("../input.txt");
    string line;
    while(!fin.eof()) {
        getline(fin, line);
        double a = stod(line.substr(0, line.find(',')));
        line = line.substr(line.find(',') + 1);
        double b = stod(line.substr(0, line.find(',')));
        line = line.substr(line.find(',') + 1);
        double c = stod(line);
        this->add_eq(a, b, c);
    }
    fin.close();
}

Eq Services::get_eq(int i) {
    return this->eqs[i];
}