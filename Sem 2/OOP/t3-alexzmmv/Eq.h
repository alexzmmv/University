#pragma once
#include <string>

using namespace std;

class Eq {
private:
    double a,b,c;
public:
    Eq(double a,double b,double c);
    string to_string();
    pair<pair<double,double>,pair<double,double>> sol();
    bool is_real();
};