#pragma once

#include <vector>
#include "eq.h"

class Services {
private:
    std::vector<Eq> eqs;
public:
    std::vector<Eq> get_eqs();
    Eq get_eq(int i);
    void add_eq(double a,double b,double c);
    Services();
};
